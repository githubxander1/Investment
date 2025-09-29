# 测试信号记录功能
import sys
import os

# 添加项目根目录到路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from utils.logger import log_signal

def test_signal_logging():
    """测试信号记录功能"""
    print("测试信号记录功能...")
    
    # 记录一些测试信号
    log_signal("601088", "阻力支撑", "买入", "测试买入信号")
    log_signal("601088", "扩展指标", "卖出", "测试卖出信号")
    log_signal("601088", "量价指标", "买入", "测试量价买入信号")
    
    print("信号记录完成!")

if __name__ == "__main__":
    test_signal_logging()