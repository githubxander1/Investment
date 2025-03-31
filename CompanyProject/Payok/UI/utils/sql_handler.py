import re

import pymysql

class SQLHandler:
    def __init__(self, host, port, user, password, database):
        self.db_config = {
            'host': host,
            'port': port,
            'user': user,
            'password': password,
            'database': database
        }
        self.connection = None

    def connect(self):
        try:
            self.connection = pymysql.connect(**self.db_config)
            # print("Database connection successful.")
        except pymysql.MySQLError as e:
            print(f"连接数据库失败: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()
            print("数据库连接已关闭")

    def get_google_secret_key(self, table_name, login_name):
        if not self.connection:
            print("数据库未连接.")
            return None

        # Ensure the table name is safe
        if not re.match(r'^[a-zA-Z0-9_]+$', table_name):
            print("表名错误")
            return None

        try:
            with self.connection.cursor() as cursor:
                sql = f"SELECT google_secret_key FROM `{table_name}` WHERE login_name=%s"
                cursor.execute(sql, (login_name,))
                result = cursor.fetchone()

                if result:
                    return result[0]
                else:
                    print("未查找到记录.")
                    return None
        except pymysql.MySQLError as e:
            print(f"执行SQL查询时出错: {e}")
            return None

# 使用示例
# if __name__ == "__main__":
#     # db_handler = SQLHandler('192.168.0.227', 3306, 'WAYANGPAY', 'Z43@Mon88', 'aesygo_test')
#     db_handler = SQLHandler('192.168.0.233', 3306, 'paylabs_payapi', 'SharkZ@DBA666', 'paylabs')
#     db_handler.connect()
#
#     # secret_key = db_handler.get_google_secret_key('2695418206@qq.com')
#     secret_key = db_handler.get_google_secret_key('merchant_operator','paylabs2@test.com')
#     if secret_key:
#         print("Google Secret Key:", secret_key)
#
#     db_handler.disconnect()
