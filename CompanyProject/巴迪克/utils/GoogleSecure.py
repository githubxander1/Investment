#谷歌验证码生成器
import hmac
import base64
import os
import struct
import hashlib
import time
import re
import os
import base64


from CompanyProject.巴迪克.utils.sql_handler import SQLHandler


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
    def create_secret_key(length: int = 20) -> str:
        """
        生成指定长度的随机字节，并编码为 RFC 4648 兼容的 Base32 字符串（无填充字符）
        :param length: 原始字节数，默认 20 字节（对应 32 位 Base32 字符）
        :return: 小写的 Base32 编码字符串
        """
        raw_bytes = os.urandom(length)
        # Base32 编码并去除填充字符 '='，转换为小写
        return base64.b32encode(raw_bytes).decode("utf-8").strip("=").lower()


    @staticmethod
    def update_google_secret_key_in_db(environment: str, project: str, table: str,
                                      login_name: str):
        """
        生成 Google Secret Key 并加密写入数据库
        :param environment: 环境标识（test/prod）
        :param project: 项目名（tax）
        :param table: 数据表（agent_operator）
        :param login_name: 登录邮箱（如 tax_agent009@linshiyou.com）
        """
        try:
            # 1. 生成 Base32 Secret Key
            secret_key = CalGoogleCode.create_secret_key()

            # 3. 写入数据库
            with SQLHandler(yaml_path, environment, project) as handler:
                sql = f"UPDATE {handler.get_table(table)} SET google_secret_key = %s WHERE login_name = %s"
                handler.execute(sql, (secret_key, login_name))
                print(f"[INFO] 已成功生成并更新加密的谷歌密钥 for {login_name}")

            return secret_key

        except Exception as e:
            print(f"[ERROR] 更新谷歌密钥失败: {str(e)}")
            raise


    def main(self):
        environment = "test"
        project = "tax"
        table = "agent_operator"
        login_name = "tax_agent0010@linshiyou.com"
        # aes_key = self.create_secret_key()

        original_secret = CalGoogleCode.update_google_secret_key_in_db(
            environment=environment,
            project=project,
            table=table,
            login_name=login_name,
            # aes_key=aes_key
        )
        print(f"生成的原始谷歌密钥: {original_secret}")

if __name__ == "__main__":
    calGoogleCode = CalGoogleCode()
    calGoogleCode.main()
    # raw_key = CalGoogleCode.generate_secure_google_key()  # 得到 16 字节原始密钥
    # print(f"原始密钥: {raw_key.hex()}")
    # secret_key = base64.b32encode(raw_key).decode().rstrip("=")  # 用于谷歌验证码
    # print(f"Base32 编码的密钥: {secret_key}")
    # encrypted_secret = CalGoogleCode.aes_encrypt(secret_key, raw_key.hex())  # raw_key.hex() 可作为 32 字符(16字节) AES 密钥
    # print(f"AES 加密后的密钥: {encrypted_secret}")
    # 'aty2zhr4aognqm4xcvaja4jqdxtaotoz'
    # '5upc2xtpmxwnzvzl6tzy2zsf6vb3qz7m'