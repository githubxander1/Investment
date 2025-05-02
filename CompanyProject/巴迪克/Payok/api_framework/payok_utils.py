import hashlib
import hmac
import base64
from Crypto.PublicKey import RSA
from Crypto.Signature import pkcs1_15
from Crypto.Hash import SHA256

from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization


def generate_rsa_keys(key_size=2048):
    """
    生成 RSA 公私钥对
    :param key_size: 密钥长度，默认为 2048 位
    :return: 私钥对象和公钥对象
    """
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=key_size,
        backend=default_backend()
    )
    public_key = private_key.public_key()
    return private_key, public_key


def save_private_key(private_key, filename):
    """
    将私钥保存到文件
    :param private_key: 私钥对象
    :param filename: 保存私钥的文件名
    """
    pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open(filename, 'wb') as f:
        f.write(pem)


def save_public_key(public_key, filename):
    """
    将公钥保存到文件
    :param public_key: 公钥对象
    :param filename: 保存公钥的文件名
    """
    pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open(filename, 'wb') as f:
        f.write(pem)



def generate_signature(private_key_path, data, api_url):
    """
    使用私钥生成签名。
    :param private_key_path: 私钥文件路径
    :param data: 待签名的数据（字典或其他可序列化对象）
    :param api_url: API URL
    :return: Base64 编码的签名字符串
    """
    with open(private_key_path, 'rb') as key_file:
        private_key = RSA.import_key(key_file.read())

    # 将数据转换为字符串并拼接 URL
    data_str = str(data).replace("'", "\"")
    message = data_str + '&' + api_url

    # 计算哈希值并签名
    hash_obj = SHA256.new(message.encode('utf-8'))
    signer = pkcs1_15.new(private_key)
    signature = signer.sign(hash_obj)

    return base64.b64encode(signature).decode('utf-8')


def verify_signature(public_key_path, signature, data):
    """
    使用公钥验证签名。
    :param public_key_path: 公钥文件路径
    :param signature: Base64 编码的签名字符串
    :param data: 原始数据（字典或其他可序列化对象）
    :return: 验签结果（布尔值）
    """
    with open(public_key_path, 'rb') as key_file:
        public_key = RSA.import_key(key_file.read())

    # 将数据转换为字符串
    data_str = str(data).replace("'", "\"")
    hash_obj = SHA256.new(data_str.encode('utf-8'))

    try:
        # 验证签名
        pkcs1_15.new(public_key).verify(hash_obj, base64.b64decode(signature))
        return True
    except (ValueError, TypeError):
        return False

import datetime

def get_current_utc_time():
    # 获取当前的 UTC 时间
    # current_utc_time = datetime.datetime.utcnow()
    current_utc_time = datetime.datetime.now(datetime.UTC)
    # 将时间格式化为指定的字符串格式
    formatted_time = current_utc_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")[:-3]
    return formatted_time

# # 测试函数
# request_time = get_current_utc_time()
# print(request_time)
if __name__ == "__main__":
    private_key, public_key = generate_rsa_keys()
    save_private_key(private_key, 'private_key.pem')
    save_public_key(public_key, 'public_key.pem')
    print("私钥和公钥已生成并保存到文件中。")