import time

from CompanyProject.Payok.Tools.paylabs.GoogleSecure import CalGoogleCode
# from CompanyProject.Payok.交付.paylabs.GoogleSecure import CalGoogleCode
from CompanyProject.Payok.UI.utils.sql_handler import SQLHandler


# def generate_google_code():
#     db_handler = SQLHandler('192.168.0.233', 3306, 'paylabs_payapi', 'SharkZ@DBA666', 'paylabs')
#     db_handler.connect()
#
#     # secret_key = db_handler.get_google_secret_key('2695418206@qq.com')
#     secret_key = db_handler.get_google_secret_key('merchant_operator', 'paylabs2@test.com')
#     if secret_key:
#         print("Google Secret Key:", secret_key)
#
#     db_handler.disconnect()
#     try:
#         current_time = int(time.time()) // 30
#         # print(f"Current Time: {current_time}")
#         generated_code = CalGoogleCode.cal_google_code(secret_key, current_time)
#         print(f"Generated Code: {generated_code}")
#         print(CalGoogleCode.cal_google_code(secret_key))  # 并未实例化CalGoogleCode，也可以调用它的方法
#         return generated_code
#     except ValueError as e:
#         print("错误:", e)

def generate_google_code(host, port, user, password, database, table_name, login_name):
    db_handler = SQLHandler(host, port, user, password, database)
    db_handler.connect()

    secret_key = db_handler.get_google_secret_key(table_name, login_name)
    if secret_key:
        print("谷歌私钥:", secret_key)
    else:
        print(f"未发现给定邮箱:{login_name} 的记录")
        return None

    db_handler.disconnect()
    try:
        current_time = int(time.time()) // 30
        generated_code = CalGoogleCode.cal_google_code(secret_key, current_time)
        # print(f"生成的谷歌验证码: {generated_code}")
        return generated_code
    except ValueError as e:
        print("错误:", e)
        return None
