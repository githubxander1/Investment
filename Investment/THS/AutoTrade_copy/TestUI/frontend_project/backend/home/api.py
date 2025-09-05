import os
import json
import sqlite3
from sqlite3 import Error
from flask import Blueprint, jsonify, request

# 创建home API Blueprint
home_api_bp = Blueprint('home_api', __name__)

# 配置数据库路径
DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'items.db')

# 确保路径正确
if not os.path.exists(DATABASE):
    print(f"警告: 数据库文件不存在: {DATABASE}")

@home_api_bp.route('/api/items', methods=['GET'])
def get_items():
    try:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row  # 使结果可以通过列名访问
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM items')
        items = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return jsonify({'items': items})
    except Error as e:
        return jsonify({'error': str(e)}), 500

@home_api_bp.route('/api/referer-links', methods=['GET'])
def get_referer_links():
    try:
        # 读取详细的referer_links_detailed.json文件
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), '../data/referer_links_detailed.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@home_api_bp.route('/api/referer-links/filter', methods=['GET'])
def filter_referer_links():
    try:
        # 获取筛选参数
        project = request.args.get('project')
        link_id = request.args.get('id')

        # 读取详细的referer_links_detailed.json文件
        with open(os.path.join(os.path.dirname(os.path.dirname(__file__)), '../data/referer_links_detailed.json'), 'r', encoding='utf-8') as f:
            data = json.load(f)

        # 应用筛选
        filtered_links = data['referer_links']
        if project:
            filtered_links = [link for link in filtered_links if link['project'] == project]
        if link_id:
            filtered_links = [link for link in filtered_links if link['id'] == link_id]

        return jsonify({
            'referer_links': filtered_links,
            'projects': data['projects']
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500