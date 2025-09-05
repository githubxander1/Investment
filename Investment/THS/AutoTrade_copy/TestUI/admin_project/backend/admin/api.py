import os
import sys
import sqlite3
from sqlite3 import Error
from flask import Blueprint, jsonify, request

# 配置数据库路径 - 与home模块共享同一路径
DATABASE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'items.db')

# 创建admin API Blueprint
admin_api_bp = Blueprint('admin_api', __name__)

@admin_api_bp.route('/api/referer-links', methods=['GET'])
def get_referer_links():
    try:
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM referer_links')
            links = [dict(row) for row in cursor.fetchall()]

            # 获取所有项目
            cursor.execute('SELECT DISTINCT project FROM referer_links')
            projects = [row[0] for row in cursor.fetchall()]
            projects.sort()

            return jsonify({
                'referer_links': links,
                'projects': projects
            }), 200
    except Error as e:
        error_msg = f'[ERROR] 数据库错误: {str(e)}'
        print(error_msg, file=sys.stderr)
        return jsonify({'error': error_msg}), 500
    except Exception as e:
        error_msg = f'[ERROR] 读取数据错误: {str(e)}'
        print(error_msg, file=sys.stderr)
        return jsonify({'error': error_msg}), 500

@admin_api_bp.route('/api/items', methods=['POST'])
def add_item():
    try:
        new_item = request.json
        if new_item is None:
            return jsonify({'error': '请提供有效的JSON数据'}), 400

        name = new_item.get('name')
        description = new_item.get('description')

        if not name or not description:
            return jsonify({'error': '项目名称和描述不能为空'}), 400

        with sqlite3.connect(DATABASE) as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO items (name, description) VALUES (?, ?)',
                           (name, description))
            new_item_id = cursor.lastrowid
            conn.commit()

        return jsonify({'id': new_item_id, 'name': name, 'description': description}), 201
    except Error as e:
        error_msg = f'[ERROR] 数据库错误: {str(e)}'
        print(error_msg, file=sys.stderr)
        return jsonify({'error': error_msg}), 500
    except Exception as e:
        error_msg = f'[ERROR] 添加项目错误: {str(e)}'
        print(error_msg, file=sys.stderr)
        return jsonify({'error': error_msg}), 500

@admin_api_bp.route('/api/referer-links/admin', methods=['POST', 'PUT'])
def manage_referer_link():
    try:
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        print(f'[{timestamp}] [DEBUG] 进入manage_referer_link函数，请求方法: {request.method}', file=sys.stderr)
        
        # 获取请求数据
        print(f'[{timestamp}] [DEBUG] 尝试获取请求数据', file=sys.stderr)
        link_data = request.json
        print(f'[{timestamp}] [DEBUG] 请求数据: {link_data}', file=sys.stderr)
        
        if not link_data:
            print(f'[{timestamp}] [WARNING] 请求数据为空', file=sys.stderr)
            return jsonify({'success': False, 'error': '请提供有效的JSON数据'}), 400

        # 验证必要字段
        # 同时支持name/link和project/url参数，保持向后兼容
        name = link_data.get('name') or link_data.get('project')
        link = link_data.get('link') or link_data.get('url')
        print(f'[{timestamp}] [DEBUG] 解析得到名称: {name}, 链接: {link}', file=sys.stderr)
        
        if not name or not link:
            print(f'[{timestamp}] [WARNING] 名称或链接为空，名称: {name}, 链接: {link}', file=sys.stderr)
            return jsonify({'success': False, 'error': '名称和链接不能为空'}), 400

        link_id = link_data.get('id')
        description = link_data.get('description', '')
        print(f'[{timestamp}] [DEBUG] 链接ID: {link_id}, 描述: {description}', file=sys.stderr)

        print(f'[{timestamp}] [DEBUG] 尝试连接数据库: {DATABASE}', file=sys.stderr)
        with sqlite3.connect(DATABASE) as conn:
            print(f'[{timestamp}] [DEBUG] 数据库连接成功', file=sys.stderr)
            cursor = conn.cursor()

            if link_id:
                # 更新现有链接
                print(f'[{timestamp}] [DEBUG] 准备更新现有链接，ID: {link_id}', file=sys.stderr)
                cursor.execute('''
                    UPDATE referer_links
                    SET project = ?, url = ?, description = ?
                    WHERE id = ?
                ''', (name, link, description, link_id))
                updated_rows = cursor.rowcount
                conn.commit()
                print(f'[{timestamp}] [DEBUG] 更新操作完成，影响行数: {updated_rows}', file=sys.stderr)
                
                if updated_rows == 0:
                    print(f'[{timestamp}] [WARNING] 找不到要更新的链接，ID: {link_id}', file=sys.stderr)
                    return jsonify({'success': False, 'error': '找不到要更新的链接'}), 404
                else:
                    print(f'[{timestamp}] [INFO] 链接 {link_id} 更新成功', file=sys.stderr)
                    return jsonify({'success': True, 'message': '链接已成功更新'}), 200
            else:
                # 添加新链接
                print(f'[{timestamp}] [DEBUG] 准备添加新链接', file=sys.stderr)
                # 生成新ID (按名称前缀分类，取最大数字+1)
                name_prefix = name.lower()[:4]  # 取名称前4个字符
                print(f'[{timestamp}] [DEBUG] 名称前缀: {name_prefix}', file=sys.stderr)
                
                # 查找相同名称前缀的最大ID
                print(f'[{timestamp}] [DEBUG] 查找相同名称前缀的最大ID', file=sys.stderr)
                cursor.execute('''
                    SELECT id FROM referer_links
                    WHERE id LIKE ?
                    ORDER BY CAST(SUBSTR(id, INSTR(id, '-') + 1) AS INTEGER) DESC
                    LIMIT 1
                ''', (f'{name_prefix}-%',))
                max_id = cursor.fetchone()
                print(f'[{timestamp}] [DEBUG] 最大ID查询结果: {max_id}', file=sys.stderr)
                
                if max_id:
                    max_num = int(max_id[0].split('-')[1])
                    new_id = f'{name_prefix}-{max_num + 1}'
                else:
                    new_id = f'{name_prefix}-1'
                print(f'[{timestamp}] [DEBUG] 生成的新ID: {new_id}', file=sys.stderr)

                # 插入新链接
                print(f'[{timestamp}] [DEBUG] 准备插入新链接，ID: {new_id}', file=sys.stderr)
                cursor.execute('''
                    INSERT INTO referer_links (id, project, url, description)
                    VALUES (?, ?, ?, ?)
                ''', (new_id, name, link, description))
                conn.commit()
                print(f'[{timestamp}] [INFO] 新链接 {new_id} 添加成功', file=sys.stderr)
                return jsonify({'success': True, 'message': '链接已成功添加', 'id': new_id}), 201
    except Error as e:
        error_msg = f'[ERROR] 数据库错误: {str(e)}'
        print(error_msg, file=sys.stderr)
        return jsonify({'success': False, 'error': error_msg}), 500
    except Exception as e:
        error_msg = f'[ERROR] 管理链接错误: {str(e)}'
        print(error_msg, file=sys.stderr)
        return jsonify({'success': False, 'error': error_msg}), 500

@admin_api_bp.route('/api/referer-links/admin/<string:link_id>', methods=['GET', 'PUT', 'DELETE'])
def manage_referer_link_detail(link_id):
    try:
        import datetime
        timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
        print(f'[{timestamp}] [DEBUG] 进入manage_referer_link_detail函数，链接ID: {link_id}，请求方法: {request.method}', file=sys.stderr)
        
        with sqlite3.connect(DATABASE) as conn:
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            # 查找链接是否存在
            print(f'[{timestamp}] [DEBUG] 查找链接是否存在，ID: {link_id}', file=sys.stderr)
            cursor.execute('SELECT * FROM referer_links WHERE id = ?', (link_id,))
            link = cursor.fetchone()
            if not link:
                print(f'[{timestamp}] [WARNING] 找不到要操作的链接，ID: {link_id}', file=sys.stderr)
                return jsonify({'success': False, 'error': '找不到要操作的链接'}), 404
            else:
                print(f'[{timestamp}] [DEBUG] 找到链接，ID: {link_id}，项目: {link["project"]}', file=sys.stderr)

            if request.method == 'GET':
                # 获取链接详情
                link_dict = dict(link)
                return jsonify({'referer_links': [link_dict]}), 200
            elif request.method == 'PUT':
                # 更新链接
                link_data = request.json
                if not link_data:
                    return jsonify({'success': False, 'error': '请提供有效的JSON数据'}), 400

                # 同时支持name/link和project/url参数，保持向后兼容
                name = link_data.get('name') or link_data.get('project')
                link = link_data.get('link') or link_data.get('url')
                description = link_data.get('description', '')

                if not name or not link:
                    return jsonify({'success': False, 'error': '名称和链接不能为空'}), 400

                cursor.execute('''
                    UPDATE referer_links
                    SET project = ?, url = ?, description = ?
                    WHERE id = ?
                ''', (name, link, description, link_id))
                updated_rows = cursor.rowcount
                conn.commit()

                if updated_rows > 0:
                    return jsonify({'success': True, 'message': '链接已成功更新'}), 200
                else:
                    return jsonify({'success': False, 'error': '更新链接失败'}), 500
            elif request.method == 'DELETE':
                # 删除链接
                import datetime
                timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]
                print(f'[{timestamp}] [DEBUG] 收到删除链接请求，ID: {link_id}', file=sys.stderr)
                print(f'[{timestamp}] [DEBUG] 检查链接是否存在', file=sys.stderr)
                
                # 链接存在性检查已在函数开始部分完成
                print(f'[{timestamp}] [DEBUG] 链接存在，准备执行删除操作', file=sys.stderr)
                
                cursor.execute('DELETE FROM referer_links WHERE id = ?', (link_id,))
                deleted_rows = cursor.rowcount
                conn.commit()
                
                print(f'[{timestamp}] [DEBUG] 删除操作完成，影响行数: {deleted_rows}', file=sys.stderr)
                
                if deleted_rows > 0:
                    print(f'[{timestamp}] [INFO] 链接 {link_id} 删除成功', file=sys.stderr)
                    return jsonify({'success': True, 'message': '链接已成功删除', 'deleted_id': link_id}), 200
                else:
                    print(f'[{timestamp}] [WARNING] 链接 {link_id} 删除失败，未找到该链接', file=sys.stderr)
                    return jsonify({'success': False, 'error': '删除链接失败: 未找到该链接'}), 404
    except Error as e:
        error_msg = f'[ERROR] 数据库错误: {str(e)}'
        print(f'[{timestamp}] {error_msg}', file=sys.stderr)
        return jsonify({'success': False, 'error': error_msg}), 500
    except Exception as e:
        error_msg = f'[ERROR] 管理链接错误: {str(e)}'
        print(f'[{timestamp}] {error_msg}', file=sys.stderr)
        return jsonify({'success': False, 'error': error_msg}), 500