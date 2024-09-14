from flask import Flask, jsonify, request, send_from_directory, render_template
import os

app = Flask(__name__)

# 用于存储日程的简单列表
schedules = []

# 处理默认路由
# @app.route('/')#定义默认路由。
# def index():
#     return render_template('index.html')#使用 render_template 渲染 index.html 页面
# 用于提供前端文件的路由
@app.route('/')
def index():
    print(f"Handling request to /")
    print(os.path.join(app.root_path, 'public'))
    return send_from_directory(os.path.join(app.root_path, 'public'), 'index.html')

@app.route('/src/<path:path>')
def send_src(path):
    print(f"Handling request to /src/{path}")
    return send_from_directory('src', path)

# 用于提供前端文件的路由
@app.route('/<path:path>')
def static_file(path):
    print(f"Handling request to /{path}")
    return send_from_directory('public', path)

# API 路由
@app.route('/api/schedules', methods=['POST'])
def create_schedule():
    print(f"Handling POST request to /api/schedules")
    schedule_data = request.get_json()
    schedules.append(schedule_data)
    return jsonify(schedule_data), 201

@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    print(f"Handling GET request to /api/schedules")
    return jsonify(schedules)

@app.route('/api/schedules/<int:id>', methods=['DELETE'])
def delete_schedule(id):
    print(f"Handling DELETE request to /api/schedules/{id}")
    global schedules
    schedules = [schedule for i, schedule in enumerate(schedules) if i != id]
    return jsonify({}), 204

# 打印所有注册的路由
def print_routes():
    for rule in app.url_map.iter_rules():
        print(f"Route: {rule}")

if __name__ == '__main__':
    print("Application root path:", app.root_path)
    print_routes()
    app.run(debug=True)
