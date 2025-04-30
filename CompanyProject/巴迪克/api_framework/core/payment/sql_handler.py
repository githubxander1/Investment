#数据库查询
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
        except pymysql.MySQLError as e:
            print(f"连接数据库失败: {e}")

    def disconnect(self):
        if self.connection:
            self.connection.close()

    def get_google_secret_key(self, table_name, login_name):
        if not self.connection:
            print("数据库未连接.")
            return None

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