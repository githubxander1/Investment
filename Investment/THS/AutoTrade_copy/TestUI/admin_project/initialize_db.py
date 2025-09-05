import sqlite3

try:
    # 连接数据库
    conn = sqlite3.connect('backend/items.db')
    cursor = conn.cursor()
    print('成功连接数据库')

    # 创建referer_links表
    create_table_sql = '''
    CREATE TABLE IF NOT EXISTS referer_links (
        id TEXT PRIMARY KEY,
        project TEXT NOT NULL,
        url TEXT NOT NULL,
        description TEXT
    )
    '''
    cursor.execute(create_table_sql)
    conn.commit()
    print('成功创建referer_links表')

    # 查看表结构
    cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='referer_links'")
    create_table_sql = cursor.fetchone()[0]
    print('表结构:')
    print(create_table_sql)

except Exception as e:
    print(f'错误: {str(e)}')
finally:
    if conn:
        conn.close()