import sqlite3

# 创建数据库连接
conn = sqlite3.connect('stock_data.db')
cursor = conn.cursor()

# 创建表
cursor.execute('''
CREATE TABLE IF NOT EXISTS lhb_data (
    date TEXT,
    stock_code TEXT,
    stock_name TEXT,
    change REAL,
    net_value REAL,
    buy_value REAL,
    sell_value REAL,
    limit_reason TEXT,
    concept TEXT,
    tags TEXT,
    hot_rank INTEGER
)
''')

# 插入数据
def save_to_db(df, date):
    df['date'] = date
    df.to_sql('lhb_data', conn, if_exists='append', index=False)

# 示例调用
save_to_db(df, "2025-06-13")
