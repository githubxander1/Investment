# generate_google_code.py
import os
import time
import re
import hmac
import base64
import struct
import hashlib
from typing import Optional

from CompanyProject.巴迪克.others.Tools.paylabs.GoogleSecure import CalGoogleCode
from CompanyProject.巴迪克.utils.sql_handler import SQLHandler

# 动态获取配置文件路径
current_dir = os.path.dirname(os.path.abspath(__file__))
yaml_path = os.path.normpath(os.path.join(current_dir, "../common/sql_config.yaml"))

class GoogleAuthenticator:
    """谷歌验证码生成器"""

    @staticmethod
    def generate(environment: str, project: str, table: str, login_name: str) -> Optional[str]:
        """
        生成谷歌验证码主流程
        :param environment: 环境标识（test/prod）
        :param project: 项目名称（tax/payok等）
        :param table: 表键名
        :param login_name: 登录用户名
        :return: 6位验证码或None
        """
        try:
            # 获取密钥
            secret_key = GoogleAuthenticator._get_secret_key(
                environment, project, table, login_name
            )

            if not secret_key:
                print(f"[ERROR] 未找到用户 {login_name} 的密钥记录")
                return None

            # 生成验证码
            return GoogleAuthenticator._calculate_code(secret_key)

        except Exception as e:
            print(f"[ERROR] 验证码生成失败: {str(e)}")
            return None

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

    @staticmethod
    def _calculate_code(secret: str) -> str:
        """核心计算逻辑（与GoogleSecure1一致）"""
        # 清理并验证密钥（允许字母大小写）
        cleaned_secret = re.sub(r'[^A-Za-z2-7=]', '', secret.upper())  # 修改点1
        if not re.fullmatch(r'[A-Z2-7]+=*', cleaned_secret):
            raise ValueError("无效的Base32密钥格式")

        # 120秒窗口有效时间
        time_window = int(time.time()) // 30

        # HMAC-SHA1计算
        key = base64.b32decode(cleaned_secret)
        msg = struct.pack(">Q", time_window)
        hmac_hash = hmac.new(key, msg, hashlib.sha1).digest()  # 修改点3

        # 动态截取验证码（完全一致）
        offset = hmac_hash[19] & 0x0F
        code_segment = hmac_hash[offset:offset+4]
        code = struct.unpack(">I", code_segment)[0] & 0x7FFFFFFF

        return f"{code % 1000000:06d}"

if __name__ == "__main__":
    # 使用示例
    code = GoogleAuthenticator.generate(
        environment='test',
        project='tax',
        table='tax_operator',
        login_name='tax001@test.com'
    )

    if code:
        remaining = 120 - int(time.time()) % 30  # <<< 修改这里
        print(f"生成的谷歌验证码: {code}（有效期剩余{remaining}秒）")
    else:
        print("验证码生成失败")


    # 测试用例
    def get_code():
        secret = "x4aaz7setzhuvnzehk7ueqw2tvn2aaj7"

        # 新旧算法对比
        old_code = CalGoogleCode.cal_google_code(secret)  # GoogleSecure1的方法
        new_code = GoogleAuthenticator._calculate_code(secret)

        print(f"旧算法: {old_code}")
        print(f"新算法: {new_code}")
        assert old_code == new_code, "验证码不一致"

    get_code()

    # if __name__ == "__main__":
    #     test_code()
