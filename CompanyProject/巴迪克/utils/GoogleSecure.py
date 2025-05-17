#谷歌验证码生成器
import hmac
import base64
import os
import struct
import hashlib
import time
import re

from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad

# from numpy import pad

from CompanyProject.巴迪克.utils.sql_handler import SQLHandler


# from CompanyProject.巴迪克.Tools.paylabs.sql_handler import SQLHandler


# 动态获取配置文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
yaml_path = os.path.normpath(os.path.join(current_dir, "../common/sql_config.yaml"))

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
    # def generate_google_code(host, port, user, password, database, table_name, login_name):
    #     db_handler = SQLHandler(host, port, user, password, database)
    #     db_handler.connect()
    #
    #     secret_key = db_handler.get_google_secret_key(table_name, login_name)
    #     if not secret_key:
    #         print("未发现给定邮箱的记录")
    #         return None
    #
    #     db_handler.disconnect()
    #     try:
    #         current_time = int(time.time()) // 30
    #         generated_code = CalGoogleCode.cal_google_code(secret_key, current_time)
    #         return generated_code
    #     except ValueError as e:
    #         print("错误:", e)
    #         return None
    def generate_google_code(environment: str, project: str, table: str, login_name: str):
        """从数据库获取谷歌密钥"""
        try:
            with SQLHandler(yaml_path, environment, project) as handler:
                sql = f"SELECT google_secret_key FROM {handler.get_table(table)} WHERE login_name = %s"
                result = handler.query_one(sql, (login_name,))
                return result[0] if result else None
        except Exception as e:
            print(f"[ERROR] 数据库查询失败: {str(e)}")
            return None

    @staticmethod
    def generate_secure_google_key(length=16) -> str:
        """
        生成符合 Google Authenticator 标准的 Secret Key（Base32 编码）
        :param length: 密钥原始字节长度，默认 16 字节（对应 26 位 Base32 字符）
        :return: Base32 编码字符串（无填充字符）
        """
        raw_key = get_random_bytes(length)
        # Base32 编码并去除填充字符
        secret = base64.b32encode(raw_key).decode().rstrip("=")
        return secret

    @staticmethod
    def aes_encrypt(plain_text: str, aes_key: str) -> str:
        """
        使用 AES ECB 模式加密 Google Secret Key
        :param plain_text: 明文 secret key
        :param aes_key: 16 位密钥
        :return: Base64 编码的密文
        """
        key = aes_key.encode('utf-8')
        cipher = AES.new(key, AES.MODE_ECB)

        # 填充 + 加密 + Base64 输出
        padded_data = pad(plain_text.encode(), AES.block_size)
        encrypted_data = cipher.encrypt(padded_data)
        return base64.b64encode(encrypted_data).decode()

    @staticmethod
    def update_google_secret_key_in_db(environment: str, project: str, table: str,
                                      login_name: str, aes_key: str):
        """
        生成 Google Secret Key 并加密写入数据库
        :param environment: 环境标识（test/prod）
        :param project: 项目名（tax）
        :param table: 数据表（agent_operator）
        :param login_name: 登录邮箱（如 tax_agent009@linshiyou.com）
        :param aes_key: AES 加密密钥（必须为16位）
        """
        try:
            # 1. 生成 Base32 Secret Key
            secret_key = CalGoogleCode.generate_secure_google_key()

            # 2. 使用 AES 加密
            encrypted_secret = CalGoogleCode.aes_encrypt(secret_key, aes_key)

            # 3. 写入数据库
            with SQLHandler(yaml_path, environment, project) as handler:
                sql = f"UPDATE {handler.get_table(table)} SET google_secret_key = %s WHERE login_name = %s"
                handler.execute(sql, (encrypted_secret, login_name))
                print(f"[INFO] 已成功生成并更新加密的谷歌密钥 for {login_name}")

            return secret_key  # 返回原始密钥，用于调试或展示给用户

        except Exception as e:
            print(f"[ERROR] 更新谷歌密钥失败: {str(e)}")
            raise

# import asyncio
# from CompanyProject.巴迪克.utils.GoogleSecure import CalGoogleCode

    def main(self):
        environment = "test"
        project = "tax"
        table = "agent_operator"
        login_name = "tax_agent009@linshiyou.com"
        aes_key = "your_16_byte_key_here"  # ← 必须是 16 字节长度

        original_secret = CalGoogleCode.update_google_secret_key_in_db(
            environment=environment,
            project=project,
            table=table,
            login_name=login_name,
            aes_key=aes_key
        )
        print(f"生成的原始谷歌密钥: {original_secret}")

if __name__ == "__main__":
    calGoogle
    main()