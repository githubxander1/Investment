# GoogleSecure1.py
# import hmac
# import base64
# import struct
# import hashlib
# import time
# import re
# from pyzbar.pyzbar import decode
# from PIL import Image
#
# from CompanyProject.巴迪克.utils.sql_handler import SQLHandler
# from CompanyProject.巴迪克.utils.yaml_handler import get_db_config
#
# class CalGoogleCode():
#     """计算谷歌验证码（16位谷歌秘钥，生成6位验证码）"""
#     @staticmethod
#     def cal_google_code(secret, current_time=int(time.time()) // 30):
#         """
#         :param secret:   16位谷歌秘钥
#         :param current_time:   时间（谷歌验证码是30s更新一次）
#         :return:  返回6位谷歌验证码
#         """
#         # 清理 secret_key
#         cleaned_secret = CalGoogleCode.clean_secret_key(secret)
#
#         # 验证 secret_key 是否为有效的 Base32 编码
#         if not CalGoogleCode.is_valid_base32(cleaned_secret):
#             raise ValueError("secret_key 不是有效的 Base32 编码")
#
#         key = base64.b32decode(cleaned_secret)
#         msg = struct.pack(">Q", current_time)
#         google_code = hmac.new(key, msg, hashlib.sha1).digest()
#         o = google_code[19] & 15  # python3时，直接使用字节索引
#         google_code = (struct.unpack(">I", google_code[o:o + 4])[0] & 0x7fffffff) % 1000000
#         return '%06d' % google_code  # 不足6位时，在前面补0
#
#     @staticmethod
#     def is_valid_base32(s):
#         """检查字符串是否为有效的 Base32 编码"""
#         return re.fullmatch('[A-Z2-7]+=*', s) is not None
#
#     @staticmethod
#     def clean_secret_key(secret_key):
#         """清理 secret_key，去除无效字符"""
#         return re.sub(r'[^A-Z2-7=]', '', secret_key.upper())


if __name__ == '__main__':
    secret_key = "tvxnmn522rd7gmag34m22iwvnvgerled"
    # secret_key = "q3woflszthh4wd5ek7euedblcppp2c53"
    sales_login_name='15318544153'
    print(CalGoogleCode().generate_google_code('logic', 'sales_operator', sales_login_name))

    # 示例：从二维码生成谷歌验证码
    # image_path = '财务密码谷歌验证码.png'
    # print(CalGoogleCode().generate_google_code_from_qr(image_path))
