# GoogleSecure1.py
import hmac
import base64
import struct
import hashlib
import time
import re

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

if __name__ == '__main__':
    # secret_key = "tvxnmn522rd7gmag34m22iwvnvgerled"
    # secret_key = "q3woflszthh4wd5ek7euedblcppp2c53"
    sales_login_name='15318544153'
    print(CalGoogleCode().generate_google_code('paylabs', 'sales_operator', sales_login_name))
