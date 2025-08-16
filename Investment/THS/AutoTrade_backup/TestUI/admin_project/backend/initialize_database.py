import os
import sqlite3
import json

# 数据库路径
DATABASE = os.path.join(os.path.dirname(__file__), 'items.db')
# JSON文件路径
JSON_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'frontend', 'data', 'referer_links_detailed.json')

# 初始化数据库
def initialize_database():
    try:
        # 连接数据库
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 创建referer_links表
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS referer_links (
                id TEXT PRIMARY KEY,
                project TEXT NOT NULL,
                url TEXT NOT NULL,
                description TEXT
            )
        ''')
        print('表referer_links创建成功')

        # 如果JSON文件存在，则导入数据
        if os.path.exists(JSON_FILE):
            with open(JSON_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                referer_links = data.get('referer_links', [])

                if referer_links:
                    # 先清空表
                    cursor.execute('DELETE FROM referer_links')
                    print('已清空referer_links表')

                    # 导入数据
                    for link in referer_links:
                        cursor.execute(
                            'INSERT INTO referer_links (id, project, url, description) VALUES (?, ?, ?, ?)',
                            (link['id'], link['project'], link['url'], link.get('description', ''))
                        )
                    print(f'成功导入{len(referer_links)}条数据')

        conn.commit()
        conn.close()
        print('数据库初始化完成')
    except Exception as e:
        print(f'数据库初始化错误: {str(e)}')

if __name__ == '__main__':
    initialize_database()