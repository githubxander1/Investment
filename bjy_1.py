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
    raw_param = '{"action":"strongRecommendStockIndex","member_id":"0","app_version":187,"n":1,"sign_level":0,"data_time_ymd":"0"}'#强势股
    
    raw_param1= {"action":"getXyStockList","member_id":"0","app_version":187,"date":"20250811"} #xy推荐
                    
    raw_param2 = {"action":"searchLdListWithNetWorth","member_id":"0","app_version":187,"n":1,"mac_id":"0","search_date_type":"8,9,2,1","search_sign_type":"1","data_time_ymd":"20250814"} #生信号 sign_tipy:1为生，2为死
    
    raw_param3 = {"action":"MakeMoney","day":2,"zdf":5,"lsgl":90,"member_id":"0","app_version":187} #想赚钱， 选择天数，赚钱比例5， 成功概率90%        
    
    raw_param4 = {"action":"chanceDangerPoolWithNetWorth","member_id":"0","app_version":187,"n":1,"mac_id":"0","search_date_type":"all","search_sign_type":"1","data_time_ymd":"0"} #机会和风险（风险时"search_date_type":"M,M60,D,W","search_sign_type":"2"）  
     
    raw_param5 = {"action":"getFourCats","member_id":"0","app_version":187,"date":"20250814"}#四只小猫        
                                                 
    raw_param6 = {"action":"AIEstimateStock","member_id":"15066612","app_version":187,"SecurityID":"600506"} #  AI预测                                
    raw_param7 = {"action":"ViewStockSignal","member_id":"15066612","app_version":187,"SecurityID":"600506","position":"域加级别","signal":"1"} #返回：{"result":"0","data":{"cover":"0","view_sum":"3","surplus_num":2}}
                            
    raw_param8 = {"action":"remindPage","member_id":"15066612","app_version":187,"SecurityID":"600506"}  #提醒                
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