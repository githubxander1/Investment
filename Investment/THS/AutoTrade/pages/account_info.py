# account_info1.py
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
from Investment.THS.AutoTrade.pages.page_common import CommonPage

logger = setup_logger("account_info.log")  # 创建日志实例

common_page = CommonPage()

class AccountInfo:
    def __init__(self):
        # 连接设备
        try:
            self.d = u2.connect()
        except Exception as e:
            logger.error(f"连接设备失败: {e}")
            exit(1)

    # 返回顶部
    def return_to_top(self,retry=5):
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
        :param region: (left, top, right, bottom) 截图区域
        :return: OCR识别结果
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

    # 获取xml
    def parse_stock_from_xml(self, xml_path):
        """
        解析持仓股票信息：标的名称、市值、持仓/可用、盈亏/盈亏率
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
            清理后的文本
        """
        if not text:
            return ''
        
        # 移除逗号和空格
        text = text.replace(',', '').strip()
        
        # 如果是纯数字、小数或负数则返回，否则返回原值
        if re.match(r'^-?\d+\.?\d*$', text):
            return text
        return text

    # 滚动获取持仓数据
    def scroll_and_dump(self, retry=30, min_stocks=0):
        """
        滑动并重新 dump XML，直到获取足够多的持仓数据
        :param retry: 最大重试次数
        :param min_stocks: 最小持仓数
        :return: 成功解析的股票列表
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
                name = stock.get('标的名称', '')
                if name and name not in all_stocks:
                    all_stocks[name] = stock
                    
            # 记录隐藏区域的股票（仅记录，不保存）
            for stock in hidden_stocks:
                name = stock.get('标的名称', '')
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

    # 获取账户表头信息
    def extract_header_info(self):
        """提取账户表头信息：总资产、浮动盈亏、总市值、可用、可取"""
        logger.info("-" * 50)
        logger.info('正在获取账户表头信息...')
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
            logger.info(f"账户表头信息完成: \n{header_info_df}")
            return header_info_df

        except Exception as e:
            logger.error(f"获取账户表头信息失败: {e}")
            return pd.DataFrame()

    # 获取持仓股票信息
    def extract_stock_info(self, max_swipe_attempts=40):
        """提取持仓股票信息，支持滑动加载更多，并过滤无效条目"""
        logger.info("-" * 50)
        logger.info('正在获取账户持仓信息...')

        # 使用滚动加载方法获取所有持仓
        stocks = self.scroll_and_dump(retry=max_swipe_attempts)
        
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

    #获取可用资金-买入
    def get_buying_power(self):
        """获取可用资金"""
        try:
            header_info = self.extract_header_info()
            if header_info.empty:
                return None
            buy_available = float(header_info["可用"].iloc[0].replace(',', ''))
            return buy_available
        except Exception as e:
            logger.error(f"获取可用资金失败: {e}")
            return None

    #获取持仓可用-卖出
    def get_stock_available(self,stock_name):
        """获取指定股票的持仓/可用数量"""
        try:
            stock_holding_df = self.extract_stock_info()
            stock_row = stock_holding_df[stock_holding_df["标的名称"] == stock_name]

            if not stock_row.empty:
                # 确保 stock_row 为单行数据
                stock_row = stock_row.iloc[0]

                position_available = stock_row.get("持仓/可用", "")
                if isinstance(position_available, str):
                    parts = position_available.strip().split('/')
                    if len(parts) >= 2:
                        position = int(parts[0])
                        available = int(parts[1])
                        return True, available
                    else:
                        logger.warning(f"持仓/可用字段格式错误: {position_available}")
                        return False, 0
                else:
                    logger.warning(f"持仓/可用字段不是字符串: {position_available}")
                    return False, 0
            else:
                logger.warning(f"{stock_name} 不在持仓中")
                return False, 0
        except Exception as e:
            logger.error(f"获取持仓失败: {e}")
            return False, 0
            
    # 更新指定账户的持仓信息
    def update_holding_info_for_account(self, account_name):
        """
        获取指定账户的持仓信息，并保存到 Excel 文件
        """
        logger.info("-" * 50)
        logger.info(f"开始更新 {account_name} 账户持仓信息...")

        try:
            # 切换到指定账户
            logger.info(f"正在切换到 {account_name} 账户...")
            switch_success = common_page.change_account(account_name)

            # 等待账户切换完成
            time.sleep(2)

            # 检查账户切换是否成功
            if not switch_success:
                logger.warning(f"❌ {account_name} 账户切换失败")
                return False

            # 提取该账户的数据
            header_info_df = self.extract_header_info()
            stocks_df = self.extract_stock_info()

            # 如果数据为空，记录警告
            if header_info_df.empty and stocks_df.empty:
                logger.warning(f"{account_name} 账户数据为空")
                return False

            # 将数据保存到Excel文件的指定工作表中
            try:
                # 如果文件已存在，先读取现有数据
                all_sheets_data = {}
                if os.path.exists(Account_holding_file):
                    with pd.ExcelFile(Account_holding_file, engine='openpyxl') as xls:
                        existing_sheets = xls.sheet_names

                        # 读取除当前账户以外的其他工作表
                        for sheet_name in existing_sheets:
                            if not sheet_name.startswith(f"{account_name}_"):
                                all_sheets_data[sheet_name] = pd.read_excel(xls, sheet_name=sheet_name)

                # 添加当前账户的数据
                if not header_info_df.empty:
                    all_sheets_data[f"{account_name}_表头数据"] = header_info_df
                if not stocks_df.empty:
                    all_sheets_data[f"{account_name}_持仓数据"] = stocks_df

                # 写入所有数据到Excel文件
                with pd.ExcelWriter(Account_holding_file, engine='openpyxl', mode='w') as writer:
                    for sheet_name, df in all_sheets_data.items():
                        df.to_excel(writer, index=False, sheet_name=sheet_name)

                logger.info(f"✅ {account_name} 账户持仓信息已更新并保存至 {Account_holding_file}")
                return True

            except Exception as e:
                logger.error(f"❌ 保存 {account_name} 账户数据失败: {e}", exc_info=True)
                return False

        except Exception as e:
            logger.error(f"❌ 获取 {account_name} 账户持仓信息失败: {e}", exc_info=True)
            return False


    # 更新持仓信息
    def update_holding_info_all(self):
        """
        获取当前账户持仓信息，并保存到 Excel 文件
        """
        logger.info("-" * 50)
        logger.info("开始更新账户持仓信息...")
        # ths = GuozhaiPage(d)
        # ths.ensure_on_holding_page()
        accounts = ["川财证券","长城证券","中泰证券"]

        try:
            account_data = {}

            # 依次获取每个账户的数据
            for account in accounts:
                logger.info(f"正在获取 {account} 账户数据...")
                common_page.change_account(account)

                # 等待账户切换完成
                time.sleep(2)

                # 提取该账户的数据
                header_info_df = self.extract_header_info()
                stocks_df = self.extract_stock_info()

                # 如果数据为空，记录警告但继续处理其他账户
                if header_info_df.empty and stocks_df.empty:
                    logger.warning(f"{account} 账户数据为空")
                    account_data[account] = (pd.DataFrame(), pd.DataFrame())
                    continue

                # 存储该账户的数据
                account_data[account] = (header_info_df, stocks_df)
                logger.info(f"✅ {account} 账户数据获取完成")

            # 将所有账户数据保存到同一个Excel文件的不同工作表中
            if account_data:
                with pd.ExcelWriter(Account_holding_file, engine='openpyxl') as writer:
                    for account, (header_df, stocks_df) in account_data.items():
                        # 保存表头数据到"{account}_表头"工作表
                        if not header_df.empty:
                            header_df.to_excel(writer, index=False, sheet_name=f"{account}_表头数据")

                        # 保存持仓数据到"{account}_持仓"工作表
                        if not stocks_df.empty:
                            stocks_df.to_excel(writer, index=False, sheet_name=f"{account}_持仓数据")

                logger.info(f"✅ 所有账户持仓信息已更新并保存至 {Account_holding_file}")
                return True
            else:
                logger.warning("所有账户数据均为空")
                return False

        except Exception as e:
            logger.error(f"❌ 保存持仓信息失败: {e}", exc_info=True)
            return False




if __name__ == '__main__':
    account = AccountInfo()
    # account.update_holding_info_all()
    account.update_holding_info_for_account('川财证券')
    # get_stock_holding('中国电信')
    # header_info = extract_header_info()
    # buy_available = float(header_info["可用"].iloc[0].replace(',', ''))
    # print(f"可用金额: {buy_available}")