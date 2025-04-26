# GoogleSecure1.py
import hmac
import base64
import struct
import hashlib
import time
import re
from pyzbar.pyzbar import decode
from PIL import Image

from CompanyProject.Payok.UI.utils.sql_handler import SQLHandler
from CompanyProject.Payok.UI.utils.yaml_handler import get_db_config

class CalGoogleCode():
    """计算谷歌验证码（16位谷歌秘钥，生成6位验证码）"""

    @staticmethod
    def cal_google_code(secret, current_time=int(time.time()) // 30):
        """
        :param secret:   16位谷歌秘钥
        :param current_time:   时间（谷歌验证码是30s更新一次）
        :return:  返回6位谷歌验证码
        """
        # 清理 secret_key
        cleaned_secret = CalGoogleCode.clean_secret_key(secret)

        # 验证 secret_key 是否为有效的 Base32 编码
        if not CalGoogleCode.is_valid_base32(cleaned_secret):
            raise ValueError("secret_key 不是有效的 Base32 编码")

        key = base64.b32decode(cleaned_secret)
        msg = struct.pack(">Q", current_time)
        google_code = hmac.new(key, msg, hashlib.sha1).digest()
        o = google_code[19] & 15  # python3时，直接使用字节索引
        google_code = (struct.unpack(">I", google_code[o:o + 4])[0] & 0x7fffffff) % 1000000
        return '%06d' % google_code  # 不足6位时，在前面补0

    @staticmethod
    def is_valid_base32(s):
        """检查字符串是否为有效的 Base32 编码"""
        return re.fullmatch('[A-Z2-7]+=*', s) is not None

    @staticmethod
    def clean_secret_key(secret_key):
        """清理 secret_key，去除无效字符"""
        return re.sub(r'[^A-Z2-7=]', '', secret_key.upper())

    def generate_google_code(self, db_name, user_type, login_name):
        yaml_file = 'sql.yaml'
        db_config = get_db_config(yaml_file, db_name, user_type)

        if not db_config:
            print(f"未找到数据库配置：{db_name}, {user_type}")
            return None

        host = db_config.get('host')
        port = db_config.get('port')
        user = db_config.get('user')
        password = db_config.get('password')
        db_name = db_config.get('db_name')
        table_name = db_config.get('table_name')

        db_handler = SQLHandler(host, port, user, password, db_name)
        db_handler.connect()

        secret_key = db_handler.get_google_secret_key(table_name, login_name)
        db_handler.disconnect()

        if not secret_key:
            print("未发现给定登录名的记录")
            return None

        try:
            current_time = int(time.time()) // 30
            generated_code = CalGoogleCode.cal_google_code(secret_key, current_time)
            return generated_code
        except ValueError as e:
            print(f"错误: {e}")
            return None

    @staticmethod
    def scan_qr_code(image_path):
        """
        扫描二维码并提取其中的文本
        :param image_path: 二维码图像路径
        :return: 提取的文本
        """
        try:
            image = Image.open(image_path)
            decoded_objects = decode(image)
            for obj in decoded_objects:
                return obj.data.decode('utf-8')
        except Exception as e:
            print(f"扫描二维码时出错: {e}")
            return None

    @staticmethod
    def extract_secret_from_qr_code(qr_data):
        """
        从二维码数据中提取谷歌验证码的密钥
        :param qr_data: 二维码数据
        :return: 提取的密钥
        """
        if qr_data:
            # 通常二维码数据格式为: otpauth://totp/Example:alice@google.com?secret=JBSWY3DPEHPK3PXP&issuer=Example
            import re
            match = re.search(r'secret=([A-Z2-7=]+)', qr_data)
            print(match)
            if match:
                return match.group(1)
        return None

    def generate_google_code_from_qr(self, image_path):
        """
        从二维码生成谷歌验证码
        :param image_path: 二维码图像路径
        :return: 生成的谷歌验证码
        """
        qr_data = CalGoogleCode.scan_qr_code(image_path)
        if not qr_data:
            print("未从二维码中提取到数据")
            return None

        secret_key = CalGoogleCode.extract_secret_from_qr_code(qr_data)
        if not secret_key:
            print("未从二维码数据中提取到密钥")
            return None

        try:
            current_time = int(time.time()) // 30
            generated_code = CalGoogleCode.cal_google_code(secret_key, current_time)
            print(f"Generated Code: {generated_code}")
            return generated_code
        except ValueError as e:
            print(f"错误: {e}")
            return None

if __name__ == '__main__':
    # secret_key = "tvxnmn522rd7gmag34m22iwvnvgerled"
    # secret_key = "q3woflszthh4wd5ek7euedblcppp2c53"
    # sales_login_name='15318544153'
    # print(CalGoogleCode().generate_google_code('paylabs', 'sales_operator', sales_login_name))

    # 示例：从二维码生成谷歌验证码
    image_path = '财务密码谷歌验证码.png'
    print(CalGoogleCode().generate_google_code_from_qr(image_path))
