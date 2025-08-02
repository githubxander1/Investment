import requests
import json

def get_etf_opportunity():
    """获取ETF机会值相关数据（GET请求）"""
    # 请求URL
    url = "https://fund.10jqka.com.cn/quotation/open/api/select/tool/v1/cache/index_opportunity_value"
    
    # 请求头
    headers = {
        "Host": "fund.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "hexin-v": "A_KraX7QzoCKS_K8D8cTwTFLQTPUg_YdKIfqQbzLHqWQT53ppBNGLfgXOlOP",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.30.02 (Royal Flush) hxtheme/0 innerversion/G037.09.033.1.32 followPhoneSystemTheme/0 userid/-789096627 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "sw8": "1-MWExNjYwZjItYmFhYy00Zjc5LTk1MWItNTU2N2M1YzBhZmZi-Yzg3NDRjYjQtMzZkNS00MzJhLTg4N2MtZGNmYWYwZmI3Mjgz-0-dGhzamotamotZXRmLXRvb2wtY2hhbmNlPGJyb3dzZXI+-dGhzX2dwaG9uZS5vbmxpbmU=-L2ZlZnVuZC9ldGYtdG9vbC1jaGFuY2Uvc2N5bV9zY3N5L3B1YmxpYy9pbmRleC5odG1s-ZnVuZC4xMGpxa2EuY29tLmNu",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-origin",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://fund.10jqka.com.cn/fefund/etf-tool-chance/scym_scsy/public/index.html",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "userid=789096627; u_name=mt_7ci19pac9; escapename=mt_7ci19pac9; user_status=0; user=MDptdF83Y2kxOXBhYzk6Ok5vbmU6NTAwOjc5OTA5NjYyNzo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDo6Ojo3ODkwOTY2Mjc6MTc1MjkyNzg3MDo6OjE3NDk4NjYzNDA6MjY3ODQwMDowOjE1OWI5ZGUzMTgzOGEwNWRlNDg5ZDUwM2RhMDM0YjgyODo6MA%3D%3D; ticket=5f1ae7f729f9ea95ffa3cf97398d22c9; _clck=lud4y2%7C2%7Cfxq%7C0%7C0; hxmPid=fund_mkt_20230301_etfrmjh; v=A_KraX7QzoCKS_K8D8cTwTFLQTPUg_YdKIfqQbzLHqWQT53ppBNGLfgXOlOP"
    }
    
    try:
        # 发送GET请求（无额外参数，参数已包含在请求头中）
        response = requests.get(
            url,
            headers=headers,
            verify=True
        )
        response.raise_for_status()  # 检查响应状态码
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求ETF机会数据失败: {e}")
        return None

# 测试函数
if __name__ == "__main__":
    etf_data = get_etf_opportunity()
    if etf_data:
        print("ETF机会值数据:")
        print(json.dumps(etf_data, indent=2, ensure_ascii=False))  # 格式化显示内容