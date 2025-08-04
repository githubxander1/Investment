import requests
import json

def delete_stock_warnings():
    """批量删除股票预警（POST请求）"""
    # 请求URL
    url = "https://vaserviece.10jqka.com.cn/iwcalarm/nlp/v1/batch_delete_warninfo"
    
    # 请求头
    headers = {
        "Host": "vaserviece.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.30.02 (Royal Flush) hxtheme/0 innerversion/G037.09.033.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://vaserviece.10jqka.com.cn",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://vaserviece.10jqka.com.cn/alarm/htmlV2/index.html",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "user_status=0; _clck=138ocji%7C2%7Cfxq%7C0%7C0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzUyOTA5NzgwOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTc3NzJmZTMyYTdjNjE5YjkwMGFjMzJkNmEyOGMxZjg2Ojox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=62bed98b41145d0eb19010429bab39b7; IFUserCookieKey={\"userid\":\"641926488\",\"escapename\":\"mo_641926488\",\"custid\":\"\"}; hxmPid=free_yujing_alllist; v=A81Vd8OxmSEkxT0NkjqmZDel3uJHqgF3i91lUA9SCDHR6OIY1_oRTBsudTGc"
    }
    
    # 请求体（表单数据，包含待删除的预警ID）
    payload = {
        "userId": "641926488",  # 用户ID
        "warnIds": "219556273,219556274",  # 待删除的预警ID列表（已解码）
        "channel": "THS_MOBILE"  # 渠道标识
    }
    
    try:
        # 发送POST请求
        response = requests.post(
            url,
            headers=headers,
            data=payload,
            verify=True
        )
        response.raise_for_status()  # 检查响应状态码
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"删除预警失败: {e}")
        return None

# 测试函数
if __name__ == "__main__":
    delete_result = delete_stock_warnings()
    if delete_result:
        print("删除预警结果:")
        print(json.dumps(delete_result, indent=2, ensure_ascii=False))  # 格式化显示响应