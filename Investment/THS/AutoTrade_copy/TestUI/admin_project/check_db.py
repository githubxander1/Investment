import sqlite3

try:
    # 连接数据库
    conn = sqlite3.connect('backend/items.db')
    cursor = conn.cursor()
    print('成功连接数据库')

    # 检查referer_links表是否存在
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='referer_links'")
    table_exists = cursor.fetchone()
    if table_exists:
        print('referer_links表存在')

        # 查看表结构
        cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='referer_links'")
        create_table_sql = cursor.fetchone()[0]
        print('表结构:')
        print(create_table_sql)

        # 查看数据量
        cursor.execute("SELECT COUNT(*) FROM referer_links")
        count = cursor.fetchone()[0]
        print(f'表中数据量: {count}')
    else:
        print('referer_links表不存在')

except Exception as e:
    print(f'错误: {str(e)}')
finally:
    if conn:
        conn.close()