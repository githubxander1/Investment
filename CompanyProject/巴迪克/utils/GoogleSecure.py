# GoogleSecure.py (精简优化版)

import hmac
import base64
import os
import re
import struct
import hashlib
import time
from typing import Optional

from CompanyProject.巴迪克.utils.sql_handler import SQLHandler

# 动态获取配置文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
yaml_path = os.path.join(current_dir, "../common/sql_config.yaml")


class GoogleAuth:
    """
    谷歌验证码工具类：密钥管理 + 验证码生成 + 数据库操作
    """
    @staticmethod
    def _get_secret_key(environment: str, project: str, table: str, login_name: str) -> Optional[str]:
        """从数据库获取谷歌密钥"""
        try:
            with SQLHandler(yaml_path, environment, project) as handler:
                sql = f"SELECT google_secret_key FROM {handler.get_table(table)} WHERE login_name = %s"
                result = handler.query_one(sql, (login_name,))
                print(f"[INFO] 获取密钥成功: {result[0]}")
                return result[0] if result else None
        except Exception as e:
            print(f"[ERROR] 数据库查询失败: {str(e)}")
            return None

    # @staticmethod
    # def generate(environment: str, project: str, table: str, login_name: str) -> Optional[str]:
    #     """
    #     生成谷歌验证码主流程
    #     :param environment: 环境标识（test/prod）
    #     :param project: 项目名称（tax/payok等）
    #     :param table: 表键名
    #     :param login_name: 登录用户名
    #     :return: 6位验证码或None
    #     """
    #     try:
    #         # 获取密钥
    #         secret_key = GoogleAuth._get_secret_key(
    #             environment, project, table, login_name
    #         )
    #
    #         if not secret_key:
    #             print(f"[ERROR] 未找到用户 {login_name} 的密钥记录")
    #             return None
    #
    #         # 生成验证码
    #         return GoogleAuth._calculate_code(secret_key)
    #
    #     except Exception as e:
    #         print(f"[ERROR] 验证码生成失败: {str(e)}")
    #         return None


    # @staticmethod
    # def _calculate_code(secret: str) -> str:
    #     """核心计算逻辑"""
    #     # 清理并验证密钥（允许字母大小写）
    #     cleaned_secret = re.sub(r'[^A-Za-z2-7=]', '', secret.upper())  # 修改点1
    #     if not re.fullmatch(r'[A-Z2-7]+=*', cleaned_secret):
    #         raise ValueError("无效的Base32密钥格式")
    #
    #     # 120秒窗口有效时间
    #     time_window = int(time.time()) // 30
    #
    #     # HMAC-SHA1计算
    #     key = base64.b32decode(cleaned_secret)
    #     msg = struct.pack(">Q", time_window)
    #     hmac_hash = hmac.new(key, msg, hashlib.sha1).digest()  # 修改点3
    #
    #     # 动态截取验证码（完全一致）
    #     offset = hmac_hash[19] & 0x0F
    #     code_segment = hmac_hash[offset:offset + 4]
    #     code = struct.unpack(">I", code_segment)[0] & 0x7FFFFFFF
    #
    #     return f"{code % 1000000:06d}"
    @staticmethod
    def _calculate(secret: str, current_time: int = int(time.time()) // 30) -> str:
        """计算并返回6位验证码"""
        missing_padding = len(secret) % 8
        if missing_padding:
            secret += '=' * (8 - missing_padding)

        cleaned = re.sub(r'[^A-Z2-7=]', '', secret.upper())
        if not re.fullmatch(r'[A-Z2-7]+=*', cleaned):
            raise ValueError("无效的 Base32 密钥格式")

        key = base64.b32decode(cleaned, casefold=True)
        msg = struct.pack(">Q", current_time)
        digest = hmac.new(key, msg, hashlib.sha1).digest()
        offset = digest[19] & 0x0F
        code = (struct.unpack(">I", digest[offset:offset+4])[0] & 0x7FFFFFFF) % 1000000
        print(f"谷歌验证码: {code:06d}")
        return f"{code:06d}"

    @staticmethod
    def generate(environment: str, project: str, table: str, login_name: str) -> Optional[str]:
        """主流程：根据用户信息生成谷歌验证码"""
        try:
            with SQLHandler(yaml_path, environment, project) as handler:
                sql = f"SELECT google_secret_key FROM {handler.get_table(table)} WHERE login_name = %s"
                result = handler.query_one(sql, (login_name,))
                print(f"{login_name} 的谷歌密钥: {result}")
                if not result:
                    print(f"[ERROR] 用户 {login_name} 没有设置谷歌密钥")
                    return None
                secret = result[0]
                return GoogleAuth._calculate(secret)
        except Exception as e:
            print(f"[ERROR] 生成验证码失败: {str(e)}")
            return None

    @staticmethod
    def create_secret_key(length: int = 20) -> str:
        """生成 RFC 4648 兼容的 Base32 编码密钥（无填充字符）"""
        return base64.b32encode(os.urandom(length)).decode().rstrip("=").lower()

    @staticmethod
    def update_secret_key_to_db(environment: str, project: str, table: str, login_name: str) -> str:
        """生成新密钥并更新数据库"""
        secret = GoogleAuth.create_secret_key()
        try:
            with SQLHandler(yaml_path, environment, project) as handler:
                sql = f"UPDATE {handler.get_table(table)} SET google_secret_key = %s WHERE login_name = %s"
                handler.execute(sql, (secret, login_name))
                print(f"[INFO] 已更新谷歌密钥 for {login_name}")
            return secret
        except Exception as e:
            print(f"[ERROR] 更新谷歌密钥失败: {str(e)}")
            raise

    @staticmethod
    def test():
        # 示例调用
        # code = GoogleAuth.generate(
        #     environment='test',
        #     project='tax',
        #     table='agent_operator',
        #     # login_name='tax_operator@test.com'
        #     login_name='tax_agent001@linshiyou.com'
        # )
        # if code:
        #     print(f"生成的验证码: {code}（有效期剩余 {30 - int(time.time()) % 30}s）")
        # else:
        #     print("验证码生成失败")
#
        # 测试一致性
        secret = "as3ofdbf7w5eatieq2hydfd6ptgtgbgr"
        secret2 = "igz4obkiqirr16pudug7qkfbjj544yy2"
        code1 = GoogleAuth._calculate(secret)
        print(f"旧算法: {code1}")
        # code2 = GoogleAuth._calculate(secret2)
        # print(f"算法一致性测试: {code1} == {code2} => {'✅' if code2 == code2 else '❌'}")
#
#
if __name__ == "__main__":
    GoogleAuth.test()
