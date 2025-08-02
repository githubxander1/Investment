import requests
import json

def add_stock_warning():
    """获取股票预警信息（POST请求，对应添加预警场景）"""
    # 请求URL
    url = "https://vaserviece.10jqka.com.cn/alarm_v2/open/api/mobile/v2/page_query_warn_info"
    
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
        "Referer": "https://vaserviece.10jqka.com.cn/alarm/htmlV2/index.html?stockCode=600295&stockName=%E9%84%82%E5%B0%94%E5%A4%9A%E6%96%AF&marketID=17",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "user_status=0; _clck=138ocji%7C2%7Cfxq%7C0%7C0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzUyOTA5NzgwOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTc3NzJmZTMyYTdjNjE5YjkwMGFjMzJkNmEyOGMxZjg2Ojox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=62bed98b41145d0eb19010429bab39b7; IFUserCookieKey={\"userid\":\"641926488\",\"escapename\":\"mo_641926488\",\"custid\":\"\"}; hxmPid=free_yujing_gegulist; v=A85W-rRUKrQ-hp6QwhO1scjYHa-QT5IopBZGLfgXOwqOsWEVYN_iWXSjljXL"
    }
    
    # 请求体（表单数据）
    payload = {
        "marketcodes": "17",  # 市场代码
        "stkcodes": "600295",  # 股票代码
        "pageIndex": "1",      # 页码
        "userId": "641926488", # 用户ID
        "channel": "THS_MOBILE", # 渠道标识
        "pageSize": "10"       # 每页条数
    }
    
    try:
        # 发送POST请求（表单数据用data参数传递）
        response = requests.post(
            url,
            headers=headers,
            data=payload,
            verify=True
        )
        response.raise_for_status()  # 检查响应状态码
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求股票预警信息失败: {e}")
        return None

# 测试函数
if __name__ == "__main__":
    warning_data = add_stock_warning()
    if warning_data:
        print("股票预警信息:")
        print(json.dumps(warning_data, indent=2, ensure_ascii=False))  # 格式化显示内容