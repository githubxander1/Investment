import json
import time

import requests
from apscheduler.schedulers.background import BackgroundScheduler
from plyer import gps


class LocationTracker:
    def __init__(self):
        self.last_location = None
        self.device_id = self.get_device_id()
        self.base_url = "https://your-domain.com/api"
        self.min_distance = 100  # 触发上报距离（米）
        self.interval = 180  # 采集间隔（秒）

    @staticmethod
    def get_device_id():
        """获取设备唯一ID"""
        try:
            with open("/data/data/com.termux/files/home/.device_id", "r") as f:
                return f.read().strip()
        except FileNotFoundError:
            import uuid
            device_id = str(uuid.uuid4())
            with open("/data/data/com.termux/files/home/.device_id", "w") as f:
                f.write(device_id)
            return device_id

    def on_location(self, **kwargs):
        """位置回调处理"""
        lat = kwargs.get('lat')
        lon = kwargs.get('lon')
        if not lat or not lon:
            return

        current = (lat, lon)
        if self.last_location:
            distance = self.calculate_distance(self.last_location, current)
            if distance < self.min_distance:
                return

        self.send_to_server(lat, lon)
        self.last_location = current

    @staticmethod
    def calculate_distance(coord1, coord2):
        """使用Haversine公式计算距离"""
        from math import radians, sin, cos, sqrt, atan2
        lat1, lon1 = map(radians, coord1)
        lat2, lon2 = map(radians, coord2)

        dlat = lat2 - lat1
        dlon = lon2 - lon1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
        return 6371000 * 2 * atan2(sqrt(a), sqrt(1 - a))  # 返回米

    def send_to_server(self, lat, lon):
        """发送位置到服务端"""
        data = {
            "device_id": self.device_id,
            "lat": lat,
            "lng": lon,
            "timestamp": int(time.time())
        }
        try:
            resp = requests.post(
                f"{self.base_url}/location",
                json=data,
                timeout=10
            )
            print(f"数据提交状态：{resp.status_code}")
        except Exception as e:
            print(f"提交失败：{str(e)}")

    def start(self):
        """启动追踪服务"""
        gps.configure(on_location=self.on_location)
        gps.start(minTime=1000, minDistance=0)  # 最低1秒更新

        scheduler = BackgroundScheduler()
        scheduler.add_job(
            gps.start,
            'interval',
            seconds=self.interval,
            args=[1000, 0]
        )
        scheduler.start()

        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            gps.stop()
            scheduler.shutdown()


# 在客户端添加
from cryptography.fernet import Fernet


class SecureClient:
    def __init__(self):
        self.key = Fernet.generate_key()
        self.cipher = Fernet(self.key)

    def encrypt_data(self, data):
        return self.cipher.encrypt(
            json.dumps(data).encode()
        ).decode()

if __name__ == "__main__":
    tracker = LocationTracker()
    print(f"设备ID: {tracker.device_id}")
    tracker.start()