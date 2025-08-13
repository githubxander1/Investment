import os
import json
import sqlite3
from sqlite3 import Error

# 配置路径
current_dir = os.path.dirname(os.path.abspath(__file__))
json_path = os.path.join(current_dir, 'data', 'referer_links_detailed.json')
DATABASE = os.path.join(current_dir, 'items.db')

# 创建数据库表
def create_referer_links_table():
    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS referer_links (
                id TEXT PRIMARY KEY,
                project TEXT NOT NULL,
                url TEXT NOT NULL,
                description TEXT
            )
        ''')
        conn.commit()
        conn.close()
        print('成功创建referer_links表')
    except Error as e:
        print(f'创建表时出错: {str(e)}')

# 从JSON文件迁移数据到数据库
def migrate_data():
    try:
        # 读取JSON数据
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            referer_links = data.get('referer_links', [])
            print(f'找到 {len(referer_links)} 条链接数据')

        # 连接数据库
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        # 导入数据
        for link in referer_links:
            # 确保必要字段存在
            if 'id' not in link or 'project' not in link or 'url' not in link:
                print(f'跳过无效链接: {link}')
                continue

            # 检查链接是否已存在
            cursor.execute('SELECT id FROM referer_links WHERE id = ?', (link['id'],))
            if cursor.fetchone():
                print(f'链接已存在，跳过: {link["id"]}')
                continue

            # 插入新链接
            cursor.execute(
                'INSERT INTO referer_links (id, project, url, description) VALUES (?, ?, ?, ?)',
                (link['id'], link['project'], link['url'], link.get('description', ''))
            )
            print(f'导入链接成功: {link["id"]}')

        conn.commit()
        conn.close()
        print('数据迁移完成')

    except json.JSONDecodeError as e:
        print(f'JSON解析错误: {str(e)}')
    except Error as e:
        print(f'数据库操作错误: {str(e)}')
    except Exception as e:
        print(f'迁移数据时出错: {str(e)}')

if __name__ == '__main__':
    print('开始数据迁移...')
    create_referer_links_table()
    migrate_data()
    print('数据迁移完成')