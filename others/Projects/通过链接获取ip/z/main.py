import math
import threading

import requests
from kivy.app import App
from kivy.uix.label import Label
from plyer import gps


class LocationApp(App):
    def build(self):
        # 初始化标签，用于显示状态信息
        self.label = Label(text="Starting...")
        # 初始化上次位置信息
        self.last_location = None
        # 初始化上一次位置信息
        self.previous_location = None
        # 启动GPS
        self.start_gps()
        return self.label

    def start_gps(self):
        try:
            # 配置GPS监听器
            gps.configure(on_location=self.on_location, on_status=self.on_status)
            # 启动GPS
            gps.start(minTime=1000, minDistance=0)
        except Exception as e:
            # 显示错误信息
            self.label.text = str(e)

    def on_location(self, **kwargs):
        # 更新上次位置信息
        self.last_location = kwargs
        # 更新显示信息
        self.label.text = f"Lat: {self.last_location['lat']}, Lon: {self.last_location['lon']}"
        # 检查位置变化
        self.check_location_change()

    def on_status(self, stype, status):
        # 更新显示信息
        self.label.text = f"GPS: {status}"

    def check_location_change(self):
        if self.last_location:
            lat1, lon1 = self.last_location['lat'], self.last_location['lon']
            if self.previous_location:
                lat2, lon2 = self.previous_location['lat'], self.previous_location['lon']
                distance = self.calculate_distance(lat1, lon1, lat2, lon2)
                if distance > 100:
                    self.send_data_to_server(lat1, lon1)
            # 更新上一次位置信息
            self.previous_location = self.last_location

    def calculate_distance(self, lat1, lon1, lat2, lon2):
        # 计算两个经纬度之间的距离（单位：米）
        R = 6371  # 地球半径（单位：公里）
        dLat = math.radians(lat2 - lat1)
        dLon = math.radians(lon2 - lon1)
        a = math.sin(dLat / 2) * math.sin(dLat / 2) + math.cos(math.radians(lat1)) \
            * math.cos(math.radians(lat2)) * math.sin(dLon / 2) * math.sin(dLon / 2)
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
        distance = R * c * 1000  # 距离（单位：米）
        return distance

    def send_data_to_server(self, lat, lon):
        # 发送位置数据到后台服务器
        url = "http://yourserver.com/track"
        data = {'latitude': lat, 'longitude': lon}
        response = requests.post(url, data=data)
        # 更新显示信息
        self.label.text = f"Sent data: {response.text}"

    def on_start(self):
        # 启动定时任务，每3分钟检查一次位置
        threading.Timer(180, self.check_location_change).start()

    def on_stop(self):
        # 停止GPS
        gps.stop()

if __name__ == '__main__':
    LocationApp().run()
