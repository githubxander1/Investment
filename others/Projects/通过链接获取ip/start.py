import os
import subprocess
import threading

import requests
from flask import Flask, request, jsonify
from flask_cors import CORS


# 启动 Flask 后端
def start_flask_app():
    app = Flask(__name__)
    CORS(app)  # 允许所有来源的跨域请求

    @app.route('/receive_ip', methods=['POST'])
    def receive_ip():
        print('接收到 /receive_ip 请求')  # 调试信息：接收到请求
        data = request.get_json()
        user_ip = data.get('ip')
        if user_ip:
            print(f'接收到的 IP 地址: {user_ip}')  # 调试信息：接收到的 IP 地址
            try:
                # 使用第三方服务根据 IP 查询地理位置
                response = requests.get(f'http://ip-api.com/json/{user_ip}')
                location_data = response.json()
                print('地理位置信息:', location_data)  # 调试信息：地理位置信息
                return jsonify(location_data)
            except Exception as e:
                print(f'获取地理位置信息时出错: {str(e)}')  # 调试信息：错误信息
                return jsonify({'error': str(e)}), 500
        print('未提供有效的 IP 地址')  # 调试信息：未提供有效的 IP 地址
        return jsonify({'error': '未提供有效的 IP 地址'}), 400

    @app.route('/receive_location', methods=['POST'])
    def receive_location():
        print('接收到 /receive_location 请求')  # 调试信息：接收到请求
        data = request.get_json()
        latitude = data.get('latitude')
        longitude = data.get('longitude')
        if latitude and longitude:
            print(f'接收到的经纬度: 纬度 {latitude}, 经度 {longitude}')  # 调试信息：接收到的经纬度
            try:
                # 可以使用其他地图 API 根据经纬度查询地理位置
                # 这里只是简单返回经纬度信息
                return jsonify({'latitude': latitude, 'longitude': longitude})
            except Exception as e:
                print(f'处理经纬度信息时出错: {str(e)}')  # 调试信息：错误信息
                return jsonify({'error': str(e)}), 500
        print('未提供有效的经纬度信息')  # 调试信息：未提供有效的经纬度信息
        return jsonify({'error': '未提供有效的经纬度信息'}), 400

    # 启动 Flask 应用
    app.run(debug=True)

# 启动前端 HTTP 服务器
def start_http_server():
    # 确保切换到正确的目录
    os.chdir('/z_others/Projects/通过链接获取ip')
    print(f"当前目录: {os.getcwd()}")  # 调试信息：当前目录
    # 使用 subprocess.Popen 启动 HTTP 服务器
    subprocess.Popen(['python', '-m', 'http.server', '8000'])

# 使用多线程同时启动后端和前端服务器
if __name__ == '__main__':
    # 启动前端 HTTP 服务器
    http_thread = threading.Thread(target=start_http_server)
    http_thread.daemon = True
    http_thread.start()

    # 启动 Flask 后端
    start_flask_app()
