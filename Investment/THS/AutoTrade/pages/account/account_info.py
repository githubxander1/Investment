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

from Investment.THS.AutoTrade.config.settings import Account_holding_file, account_xml_file
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.pages.base.page_common import CommonPage

logger = setup_logger("account_info.log")

# 定义all_stocks.xlsx文件路径
ALL_STOCKS_FILE = 'all_stocks.xlsx'

class AccountInfo:
    """
    账户信息管理类，负责账户数据的获取和处理
    """
    
    def __init__(self):
        # 连接设备
        try:
            self.d = u2.connect()
        except Exception as e:
            logger.error(f"连接设备失败: {e}")
            exit(1)
            
        # 加载股票代码和名称映射
        self.stock_code_name_map = self._load_stock_code_name_map()
        self.common_page = CommonPage(self.d)

    def _load_stock_code_name_map(self):
        """
        加载股票代码和名称映射
        
        Returns:
            dict: 股票代码名称映射字典
        """
        stock_map = {}
        if os.path.exists(ALL_STOCKS_FILE):
            try:
                all_stocks_df = pd.read_excel(ALL_STOCKS_FILE)
                # 创建代码到名称的映射
                for _, row in all_stocks_df.iterrows():
                    code = str(row.get('代码', ''))
                    name = str(row.get('名称', ''))
                    if code and name:
                        stock_map[name] = code
                        # 同时添加不带市场前缀的代码映射
                        if code.startswith(('sh', 'sz')):
                            short_code = code[2:]  # 去掉sh或sz前缀
                            stock_map[name] = short_code
                logger.info(f"成功加载 {len(stock_map)} 个股票代码名称映射")
            except Exception as e:
                logger.error(f"加载股票代码名称映射失败: {e}")
        else:
            logger.warning(f"未找到股票代码名称映射文件: {ALL_STOCKS_FILE}")
        return stock_map

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

    def capture_screen_with_ocr(self, region=None):
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
            text = pytesseract.image_to_string(binary, lang='chi_sim+eng')
            return text
        except Exception as e:
            logger.error(f"OCR识别失败: {e}")
            return ""

    def parse_stock_from_xml(self, xml_path):
        """
        解析持仓股票信息：股票名称、市值、持仓/可用、盈亏/盈亏率
        
        Args:
            xml_path: XML文件路径
            
        Returns:
            tuple: (正常股票列表, 隐藏股票列表)
        """
        try:
            tree = ET.parse(xml_path)
            root = tree.getroot()

            stocks = []  # 存储正常区域的股票
            hidden_stocks = []  # 存储隐藏区域的股票

            # 查找 RecyclerView（模糊匹配）
            parents = root.findall(".//*[@resource-id='com.hexin.plat.android:id/recyclerview_id']")
            if not parents:
                logger.warning("未找到 recyclerview_id 节点")
                return [], []

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

                # 提取股票数据
                stock_data = self._extract_stock_data(item)
                if stock_data:
                    if in_hidden_section:
                        # 隐藏区域的股票只记录到日志中
                        hidden_stocks.append(stock_data)
                        logger.info(f"隐藏区域股票数据: {stock_data}")
                    else:
                        # 正常区域的股票添加到返回列表中
                        stocks.append(stock_data)

            return stocks, hidden_stocks

        except Exception as e:
            logger.error(f"解析XML文件失败: {e}")
            return [], []

    def _extract_stock_data(self, item):
        """
        从单个股票项中提取数据
        
        Args:
            item: XML中的股票项节点
            
        Returns:
            dict: 股票数据字典，如果提取失败返回None
        """
        try:
            name_nodes = item.findall(".//*[@class='android.widget.TextView']")
            if len(name_nodes) < 2:
                return None

            # 重点：强化"股票名称"的识别逻辑
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
                '股票名称': stock_name,
                '市值': market_value,
                '持仓': position,
                '可用': available,
                '盈亏': profit_loss_text,
                '盈亏率': profit_loss_rate_text,
                '成本价': cost,
                '当前价': current_price
            }
        except Exception as e:
            logger.error(f"提取单个股票数据失败: {e}")
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

    def scroll_and_dump(self, retry=30, min_stocks=0):
        """
        滑动并重新 dump XML，直到获取足够多的持仓数据
        
        Args:
            retry: 最大重试次数
            min_stocks: 最小持仓数
            
        Returns:
            list: 成功解析的股票列表
        """
        all_stocks = {}  # 使用字典避免重复
        all_hidden_stocks = {}  # 存储隐藏区域的股票信息
        
        # 先回到顶部
        self.return_to_top()
        
        for i in range(retry):
            # 保存当前页面的 XML
            xml_content = self.d.dump_hierarchy(pretty=True)
            temp_xml_file = f"{account_xml_file}.tmp{i}"
            with open(temp_xml_file, 'w', encoding='utf-8') as f:
                f.write(xml_content)

            # 解析持仓
            stocks, hidden_stocks = self.parse_stock_from_xml(temp_xml_file)
            
            # 添加到总列表中，避免重复（仅添加非隐藏区域的股票）
            for stock in stocks:
                name = stock.get('股票名称', '')
                if name and name not in all_stocks:
                    all_stocks[name] = stock
                    
            # 记录隐藏区域的股票（仅记录，不保存）
            for stock in hidden_stocks:
                name = stock.get('股票名称', '')
                if name and name not in all_hidden_stocks:
                    all_hidden_stocks[name] = stock
            
            logger.info(f"第 {i + 1} 次尝试，当前页面提取到 {len(stocks)} 条持仓信息，累计 {len(all_stocks)} 条")

            # 检查是否到底（是否有"查看已清仓股票"按钮）
            qingcang = self.d(text="查看已清仓股票")
            if qingcang.exists:
                logger.info("检测到'查看已清仓股票'，已加载全部持仓")
                break

            # 向上滑动（模拟加载更多）
            logger.info("🔄 页面继续滑动加载...")
            self.d.swipe(0.5, 0.8, 0.5, 0.2, duration=0.5)
            time.sleep(2)  # 等待加载

        logger.info(f"✅ 滚动加载完成，共获取 {len(all_stocks)} 条持仓信息")
        if all_hidden_stocks:
            logger.info(f"🔍 隐藏区域共 {len(all_hidden_stocks)} 条股票信息（仅记录，不保存）")
            hidden_df = pd.DataFrame(list(all_hidden_stocks.values()))
            # 从1开始索引
            hidden_df.index = hidden_df.index + 1
            logger.info(f"隐藏区域股票详情:共 {len(hidden_df)}条\n{hidden_df.to_string(index=True)}")
        return list(all_stocks.values())

    def extract_header_info(self):
        """
        提取账户表头信息：总资产、浮动盈亏、总市值、可用、可取
        
        Returns:
            pandas.DataFrame: 账户表头信息
        """
        logger.info("-" * 50)
        logger.info('开始：获取账户表头信息')
        header_info = {}

        try:
            # 仓位
            total_cangwei_node = self.d(resourceId="com.hexin.plat.android:id/total_cangwei_text")
            header_info["仓位"] = total_cangwei_node.get_text() if total_cangwei_node.exists else "None"

            # 总资产
            total_asset_node = self.d(resourceId="com.hexin.plat.android:id/capital_cell_value",
                                 className="android.widget.TextView", index=2)
            header_info["总资产"] = total_asset_node.get_text() if total_asset_node.exists else "None"

            # 总市值
            total_market_value_node = self.d.xpath('(//*[@resource-id="com.hexin.plat.android:id/capital_cell_value"])[3]')
            header_info["总市值"] = total_market_value_node.get_text() if total_market_value_node.exists else "None"

            # 浮动盈亏
            float_profit_loss_node = self.d(resourceId="com.hexin.plat.android:id/capital_cell_value",
                                       className="android.widget.TextView", index=1)
            header_info["浮动盈亏"] = float_profit_loss_node.get_text() if float_profit_loss_node.exists else "None"

            # 可用
            available_node = self.d.xpath('(//*[@resource-id="com.hexin.plat.android:id/capital_cell_value"])[4]')
            header_info["可用"] = available_node.get_text() if available_node.exists else "None"

            # 可取
            available_for_withdrawal_node = self.d.xpath('(//*[@resource-id="com.hexin.plat.android:id/capital_cell_value"])[5]')
            header_info["可取"] = available_for_withdrawal_node.get_text() if available_for_withdrawal_node.exists else "None"

            header_info_df = pd.DataFrame([header_info])
            logger.info(f"结束：账户表头信息完成: \n{header_info_df}")
            logger.info("-" * 50)
            return header_info_df

        except Exception as e:
            logger.error(f"结束：获取账户表头信息失败: {e}")
            logger.info("-" * 50)
            return pd.DataFrame()

    def extract_stock_info(self, max_swipe_attempts=40):
        """
        提取持仓股票信息，支持滑动加载更多，并过滤无效条目
        
        Args:
            max_swipe_attempts: 最大滑动尝试次数
            
        Returns:
            pandas.DataFrame: 持仓股票信息
        """
        logger.info("-" * 50)
        logger.info('开始：获取账户持仓信息')

        # 使用滚动加载方法获取所有持仓
        stocks = self.scroll_and_dump(retry=max_swipe_attempts)
        
        # 转换为DataFrame并进行数据清洗
        df = pd.DataFrame(stocks)
        
        if not df.empty:
            # 添加代码列（如果不存在）
            if '代码' not in df.columns:
                df['代码'] = df['股票名称'].apply(self._get_stock_code_by_name)
            
            # 处理缺失值
            numeric_columns = ['市值', '持仓', '可用', '盈亏', '盈亏率', '成本价', '当前价', '代码']
            for col in numeric_columns:
                if col in df.columns and col != '代码':  # 代码列不需要数值处理
                    # 将无法转换为数字的值替换为NaN
                    df[col] = pd.to_numeric(df[col], errors='coerce')
                    # 用列的均值填充NaN值
                    df[col] = df[col].fillna(df[col].mean() if not df[col].isna().all() else 0)
            
            # 计算并添加持仓占比列
            try:
                # 获取账户总资产
                header_info = self.extract_header_info()
                if not header_info.empty:
                    total_asset_text = header_info.iloc[0]["总资产"]
                    if total_asset_text and total_asset_text != "None":
                        total_asset = float(str(total_asset_text).replace(',', ''))
                        logger.info(f"账户总资产: {total_asset}")
                        
                        # 计算每只股票的持仓占比，并四舍五入取整
                        if '市值' in df.columns:
                            df['持仓占比'] = (df['市值'] / total_asset * 100).round(0).astype(int)
                            logger.info("已计算持仓占比并取整")
                    else:
                        logger.warning("无法获取账户总资产信息，无法计算持仓占比")
                else:
                    logger.warning("无法获取账户汇总信息，无法计算持仓占比")
            except Exception as e:
                logger.error(f"计算持仓占比时出错: {e}")
            
            # 从1开始索引
            df.index = range(1, len(df) + 1)
        
        logger.info(f"完成：✅ 提取持仓数据，共 {len(df)} 条:\n{df}")
        logger.info("-" * 50)
        return df

    def _get_stock_code_by_name(self, name):
        """
        根据股票名称获取股票代码
        
        Args:
            name: 股票名称
            
        Returns:
            str: 股票代码
        """
        # 从加载的映射中查找代码
        if name in self.stock_code_name_map:
            return self.stock_code_name_map[name]
        else:
            logger.warning(f"未找到股票名称'{name}'对应的代码")
            return f"未知代码({name})"

    def get_buying_power(self):
        """
        获取可用资金
        
        Returns:
            float: 可用资金
        """
        logger.info("-" * 50)
        logger.info('开始：获取可用资金-买入')
        try:
            header_info = self.extract_header_info()
            if header_info.empty:
                return None
            buy_available = float(header_info["可用"].iloc[0].replace(',', ''))
            logger.info(f"完成：获取可用资金，可用金额: {buy_available}")
            logger.info("-" * 50)
            return buy_available
        except Exception as e:
            logger.error(f"完成：获取可用资金失败: {e}")
            logger.info("-" * 50)
            return None

    def get_stock_available(self, stock_name):
        """
        获取指定股票的持仓/可用数量
        
        Args:
            stock_name: 股票名称
            
        Returns:
            tuple: (是否存在, 可用数量)
        """
        logger.info("-" * 50)
        logger.info(f'开始：获取持仓可用-卖出，股票名称: {stock_name}')
        try:
            stock_holding_df = self.extract_stock_info()
            stock_row = stock_holding_df[stock_holding_df["股票名称"] == stock_name]

            if not stock_row.empty:
                # 确保 stock_row 为单行数据
                stock_row = stock_row.iloc[0]

                # 直接获取持仓和可用字段，而不是通过"持仓/可用"组合字段
                position = stock_row.get("持仓", 0)
                available = stock_row.get("可用", 0)
                
                # 确保数据类型正确
                try:
                    position = int(float(position))
                    available = int(float(available))
                    logger.info(f"完成：获取持仓可用-卖出，股票名称: {stock_name}, 持仓: {position}, 可用: {available}")
                    logger.info("-" * 50)
                    return True, available
                except (ValueError, TypeError) as e:
                    logger.warning(f"完成：持仓/可用字段格式错误: 持仓={position}, 可用={available}")
                    logger.info("-" * 50)
                    return False, 0
            else:
                logger.warning(f"{stock_name} 不在持仓中")
                logger.info("-" * 50)
                return False, 0
        except Exception as e:
            logger.error(f"获取持仓失败: {e}")
            logger.info("-" * 50)
            return False, 0
            
    def get_account_summary_info(self):
        """
        获取账户汇总信息：总资产、可用资金、各股票的当前价和可用数量
        
        Returns:
            dict: 账户汇总信息
        """
        logger.info("-" * 50)
        logger.info('开始：获取账户汇总信息')
        
        try:
            # 获取账户表头信息（包含总资产和可用资金）
            header_info_df = self.extract_header_info()
            
            # 获取持仓股票信息（包含各股票的当前价和可用数量）
            stock_info_df = self.extract_stock_info()
            
            # 整合信息
            summary_info = {
                "总资产": None,
                "可用资金": None,
                "持仓股票": []
            }
            
            # 提取总资产和可用资金
            if not header_info_df.empty:
                summary_info["总资产"] = header_info_df.iloc[0]["总资产"]
                summary_info["可用资金"] = header_info_df.iloc[0]["可用"]
            
            # 提取各股票的当前价和可用数量
            if not stock_info_df.empty:
                for _, row in stock_info_df.iterrows():
                    stock_info = {
                        "股票名称": row.get("股票名称", ""),
                        "当前价": row.get("当前价", 0),
                        "可用": row.get("可用", 0)
                    }
                    summary_info["持仓股票"].append(stock_info)
            
            logger.info(f"完成：获取账户汇总信息: {summary_info}")
            logger.info("-" * 50)
            return summary_info
            
        except Exception as e:
            logger.error(f"获取账户汇总信息失败: {e}")
            logger.info("-" * 50)
            return None
            
    def get_account_summary_info_from_file(self, account_file, account_name, stock_name):
        """
        从Excel文件中读取账户信息：总资产、账户余额、股票可用数量、持仓比例、当前价格
        参考trade_logic中的get_account_info方法实现
        
        Args:
            account_file (str): 账户持仓文件路径
            account_name (str): 账户名称，如"川财证券"
            stock_name (str): 股票名称
        
        Returns:
            tuple: (account_asset, account_balance, stock_available, stock_ratio, stock_price)
        """
        logger.info("-" * 50)
        logger.info(f'开始：从文件读取账户信息，账户: {account_name}，股票: {stock_name}')
        
        try:
            # 检查文件是否存在
            if not os.path.exists(account_file):
                logger.error(f"账户持仓文件不存在: {account_file}")
                logger.info("-" * 50)
                return None, None, None, None, None
            
            # 读取Excel文件中的账户汇总和持仓数据
            account_balance_data = pd.read_excel(account_file, sheet_name='账户汇总')
            account_holding_data = pd.read_excel(account_file, sheet_name=account_name)
            
            pd.set_option('display.max_columns', None)
            pd.set_option('display.max_colwidth', None)
            pd.set_option('display.width', None)
            
            logger.debug(f"账户持仓数据:\n{account_holding_data}")
            logger.debug(f"账户汇总数据:\n{account_balance_data}")
            
            # 提取账户信息
            account_row = account_balance_data[account_balance_data['账户名'] == account_name]
            if not account_row.empty:
                account_balance = float(str(account_row['可用'].values[0]).replace(',', ''))
                account_asset = float(str(account_row['总资产'].values[0]).replace(',', ''))
            else:
                logger.warning(f"未找到{account_name}的账户信息")
                account_balance = 0.0
                # 尝试从其他列获取总资产
                asset_columns = ['总资产', '总市值']
                for col in asset_columns:
                    if col in account_row.columns and len(account_row[col].values) > 0:
                        account_asset = float(str(account_row[col].values[0]).replace(',', ''))
                        break
                else:
                    account_asset = 0.0
            
            # 提取股票信息
            # 首先检查账户持仓数据是否为空
            if account_holding_data.empty:
                logger.info(f"{account_name} 账户持仓数据为空")
                stock_available = 0
                stock_ratio = 0
                stock_price = 0
            else:
                stock_data = account_holding_data[account_holding_data['股票名称'] == stock_name]
                
                if not stock_data.empty:
                    stock_available = stock_data['可用'].values[0]
                    stock_ratio = stock_data['持仓占比'].values[0] if '持仓占比' in stock_data.columns else 0
                    stock_price = stock_data['当前价'].values[0]
                    logger.info(f"获取到 {account_name} 账户总资产: {account_asset}, {stock_name} 当前价 {stock_price} 可用数量 {stock_available}, 持仓占比 {stock_ratio}%")
                else:
                    logger.warning(f"未找到{account_name}账户中的股票 {stock_name}")
                    stock_available = 0
                    stock_ratio = 0
                    # 当账户中没有该股票时，仍然需要返回有效的默认值
                    stock_price = 0
            
            logger.info(f"完成：从文件读取账户信息: 账户总资产={account_asset}, 账户余额={account_balance}, 股票可用={stock_available}, 持仓比例={stock_ratio}%, 股票价格={stock_price}")
            logger.info("-" * 50)
            return account_asset, account_balance, stock_available, stock_ratio, stock_price
            
        except Exception as e:
            logger.error(f"从文件读取账户信息失败: {e}")
            logger.info("-" * 50)
            return None, None, None, None, None

    def update_holding_info_for_account(self, account_name):
        """
        获取指定账户的持仓信息，并保存到 Excel 文件
        """
        logger.info("-" * 50)
        logger.info(f"开始：更新 {account_name} 账户持仓信息...")

        try:
            # 切换到指定账户
            logger.info(f"正在切换到 {account_name} 账户...")
            switch_success = self.common_page.change_account(account_name)

            # 等待账户切换完成
            time.sleep(2)

            # 检查账户切换是否成功
            if not switch_success:
                logger.warning(f"❌ {account_name} 账户切换失败")
                return False

            # 提取该账户的数据
            header_info_df = self.extract_header_info()
            stocks_df = self.extract_stock_info()

            # 如果有持仓数据且账户汇总信息不为空，计算持仓占比
            if not stocks_df.empty and not header_info_df.empty:
                try:
                    # 从账户汇总信息中获取总资产
                    total_asset_text = header_info_df.iloc[0]["总资产"]
                    if total_asset_text and total_asset_text != "None":
                        total_asset = float(str(total_asset_text).replace(',', ''))
                        logger.info(f"账户 {account_name} 总资产: {total_asset}")

                        # 计算每只股票的持仓占比，并四舍五入为整数
                        if '市值' in stocks_df.columns:
                            stocks_df['持仓占比'] = (stocks_df['市值'] / total_asset * 100).round(0).astype(int)
                            logger.info(f"已为账户 {account_name} 的持仓股票计算持仓占比")
                    else:
                        logger.warning(f"账户 {account_name} 无总资产信息，无法计算持仓占比")
                except Exception as e:
                    logger.error(f"计算持仓占比时出错: {e}")

            # 如果数据为空，记录警告
            if header_info_df.empty and stocks_df.empty:
                logger.warning(f"{account_name} 账户数据为空")
                return False
        except Exception as e:
            logger.error(f"获取 {account_name} 账户数据时出错: {e}", exc_info=True)
            return False

        logger.info(f"完成：✅ {account_name} 账户持仓信息已更新")
        return header_info_df, stocks_df

    def _update_account_summary(self, all_sheets_data, account_name, header_info_df):
        """
        更新账户汇总信息
        
        :param all_sheets_data: 所有工作表数据的字典
        :param account_name: 账户名称
        :param header_info_df: 表头信息DataFrame
        """
        try:
            # 初始化或读取现有的账户汇总数据
            if '账户汇总' in all_sheets_data:
                summary_df = all_sheets_data['账户汇总']
            else:
                summary_df = pd.DataFrame(columns=['账户名', '仓位', '总资产', '总市值', '浮动盈亏', '可用', '可取'])
            
            # 从表头信息中提取账户数据
            if not header_info_df.empty:
                # 创建新行数据
                new_row_data = {
                    '账户名': account_name,
                    '仓位': header_info_df.iloc[0].get('仓位', 'None'),
                    '总资产': header_info_df.iloc[0].get('总资产', 'None'),
                    '总市值': header_info_df.iloc[0].get('总市值', 'None'),
                    '浮动盈亏': header_info_df.iloc[0].get('浮动盈亏', 'None'),
                    '可用': header_info_df.iloc[0].get('可用', 'None'),
                    '可取': header_info_df.iloc[0].get('可取', 'None')
                }
                
                # 检查账户是否已存在于汇总数据中
                existing_idx = summary_df[summary_df['账户名'] == account_name].index
                
                if len(existing_idx) > 0:
                    # 更新现有记录
                    for col, value in new_row_data.items():
                        summary_df.at[existing_idx[0], col] = value
                else:
                    # 添加新记录
                    new_row = pd.DataFrame([new_row_data])
                    summary_df = pd.concat([summary_df, new_row], ignore_index=True)
                
                # 更新账户汇总数据
                all_sheets_data['账户汇总'] = summary_df
                
            logger.info(f"已更新 {account_name} 的账户汇总信息")
        except Exception as e:
            logger.error(f"更新账户汇总信息失败: {e}")

    def update_holding_info_all(self):
        """
        获取当前账户持仓信息，并保存到 Excel 文件
        """
        logger.info("-" * 50)
        logger.info("开始：更新账户持仓信息...")
        # ths = GuozhaiPage(d)
        # ths.ensure_on_holding_page()
        accounts = ["川财证券","长城证券","中泰证券","中山证券"]

        try:
            account_data = {}
            summary_data = []  # 用于存储汇总数据

            # 依次获取每个账户的数据
            for account in accounts:
                logger.info(f"正在获取 {account} 账户数据...")
                self.common_page.change_account(account)

                # 等待账户切换完成
                time.sleep(2)

                # 提取该账户的数据
                header_info_df = self.extract_header_info()
                stocks_df = self.extract_stock_info()
                
                # 如果有持仓数据且账户汇总信息不为空，计算持仓占比
                if not stocks_df.empty and not header_info_df.empty:
                    try:
                        # 从账户汇总信息中获取总资产
                        total_asset_text = header_info_df.iloc[0]["总资产"]
                        if total_asset_text and total_asset_text != "None":
                            total_asset = float(str(total_asset_text).replace(',', ''))
                            logger.info(f"账户 {account} 总资产: {total_asset}")
                            
                            # 计算每只股票的持仓占比，并四舍五入为整数
                            if '市值' in stocks_df.columns:
                                stocks_df['持仓占比'] = (stocks_df['市值'] / total_asset * 100).round(0).astype(int)
                                logger.info(f"已为账户 {account} 的持仓股票计算持仓占比")
                        else:
                            logger.warning(f"账户 {account} 无总资产信息，无法计算持仓占比")
                    except Exception as e:
                        logger.error(f"计算持仓占比时出错: {e}")

                # 如果数据为空，记录警告但继续处理其他账户
                if header_info_df.empty and stocks_df.empty:
                    logger.warning(f"{account} 账户数据为空")
                    account_data[account] = (pd.DataFrame(), pd.DataFrame())
                    continue

                # 存储该账户的数据
                account_data[account] = (header_info_df, stocks_df)
                logger.info(f"完成：✅ {account} 账户数据获取完成")
                # logger.info("-" * 50)
                
                # 添加账户数据到汇总表
                if not header_info_df.empty:
                    header_info_copy = header_info_df.copy()
                    header_info_copy['账户名'] = account  # 添加账户名列
                    summary_data.append(header_info_copy)

            # 将所有账户数据保存到同一个Excel文件的不同工作表中
            if account_data:
                with pd.ExcelWriter(Account_holding_file, engine='openpyxl') as writer:
                    # 保存汇总表头数据到"账户汇总"工作表
                    if summary_data:
                        summary_df = pd.concat(summary_data, ignore_index=True)
                        summary_df.to_excel(writer, index=False, sheet_name="账户汇总")
                    
                    # 保存各账户详细数据
                    for account, (header_df, stocks_df) in account_data.items():
                        # 保存表头数据到"{account}_表头"工作表
                        # if not header_df.empty:
                        #     header_df.to_excel(writer, index=False, sheet_name=f"{account}")

                        # 保存持仓数据到"{account}_持仓"工作表
                        # 即使持仓为空也创建空的工作表
                        stocks_df.to_excel(writer, index=False, sheet_name=f"{account}")

                logger.info(f"完成：✅ 所有账户持仓信息已更新并保存至 {Account_holding_file}")
                logger.info("-" * 50)
                return True
            else:
                logger.warning("所有账户数据均为空")
                return False

        except Exception as e:
            logger.error(f"❌ 保存持仓信息失败: {e}", exc_info=True)
            return False

if __name__ == '__main__':
    account = AccountInfo()
    account.update_holding_info_for_account("中山证券")
    # account.update_holding_info_all()
    # account.update_holding_info_all()