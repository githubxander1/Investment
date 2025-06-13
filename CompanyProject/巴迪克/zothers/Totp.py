import pyotp
import time
from CompanyProject.巴迪克.utils.sql_handler import SQLHandler

# 存储账户信息的字典
accounts = {}

def add_account(account_name, secret):
    """
    添加一个新的账户及其对应的 secret
    :param account_name: 账户名称
    :param secret: 账户的 secret
    """
    accounts[account_name] = secret
    print(f"账户 {account_name} 已添加")

def get_totp_code(account_name):
    """
    获取指定账户的当前 TOTP 验证码
    :param account_name: 账户名称
    :return: 当前的 TOTP 验证码或 None（如果账户不存在）
    """
    if account_name in accounts:
        secret = accounts[account_name]
        totp = pyotp.TOTP(secret)
        current_code = totp.now()
        return current_code
    else:
        print(f"账户 {account_name} 不存在")
        return None

def verify_totp_code(account_name, code):
    """
    验证指定账户的 TOTP 验证码是否正确
    :param account_name: 账户名称
    :param code: 用户输入的验证码
    :return: 验证结果（True 或 False）
    """
    if account_name in accounts:
        secret = accounts[account_name]
        totp = pyotp.TOTP(secret)
        is_valid = totp.verify(code)
        return is_valid
    else:
        print(f"账户 {account_name} 不存在")
        return False

def display_codes_for_accounts():
    """
    显示所有账户的 TOTP 验证码
    """
    for account_name in accounts:
        code = get_totp_code(account_name)
        print(f"账户: {account_name}, 当前时间: {time.strftime('%Y-%m-%d %H:%M:%S')}, 验证码: {code}")

# 示例使用
# 平台端
# db_handler = SQLHandler('192.168.0.227', 3306, 'WAYANGPAY', 'Z43@Mon88', 'aesygo_test')
# 商户端
db_handler = SQLHandler('192.168.0.227', 3306, 'WAYANGPAY', 'Z43@Mon88', 'aesygo_test')
db_handler.connect()

# secret_key = db_handler.get_google_secret_key('2695418206@qq.com')
secret_key = db_handler.get_google_secret_key('2695418206@qq.com')
if secret_key:
    add_account("2695418206@qq.com", secret_key)

db_handler.disconnect()

# 获取并打印所有账户的验证码
display_codes_for_accounts()

# 验证某个账户的验证码
account_name = "2695418206@qq.com"
code = get_totp_code(account_name)
if code:
    print(f"账户 {account_name} 的当前验证码是: {code}")
    is_valid = verify_totp_code(account_name, code)
    if is_valid:
        print("验证码验证通过")
    else:
        print("验证码验证失败")

# 循环显示验证码变化
print("接下来的 3 个时间间隔内的验证码：")
for _ in range(3):
    display_codes_for_accounts()
    time.sleep(30)
