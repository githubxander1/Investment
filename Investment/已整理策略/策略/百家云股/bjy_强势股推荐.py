from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import requests

# ========================  加密解密配置与工具函数  ========================
# AES 算法相关配置（需与服务端保持一致）
AES_KEY = "romaway2015-bjcf"       # 加密密钥
AES_IV = "bjcf-romaway2015"        # 初始向量（CBC 模式需要）
AES_MODE = AES.MODE_CBC            # 加密模式
AES_BLOCK_SIZE = AES.block_size    # PKCS5Padding 填充的块大小（固定 16 字节）


def aes_encrypt(plaintext: str) -> str:
    """
    AES/CBC/PKCS5Padding 加密函数
    :param plaintext: 待加密的明文（字符串）
    :return: 加密后经 Base64 编码的字符串
    """
    cipher = AES.new(AES_KEY.encode("utf-8"), AES_MODE, AES_IV.encode("utf-8"))
    padded_data = pad(plaintext.encode("utf-8"), AES_BLOCK_SIZE)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(ciphertext).decode("utf-8")


def aes_decrypt(ciphertext_base64: str) -> str:
    """
    AES/CBC/PKCS5Padding 解密函数
    :param ciphertext_base64: 经 Base64 编码的密文字符串
    :return: 解密后的明文字符串
    """
    ciphertext = base64.b64decode(ciphertext_base64)
    cipher = AES.new(AES_KEY.encode("utf-8"), AES_MODE, AES_IV.encode("utf-8"))
    plaintext = unpad(cipher.decrypt(ciphertext), AES_BLOCK_SIZE)
    return plaintext.decode("utf-8")


# ========================  HTTP 请求函数  ========================
def send_encrypted_request():
    """
    发送加密 POST 请求并处理响应解密的完整流程
    1. 构造原始请求参数 → 2. AES 加密参数 → 3. 发送 POST 请求 → 4. 解密响应内容
    """
    # 1. 构造原始请求参数（与加密内容文本一致）
    raw_param = '{"action":"strongRecommendStockIndex","member_id":"0","app_version":187,"n":1,"sign_level":0,"data_time_ymd":"0"}'
    
    # 2. AES 加密请求参数
    encrypted_param = aes_encrypt(raw_param)
    
    # 3. 构造 HTTP 请求
    url = "https://www.baijiayungu.cn/bjcf/Interface6720"
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=utf-8",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.3.1"
    }
    data = {
        "para": encrypted_param  # 参数名需与服务端接口约定一致
    }

    try:
        # 发送 POST 请求
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()  # 检查 HTTP 状态码（非 200 会抛异常）

        # 4. 解密响应内容（假设响应体是 Base64 编码的 AES 密文）
        encrypted_response = response.text
        decrypted_response = aes_decrypt(encrypted_response)
        
        print("=== 解密后的响应内容 ===")
        print(decrypted_response)

    except requests.RequestException as e:
        print(f"请求失败：{str(e)}")


# ========================  主程序入口  ========================
if __name__ == "__main__":
    send_encrypted_request()