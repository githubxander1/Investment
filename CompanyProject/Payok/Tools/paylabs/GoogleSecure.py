#谷歌验证码生成器
import hmac
import base64
import struct
import hashlib
import time
import re

from CompanyProject.Payok.交付.paylabs.sql_handler import SQLHandler


class CalGoogleCode:
    @staticmethod
    def cal_google_code(secret, current_time=int(time.time()) // 30):
        cleaned_secret = CalGoogleCode.clean_secret_key(secret)

        if not CalGoogleCode.is_valid_base32(cleaned_secret):
            raise ValueError("secret_key 不是有效的 Base32 编码")

        key = base64.b32decode(cleaned_secret)
        msg = struct.pack(">Q", current_time)
        google_code = hmac.new(key, msg, hashlib.sha1).digest()
        o = google_code[19] & 15
        google_code = (struct.unpack(">I", google_code[o:o + 4])[0] & 0x7fffffff) % 1000000
        return '%06d' % google_code

    @staticmethod
    def is_valid_base32(s):
        return re.fullmatch('[A-Z2-7]+=*', s) is not None

    @staticmethod
    def clean_secret_key(secret_key):
        return re.sub(r'[^A-Z2-7=]', '', secret_key.upper())

    @staticmethod
    def generate_google_code(host, port, user, password, database, table_name, login_name):
        db_handler = SQLHandler(host, port, user, password, database)
        db_handler.connect()

        secret_key = db_handler.get_google_secret_key(table_name, login_name)
        if not secret_key:
            print("未发现给定邮箱的记录")
            return None

        db_handler.disconnect()
        try:
            current_time = int(time.time()) // 30
            generated_code = CalGoogleCode.cal_google_code(secret_key, current_time)
            return generated_code
        except ValueError as e:
            print("错误:", e)
            return None
