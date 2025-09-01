import asyncio
import sys
import traceback
import datetime
from Investment.THS.AutoTrade.scripts.portfolio_today.Lhw_portfolio_today import Lhw_main
from Investment.THS.AutoTrade.scripts.portfolio_today.Combination_portfolio_today import Combination_main
from Investment.THS.AutoTrade.scripts.holding.Strategy import StrategyHoldingProcessor
from Investment.THS.AutoTrade.scripts.holding.LhwHoldingProcessor import LhwHoldingProcessor
from Investment.THS.AutoTrade.scripts.holding.CombinationHoldingProcessor import CombinationHoldingProcessor
from Investment.THS.AutoTrade.utils.logger import setup_logger
from Investment.THS.AutoTrade.utils.notification import send_notification

logger = setup_logger("trade_main.log")

async def run_strategy_updates():
    """运行策略数据更新"""
    try:
        logger.info("🚀 开始更新量化王策略数据...")
        has_new_data, new_data = await Lhw_main()
        logger.info("✅ 量化王策略数据更新完成")
        return has_new_data, new_data
    except Exception as e:
        logger.error(f"❌ 量化王策略数据更新失败: {e}")
        send_notification(f"量化王策略数据更新失败: {e}")
        return False, None

async def run_combination_updates():
    """运行组合数据更新"""
    try:
        logger.info("🚀 开始更新组合数据...")
        has_new_data, new_data = await Combination_main()
        logger.info("✅ 组合数据更新完成")
        return has_new_data, new_data
    except Exception as e:
        logger.error(f"❌ 组合数据更新失败: {e}")
        send_notification(f"组合数据更新失败: {e}")
        return False, None

def execute_ai_strategy_trades():
    """执行AI策略交易"""
    try:
        logger.info("🚀 开始执行AI策略交易...")
        processor = StrategyHoldingProcessor()
        success = processor.execute_strategy_trades()
        if success:
            logger.info("✅ AI策略交易执行完成")
            send_notification("AI策略交易执行完成")
        else:
            logger.error("❌ AI策略交易执行失败")
            send_notification("AI策略交易执行失败")
        return success
    except Exception as e:
        logger.error(f"❌ AI策略交易执行异常: {e}")
        send_notification(f"AI策略交易执行异常: {e}")
        return False

def execute_lhw_trades():
    """执行量化王策略交易"""
    try:
        logger.info("🚀 开始执行量化王策略交易...")
        processor = LhwHoldingProcessor()
        success = processor.execute_lhw_trades()
        if success:
            logger.info("✅ 量化王策略交易执行完成")
            send_notification("量化王策略交易执行完成")
        else:
            logger.error("❌ 量化王策略交易执行失败")
            send_notification("量化王策略交易执行失败")
        return success
    except Exception as e:
        logger.error(f"❌ 量化王策略交易执行异常: {e}")
        send_notification(f"量化王策略交易执行异常: {e}")
        return False

def execute_combination_trades():
    """执行组合策略交易"""
    try:
        logger.info("🚀 开始执行组合策略交易...")
        processor = CombinationHoldingProcessor()
        success = processor.execute_combination_trades()
        if success:
            logger.info("✅ 组合策略交易执行完成")
            send_notification("组合策略交易执行完成")
        else:
            logger.error("❌ 组合策略交易执行失败")
            send_notification("组合策略交易执行失败")
        return success
    except Exception as e:
        logger.error(f"❌ 组合策略交易执行异常: {e}")
        send_notification(f"组合策略交易执行异常: {e}")
        return False

async def main():
    """主函数"""
    try:
        logger.info("=== 自动化交易系统启动 ===")
        start_time = datetime.datetime.now()
        logger.info(f"开始时间: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")

        # 1. 更新策略和组合数据
        logger.info("🔄 开始数据更新阶段...")

        # 并行更新策略和组合数据
        lhw_task = run_strategy_updates()
        combination_task = run_combination_updates()

        lhw_result, combination_result = await asyncio.gather(lhw_task, combination_task, return_exceptions=True)

        lhw_success = not isinstance(lhw_result, Exception) and lhw_result[0] if isinstance(lhw_result, tuple) else False
        combination_success = not isinstance(combination_result, Exception) and combination_result[0] if isinstance(combination_result, tuple) else False

        logger.info("✅ 数据更新阶段完成")

        # 2. 执行交易操作
        logger.info("💰 开始交易执行阶段...")

        # 执行AI策略交易
        ai_success = execute_ai_strategy_trades()

        # 如果量化王有新数据或强制执行，执行量化王交易
        lhw_trade_success = True
        if lhw_success:
            lhw_trade_success = execute_lhw_trades()

        # 如果组合有新数据或强制执行，执行组合交易
        combination_trade_success = True
        if combination_success:
            combination_trade_success = execute_combination_trades()

        # 检查所有交易是否成功
        all_trades_success = ai_success and lhw_trade_success and combination_trade_success

        end_time = datetime.datetime.now()
        duration = end_time - start_time

        if all_trades_success:
            logger.info("🎉 所有交易执行成功")
            send_notification(f"自动化交易完成，耗时: {duration.seconds}秒")
        else:
            logger.error("❌ 部分交易执行失败")
            send_notification(f"自动化交易部分失败，耗时: {duration.seconds}秒")

        logger.info(f"结束时间: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")
        logger.info(f"总耗时: {duration.seconds}秒")
        logger.info("=== 自动化交易系统结束 ===")

        return all_trades_success

    except KeyboardInterrupt:
        logger.info("程序被用户中断")
        send_notification("程序被用户中断")
        sys.exit(0)
    except Exception as e:
        error_msg = f"程序执行出现未捕获异常: {str(e)}\n{traceback.format_exc()}"
        logger.error(error_msg)
        send_notification(error_msg)
        sys.exit(1)

if __name__ == '__main__':
    success = asyncio.run(main())
    sys.exit(0 if success else 1)
