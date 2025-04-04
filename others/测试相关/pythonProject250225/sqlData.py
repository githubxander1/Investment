import pymysql
from web import *

def conMySqlDB():
    # 连接数据库
    global conn
    #conn = pymysql.connect(host='192.168.5.27', port=3306, user='root', password='123456', db='db_public')
    conn = pymysql.connect(host='192.168.5.27', port=3306, user='root', password='123456')
    # 创建游标对象
    global cursor
    cursor= conn.cursor()
    time.sleep(2)


def mysqlClose():
    # 关闭游标和数据库连接
    cursor.close()
    conn.close()

#根据id查询获取电话号码
def agencyTel(id):
    cursor.execute("SELECT phone FROM db_public.t_agency_list where id = '%s'"%id)
    result = cursor.fetchall()
    # 输出所有查询结果
    for row in result:
        return row


'''
def t_acc_account(name):
    cursor.execute("SELECT agencyId FROM 100msh.t_acc_account where agencyId = (SELECT id FROM db_public.t_agency_list where name ='%s')"%name)
    result2 = cursor.fetchall()
    # 输出所有查询结果
    for row in result2:
        return row

def t_agency_list(agencyId):
    cursor.execute("SELECT name,phone FROM db_public.t_agency_list where id = '%s'"%agencyId)
    result = cursor.fetchall()
    # 输出所有查询结果
    for row in result:
        return row
'''