# 跨域资源共享 (CORS)：如果你的前端和后端不在同一个域名或端口上运行，可能会遇到 CORS 问题。Flask 默认不允许跨域请求，除非你显式配置允许。
import requests
from flask import Flask, request, jsonify
from flask_cors import CORS  # 导入 CORS 模块

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

if __name__ == '__main__':
    app.run(debug=True)
