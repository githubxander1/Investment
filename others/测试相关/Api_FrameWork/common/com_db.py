
from pymysql import connect, cursors
import psycopg2
import settings


# mysql
class DatabaseMysql:
    def get_mysql_cursor(self):
        conn = connect(
            user=settings.mysql_user,
            password=settings.mysql_password,
            host=settings.mysql_host,
            database=settings.mysql_database,
            port=settings.mysql_port,
            charset="utf8",
            # Cursor\SSCursor\DictCursor\SSDictCursor，有SS的主要用于返回大量数据的查询，或者用于通过慢速网络连接到远程服务器。
            cursorclass=cursors.SSDictCursor  # 查询结果返回字典
        )
        cs = conn.cursor()
        return conn, cs

    def insert(self):
        pass

    def delete(self):
        pass

    def update(self):
        pass

    def select_one(self, sql):
        conn, cs = self.get_mysql_cursor()
        cs.execute(sql)
        return cs.fetchone()

    def select_all(self, sql):
        conn, cs = self.get_mysql_cursor()
        cs.execute(sql)
        return cs.fetchall()


# postgreSql
class DatabasePG:
    def get_pg_cursor(self):
        conn = psycopg2.connect(
            host=settings.pg_host,
            database=settings.pg_database,
            user=settings.pg_user,
            password=settings.pg_password,
            port=settings.pg_port
        )
        cs = conn.cursor()
        return conn, cs

    def insert(self):
        pass

    def delete(self, sql):
        conn, cs = self.get_pg_cursor()
        cs.execute(sql)
        conn.commit()
        cs.close()
        conn.close()

    def update(self):
        pass

    def select_one(self, sql):
        conn, cs = self.get_pg_cursor()
        cs.execute(sql)
        data = cs.fetchone()
        cs.close()
        conn.close()
        return data

    def select_all(self, sql):
        conn, cs = self.get_pg_cursor()
        cs.execute(sql)
        data = cs.fetchall()
        cs.close()
        conn.close()
        return data

