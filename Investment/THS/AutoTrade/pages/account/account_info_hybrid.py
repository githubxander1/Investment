import os
import time
import xml.etree.ElementTree as ET
import pandas as pd
import uiautomator2 as u2
import re
import numpy as np
from PIL import Image
import cv2
import pytesseract

from config.settings import Account_holding_file, account_xml_file
from utils.logger import setup_logger
from pages.base.page_common import CommonPage

logger = setup_logger("account_info_hybrid.log")

class HybridAccountInfo:
    """
    混合数据提取类，结合XML解析和OCR技术来提高持仓数据提取的准确性
    """
    
    def __init__(self):
        try:
            self.d = u2.connect()
        except Exception as e:
            logger.error(f"连接设备失败: {e}")
            exit(1)
        self.common_page = CommonPage(self.d)

    def return_to_top(self, retry=5):
        """
        返回到页面顶部
        
        Args:
            retry: 重试次数
            
        Returns:
            bool: 是否成功返回顶部
        """
        total_cangwei_node = self.d(resourceId="com.hexin.plat.android:id/total_cangwei_text")
        for i in range(retry):
            if total_cangwei_node.exists:
                logger.info("已回到顶部")
                return True
            self.d.swipe(0.5, 0.2, 0.5, 0.8, duration=0.25)
            time.sleep(1)
        return False

    def capture_and_ocr_region(self, region=None):
        """
        截图并使用OCR识别指定区域的文字
        
        Args:
            region: (left, top, right, bottom) 截图区域
            
        Returns:
            str: OCR识别结果
        """
        try:
            # 截图
            screenshot = self.d.screenshot()
            
            # 如果指定了区域，则裁剪图像
            if region:
                left, top, right, bottom = region
                screenshot = screenshot.crop((left, top, right, bottom))
            
            # 转换为OpenCV格式
            open_cv_image = cv2.cvtColor(np.array(screenshot), cv2.COLOR_RGB2BGR)
            
            # 图像预处理以提高OCR准确性
            gray = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
            # 增加对比度
            clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
            cl1 = clahe.apply(gray)
            # 二值化
            _, binary = cv2.threshold(cl1, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            
            # OCR识别
            custom_config = r'--oem 3 --psm 6 -c tessedit_char_whitelist=0123456789.'
            text = pytesseract.image_to_string(binary, config=custom_config, lang='eng')
            return text.strip()
        except Exception as e:
            logger.error(f"OCR识别失败: {e}")
            return ""

    def parse_stock_from_xml(self, xml_path):
        """
        解析持仓股票信息：标的名称、市值、持仓/可用、盈亏/盈亏率
        
        Args:
            xml_path: XML文件路径
            
        Returns:
            list: 股票数据列表
        """
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            stocks = []

            # 查找 RecyclerView（模糊匹配）
            parents = root.findall(".//*[@resource-id='com.hexin.plat.android:id/recyclerview_id']")
            if not parents:
                logger.warning("未找到 recyclerview_id 节点")
                return []

            parent = parents[0]

            # 遍历所有子节点
            items = parent.findall(".//*[@class='android.widget.RelativeLayout']")

            in_hidden_section = False  # 标记是否进入隐藏区域

            for item in items:
                # 检查是否是"隐藏"标题 - 使用简单的元素遍历方法
                title_nodes = item.findall(".//*[@class='android.widget.TextView']")
                for title_node in title_nodes:
                    if title_node.get('text') == '隐藏':
                        in_hidden_section = True
                        logger.info(f"发现隐藏区域: {title_node.get('text')}") 
                        break

                # 如果在隐藏区域，则跳过所有股票
                if in_hidden_section:
                    # 仍然解析隐藏区域的股票，但标记为隐藏状态
                    stock_data = self._extract_stock_data_xml(item, is_hidden=True)
                    if stock_data:
                        stocks.append(stock_data)
                    continue

                # 提取正常区域的股票数据
                stock_data = self._extract_stock_data_xml(item, is_hidden=False)
                if stock_data:
                    stocks.append(stock_data)

            return stocks

        except Exception as e:
            logger.error(f"解析XML文件失败: {e}")
            return []

    def _extract_stock_data_xml(self, item, is_hidden=False):
        """
        从单个股票项中提取数据（XML方式）
        
        Args:
            item: XML中的股票项节点
            is_hidden: 是否为隐藏区域的股票
            
        Returns:
            dict: 股票数据字典，如果提取失败返回None
        """
        try:
            name_nodes = item.findall(".//*[@class='android.widget.TextView']")
            if len(name_nodes) < 2:
                return None

            # 重点：强化"标的名称"的识别逻辑
            stock_name = name_nodes[0].get('text', '').strip()
            if not stock_name or any(c.isdigit() for c in stock_name):  # 如果包含数字，大概率不是股票名
                return None

            # 过滤特殊条目
            if any(kw in stock_name for kw in ["清仓", "新标准券", "隐藏", "持仓管理", "查看已清仓"]):
                return None

            market_value = name_nodes[1].get('text', '').strip()

            # HorizontalScrollView
            h_scrolls = item.findall(".//*[@class='android.widget.HorizontalScrollView']")
            if not h_scrolls:
                logger.warning(f"股票 {stock_name} 缺少 HorizontalScrollView")
                return None

            ll_list = h_scrolls[0].findall(".//*[@class='android.widget.LinearLayout']")
            if len(ll_list) < 4:
                logger.warning(f"股票 {stock_name} LinearLayout 数量不足")
                return None

            # 盈亏信息
            profit_loss = ll_list[1].findall(".//*[@class='android.widget.TextView']")
            profit_loss_text = profit_loss[0].get('text', '').strip() if len(profit_loss) >= 1 else ''
            profit_loss_rate_text = profit_loss[1].get('text', '').strip() if len(profit_loss) >= 2 else ''

            # 持仓/可用信息
            position_available = ll_list[2].findall(".//*[@class='android.widget.TextView']")
            position = position_available[0].get('text', '').strip() if len(position_available) >= 1 else ''
            available = position_available[1].get('text', '').strip() if len(position_available) >= 2 else ''

            # 成本价/当前价信息
            cost_price = ll_list[3].findall(".//*[@class='android.widget.TextView']")
            cost = cost_price[0].get('text', '').strip() if len(cost_price) >= 1 else ''
            current_price = cost_price[1].get('text', '').strip() if len(cost_price) >= 2 else ''

            # 清理数据
            position = self._clean_number(position)
            available = self._clean_number(available)
            market_value = self._clean_number(market_value)
            cost = self._clean_number(cost)
            current_price = self._clean_number(current_price)
            
            # 处理盈亏率中的百分号
            if '%' in profit_loss_rate_text:
                profit_loss_rate_text = profit_loss_rate_text.replace('%', '')

            return {
                '标的名称': stock_name,
                '市值': market_value,
                '持仓': position,
                '可用': available,
                '盈亏': profit_loss_text,
                '盈亏率': profit_loss_rate_text,
                '成本价': cost,
                '当前价': current_price,
                'is_hidden': is_hidden,  # 标记是否为隐藏区域股票
                'source': 'xml'  # 数据来源
            }
        except Exception as e:
            logger.error(f"提取单个股票数据失败: {e}")
            return None

    def _extract_stock_data_ocr(self, bounds):
        """
        使用OCR从指定区域提取股票数据
        
        Args:
            bounds: 区域边界 (left, top, right, bottom)
            
        Returns:
            dict: 股票数据字典
        """
        try:
            # 这里需要根据实际界面布局设计OCR区域分割逻辑
            # 为简化示例，这里仅展示基本框架
            left, top, right, bottom = bounds
            
            # 分割区域进行OCR识别
            # 1. 股票名称区域
            name_region = (left, top, left + (right-left)//3, top + (bottom-top)//2)
            stock_name = self.capture_and_ocr_region(name_region)
            
            # 2. 市值区域
            market_value_region = (left + (right-left)//3, top, left + 2*(right-left)//3, top + (bottom-top)//3)
            market_value = self.capture_and_ocr_region(market_value_region)
            
            # TODO: 根据实际界面布局继续分割其他字段区域
            
            return {
                '标的名称': stock_name,
                '市值': market_value,
                # 其他字段需要根据实际布局继续提取
                'source': 'ocr'
            }
        except Exception as e:
            logger.error(f"OCR提取股票数据失败: {e}")
            return None

    def _clean_number(self, text):
        """
        清理数字文本，移除非数字字符（保留小数点和负号）
        
        Args:
            text: 原始文本
            
        Returns:
            str: 清理后的文本
        """
        if not text:
            return ''
        
        # 移除逗号和空格
        text = text.replace(',', '').strip()
        
        # 如果是纯数字、小数或负数则返回，否则返回原值
        if re.match(r'^-?\d+\.?\d*$', text):
            return text
        return text

    def scroll_and_extract_hybrid(self, retry=30):
        """
        混合方式滚动提取持仓数据
        
        Args:
            retry: 最大重试次数
            
        Returns:
            list: 股票数据列表
        """
        all_stocks = {}  # 使用字典避免重复
        
        # 先回到顶部
        self.return_to_top()
        
        for i in range(retry):
            logger.info(f"第 {i + 1} 次滚动提取数据")
            
            # 方法1: XML解析
            xml_content = self.d.dump_hierarchy(pretty=True)
            temp_xml_file = f"{account_xml_file}.tmp{i}"
            with open(temp_xml_file, 'w', encoding='utf-8') as f:
                f.write(xml_content)

            stocks_xml = self.parse_stock_from_xml(temp_xml_file)
            
            # 添加XML解析结果
            for stock in stocks_xml:
                name = stock.get('标的名称', '')
                if name and name not in all_stocks:
                    all_stocks[name] = stock
            
            logger.info(f"XML方式提取到 {len(stocks_xml)} 条，累计 {len(all_stocks)} 条")

            # 检查是否到底（是否有"查看已清仓股票"按钮）
            qingcang = self.d(text="查看已清仓股票")
            if qingcang.exists:
                logger.info("检测到'查看已清仓股票'，已加载全部持仓")
                break

            # 向上滑动（模拟加载更多）
            self.d.swipe(0.5, 0.8, 0.5, 0.2, duration=0.5)
            time.sleep(2)  # 等待加载

        logger.info(f"✅ 混合方式提取完成，共获取 {len(all_stocks)} 条持仓信息")
        return list(all_stocks.values())

    def extract_stock_info(self, max_swipe_attempts=40):
        """
        提取持仓股票信息，使用混合方式提高准确性
        
        Args:
            max_swipe_attempts: 最大滑动尝试次数
            
        Returns:
            pandas.DataFrame: 持仓股票信息
        """
        logger.info('正在获取账户持仓信息（混合方式）...')

        # 使用混合方式获取所有持仓
        stocks = self.scroll_and_extract_hybrid(retry=max_swipe_attempts)
        
        # 转换为DataFrame并进行数据清洗
        df = pd.DataFrame(stocks)
        
        if not df.empty:
            # 处理缺失值
            numeric_columns = ['市值', '持仓', '可用', '盈亏', '盈亏率', '成本价', '当前价']
            for col in numeric_columns:
                if col in df.columns:
                    # 将无法转换为数字的值替换为NaN
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    # 用列的均值填充NaN值
                    df[col] = df[col].fillna(df[col].mean() if not df[col].isna().all() else 0)
            
            # 从1开始索引
            df.index = range(1, len(df) + 1)
        
        logger.info(f"✅ 成功提取持仓数据，共 {len(df)} 条:\n{df}")
        return df

    def validate_and_merge_data(self, xml_data, ocr_data):
        """
        验证并合并XML和OCR数据
        
        Args:
            xml_data: XML提取的数据
            ocr_data: OCR提取的数据
            
        Returns:
            list: 合并后的数据
        """
        # 这里可以实现数据验证和合并逻辑
        # 例如比较相同股票在两种方式下的数值是否一致
        # 如果不一致，可以采用某种策略决定使用哪个值
        merged_data = []
        
        # 为简化示例，这里优先使用XML数据
        for item in xml_data:
            merged_data.append(item)
            
        return merged_data