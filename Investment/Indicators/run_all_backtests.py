"""
统一运行所有指标回测的主文件
"""

import sys
import os

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def run_all_backtests():
    """运行所有回测"""
    print("开始运行所有指标回测...")
    
    # 1. 运行顶底指标回测
    try:
        print("\n1. 运行顶底指标回测...")
        from Technology.top_bottom_strategy import main as run_top_bottom
        run_top_bottom()
    except Exception as e:
        print(f"顶底指标回测运行失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 2. 运行主力建仓回测
    try:
        print("\n2. 运行主力建仓回测...")
        from Technology.主力建仓回测 import main as run_main_force
        run_main_force()
    except Exception as e:
        print(f"主力建仓回测运行失败: {e}")
        import traceback
        traceback.print_exc()
    
    # 3. 运行优化CCI回测
    try:
        print("\n3. 运行优化CCI回测...")
        from Technology.优化CCI回测 import main as run_cci
        run_cci()
    except Exception as e:
        print(f"优化CCI回测运行失败: {e}")
        import traceback
        traceback.print_exc()
    
    print("\n所有回测运行完成！")

if __name__ == "__main__":
    run_all_backtests()