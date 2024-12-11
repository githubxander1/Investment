import easytrader
from pywinauto import Application
from pywinauto.timings import Timings

Timings.defaults()  # 重置默认等待时间
Timings.slow()      # 使用较慢的等待时间

user = easytrader.use('universal_client')
user.connect(r'D:\Applications\同花顺\hexin.exe')

# 打印余额
try:
    print(user.balance)
except Exception as e:
    print(f"获取余额失败: {e}")

# 打印持仓
try:
    print(user.position)
except Exception as e:
    print(f"获取持仓失败: {e}")
