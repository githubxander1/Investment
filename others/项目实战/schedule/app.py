from flask import Flask, jsonify, request, send_from_directory
import os
import json

app = Flask(__name__)

# 用于存储日程的简单列表
schedules = []

# 用于提供前端文件的路由
@app.route('/')
def index():
    return send_from_directory(os.path.join(app.root_path, 'public'), 'index.html')

# 用于提供前端文件的路由
@app.route('/<path:path>')
def static_file(path):
    return send_from_directory(os.path.join(app.root_path, 'public'), path)

# API 路由
@app.route('/api/schedules', methods=['POST'])
def create_schedule():
    schedule_data = request.get_json()
    schedules.append(schedule_data)
    return jsonify(schedule_data), 201

@app.route('/api/schedules', methods=['GET'])
def get_schedules():
    return jsonify(schedules)

@app.route('/api/schedules/<int:id>', methods=['DELETE'])
def delete_schedule(id):
    global schedules
    schedules = [schedule for i, schedule in enumerate(schedules) if i != id]
    return jsonify({}), 204

if __name__ == '__main__':
    app.run(debug=True)