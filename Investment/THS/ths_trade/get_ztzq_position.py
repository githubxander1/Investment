#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
中泰证券持仓查询工具
使用ths_trade项目获取中泰证券账户的持仓信息
"""
import sys
import os
import json
import time
import psutil
import logging

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger('ztzq_position_tool')

def check_ths_running():
    """检查同花顺交易软件是否正在运行"""
    for proc in psutil.process_iter(['name']):
        if proc.info['name'] == 'xiadan.exe':
            logger.info("同花顺交易软件正在运行")
            return True
    logger.warning("警告：同花顺交易软件(xiadan.exe)未运行，请先手动启动并登录中泰证券账户")
    return False

def get_ztzq_position():
    """
    获取中泰证券的持仓信息
    
    Returns:
        dict: 持仓数据
    """
    try:
        # 导入THS交易适配器
        from applications.adapter.ths_trade_adapter import THSTradeAdapter
        
        # 初始化适配器
        logger.info("正在初始化同花顺交易适配器...")
        adapter = THSTradeAdapter(account_name="中泰证券账户")
        
        if not adapter.initialized:
            logger.error("❌ 交易适配器初始化失败")
            return None
        
        logger.info("✅ 交易适配器初始化成功")
        
        # 获取持仓信息
        logger.info("正在获取中泰证券持仓信息...")
        positions = adapter.get_position()
        
        if positions is not None:
            logger.info(f"✅ 成功获取持仓信息，股票数量: {len(positions)}")
            return positions
        else:
            logger.error("❌ 获取持仓信息失败")
            return None
            
    except ImportError as e:
        logger.error(f"❌ 导入THSTradeAdapter失败: {e}")
        return None
    except Exception as e:
        logger.error(f"❌ 获取持仓过程中发生异常: {e}", exc_info=True)
        return None

def display_position_info(positions):
    """
    显示持仓信息
    
    Args:
        positions: 持仓数据
    """
    if not positions:
        print("没有获取到持仓信息")
        return
    
    print("\n=== 中泰证券持仓信息 ===")
    print(f"持仓股票数量: {len(positions)}")
    print("-" * 80)
    
    total_value = 0
    total_cost = 0
    total_profit = 0
    
    # 打印表头
    print(f"{'股票代码':<10} {'股票名称':<10} {'持仓数量':<10} {'可用数量':<10} {'最新价格':<10} {'持仓成本':<10} {'市值':<10} {'盈亏额':<10} {'盈亏比例':<10}")
    print("-" * 80)
    
    # 打印每只股票的信息
    for pos in positions:
        # 处理不同格式的数据结构
        if isinstance(pos, dict):
            stock_code = pos.get('证券代码', '') or pos.get('stock_no', '')
            stock_name = pos.get('证券名称', '') or pos.get('stock_name', '')
            holding_quantity = pos.get('持仓数量', 0) or pos.get('amount', 0)
            available_quantity = pos.get('可用数量', 0) or pos.get('available_amount', 0)
            current_price = pos.get('最新价', 0.0) or pos.get('current_price', 0.0) or pos.get('最新价格', 0.0)
            cost_price = pos.get('摊薄成本价', 0.0) or pos.get('cost_price', 0.0)
            market_value = pos.get('市值', 0.0) or (current_price * holding_quantity)
            profit = pos.get('浮动盈亏', 0.0) or pos.get('profit', 0.0) or (market_value - cost_price * holding_quantity)
        else:
            # 处理DataFrame行数据
            try:
                stock_code = str(pos['证券代码']) if '证券代码' in pos else ''
                stock_name = str(pos['证券名称']) if '证券名称' in pos else ''
                holding_quantity = int(pos['持仓数量']) if '持仓数量' in pos else 0
                available_quantity = int(pos['可用数量']) if '可用数量' in pos else 0
                current_price = float(pos['最新价']) if '最新价' in pos else 0.0
                cost_price = float(pos['摊薄成本价']) if '摊薄成本价' in pos else 0.0
                market_value = float(pos['市值']) if '市值' in pos else (current_price * holding_quantity)
                profit = float(pos['浮动盈亏']) if '浮动盈亏' in pos else (market_value - cost_price * holding_quantity)
            except Exception as e:
                logger.warning(f"处理持仓数据时出错: {e}")
                continue
        
        # 计算盈亏比例
        profit_ratio = (profit / (cost_price * holding_quantity) * 100) if cost_price > 0 and holding_quantity > 0 else 0
        
        # 累计总市值和盈亏
        total_value += market_value
        total_cost += cost_price * holding_quantity
        total_profit += profit
        
        # 打印股票信息
        print(f"{stock_code:<10} {stock_name:<10} {holding_quantity:<10} {available_quantity:<10} "
              f"{current_price:<10.2f} {cost_price:<10.2f} {market_value:<10.2f} {profit:<10.2f} {profit_ratio:<9.2f}%")
    
    print("-" * 80)
    total_profit_ratio = (total_profit / total_cost * 100) if total_cost > 0 else 0
    print(f"总市值: {total_value:.2f} 元")
    print(f"总成本: {total_cost:.2f} 元")
    print(f"总盈亏: {total_profit:.2f} 元 ({total_profit_ratio:.2f}%)")
    print("-" * 80)

def main():
    """主函数"""
    print("===== 中泰证券持仓查询工具 =====")
    print("使用说明：")
    print("1. 请确保同花顺交易软件已启动并登录中泰证券账户")
    print("2. 程序将自动连接同花顺并获取持仓信息")
    print("3. 查询结果将显示每只股票的详细持仓情况和总览")
    print("\n正在检查环境...")
    
    # 检查同花顺是否运行
    if not check_ths_running():
        input("请先启动同花顺交易软件并登录中泰证券账户，然后按Enter键继续...")
    
    # 获取持仓信息
    print("\n正在获取中泰证券持仓数据...")
    position_data = get_ztzq_position()
    
    if position_data:
        # 显示持仓信息
        display_position_info(position_data)
        
        # 保存持仓数据到文件
        timestamp = time.strftime("%Y%m%d_%H%M%S")
        filename = f"ztzq_position_{timestamp}.json"
        
        try:
            # 转换持仓数据为可JSON序列化的格式
            serializable_data = []
            for pos in position_data:
                if isinstance(pos, dict):
                    serializable_data.append(pos)
                else:
                    # 如果是DataFrame行，转换为字典
                    try:
                        pos_dict = {}
                        for key in pos.keys():
                            try:
                                # 尝试转换为基本类型
                                value = pos[key]
                                if isinstance(value, (int, float, str, bool, type(None))):
                                    pos_dict[key] = value
                                else:
                                    pos_dict[key] = str(value)
                            except:
                                pos_dict[key] = "未知"
                        serializable_data.append(pos_dict)
                    except:
                        serializable_data.append({"error": "无法序列化该行数据"})
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(serializable_data, f, ensure_ascii=False, indent=2)
            print(f"\n持仓数据已保存至文件: {filename}")
        except Exception as e:
            logger.error(f"保存持仓数据失败: {e}")
    else:
        print("\n❌ 无法获取中泰证券持仓信息")
        print("请检查以下事项:")
        print("1. 同花顺交易软件是否正常运行")
        print("2. 是否已成功登录中泰证券账户")
        print("3. ths_trade项目是否正确安装")
        print("4. Python环境是否正确配置")

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n程序被用户中断")
    except Exception as e:
        logger.error(f"发生未预期的错误: {e}", exc_info=True)
        print(f"\n发生错误: {e}")
    finally:
        input("\n按Enter键退出...")