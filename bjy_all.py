from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import requests
import json  # 用于格式化保存结果

# ========================  加密解密配置与工具函数  ========================
AES_KEY = "romaway2015-bjcf"       # 需与服务端一致
AES_IV = "bjcf-romaway2015"        # CBC模式必需
AES_MODE = AES.MODE_CBC            
AES_BLOCK_SIZE = AES.block_size    # PKCS5Padding固定16字节


def aes_encrypt(plaintext: str) -> str:
    """AES/CBC/PKCS5Padding加密，返回Base64编码"""
    cipher = AES.new(AES_KEY.encode("utf-8"), AES_MODE, AES_IV.encode("utf-8"))
    padded_data = pad(plaintext.encode("utf-8"), AES_BLOCK_SIZE)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(ciphertext).decode("utf-8")


def aes_decrypt(ciphertext_base64: str) -> str:
    """解密Base64编码的AES密文，返回明文"""
    ciphertext = base64.b64decode(ciphertext_base64)
    cipher = AES.new(AES_KEY.encode("utf-8"), AES_MODE, AES_IV.encode("utf-8"))
    plaintext = unpad(cipher.decrypt(ciphertext), AES_BLOCK_SIZE)
    return plaintext.decode("utf-8")


# ========================  批量请求与结果保存  ========================
def send_all_encrypted_requests(save_file: str = "request_results.json"):
    """
    批量请求所有raw_param，解密结果并保存到JSON文件
    :param save_file: 结果保存路径
    """
    # 1. 整理所有待请求的原始参数（给每个参数加名称，方便区分结果）
    all_raw_params = [
        {"name": "强势股推荐", "param": '{"action":"strongRecommendStockIndex","member_id":"0","app_version":187,"n":1,"sign_level":0,"data_time_ymd":"0"}'},
        {"name": "xy推荐列表", "param": '{"action":"getXyStockList","member_id":"0","app_version":187,"date":"20250811"}'},
        {"name": "生信号列表", "param": '{"action":"searchLdListWithNetWorth","member_id":"0","app_version":187,"n":1,"mac_id":"0","search_date_type":"8,9,2,1","search_sign_type":"1","data_time_ymd":"20250814"}'},
        {"name": "想赚钱筛选", "param": '{"action":"MakeMoney","day":2,"zdf":5,"lsgl":90,"member_id":"0","app_version":187}'},
        {"name": "机会池（生信号）", "param": '{"action":"chanceDangerPoolWithNetWorth","member_id":"0","app_version":187,"n":1,"mac_id":"0","search_date_type":"all","search_sign_type":"1","data_time_ymd":"0"}'},
        {"name": "四只小猫数据", "param": '{"action":"getFourCats","member_id":"0","app_version":187,"date":"20250814"}'},
        {"name": "AI股票预测（600506）", "param": '{"action":"AIEstimateStock","member_id":"15066612","app_version":187,"SecurityID":"600506"}'},
        {"name": "股票信号查看（600506）", "param": '{"action":"ViewStockSignal","member_id":"15066612","app_version":187,"SecurityID":"600506","position":"域加级别","signal":"1"}'},
        {"name": "股票提醒（600506）", "param": '{"action":"remindPage","member_id":"15066612","app_version":187,"SecurityID":"600506"}'}
    ]

    # 2. 初始化结果存储列表
    all_results = []
    request_url = "https://www.baijiayungu.cn/bjcf/Interface6720"
    request_headers = {
        "content-type": "application/x-www-form-urlencoded; charset=utf-8",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.3.1"
    }

    # 3. 循环请求每个参数
    for idx, item in enumerate(all_raw_params, 1):
        param_name = item["name"]
        raw_param = item["param"]
        result = {"请求序号": idx, "请求名称": param_name, "原始参数": raw_param}

        try:
            # 加密参数 + 发送请求
            encrypted_param = aes_encrypt(raw_param)
            response = requests.post(
                url=request_url,
                headers=request_headers,
                data={"para": encrypted_param},
                timeout=15
            )
            response.raise_for_status()  # 非200状态码抛异常

            # 解密响应 + 记录结果
            encrypted_response = response.text
            decrypted_response = aes_decrypt(encrypted_response)
            result["请求状态"] = "成功"
            result["解密后响应"] = decrypted_response
            print(f"✅ 第{idx}个请求（{param_name}）成功")

        except Exception as e:
            # 捕获异常（网络错误、解密错误等）
            result["请求状态"] = "失败"
            result["错误信息"] = str(e)
            print(f"❌ 第{idx}个请求（{param_name}）失败：{str(e)}")

        finally:
            all_results.append(result)

    # 4. 保存所有结果到JSON文件（格式化排版，方便阅读）
    with open(save_file, "w", encoding="utf-8") as f:
        json.dump(all_results, f, ensure_ascii=False, indent=2)
    print(f"\n📁 所有请求结果已保存到：{save_file}")


# ========================  主程序入口  ========================
if __name__ == "__main__":
    send_all_encrypted_requests()  # 运行后会在当前目录生成 request_results.json