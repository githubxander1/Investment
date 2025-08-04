import requests
import json
import re

def get_theme_investment_data():
    """获取主题投资相关数据（GET请求）"""
    # 请求URL
    url = "https://ms.10jqka.com.cn/mobile/NewHotSpotStocks/indexData"
    
    # URL参数
    params = {
        "params": "jrjh%3A7%2Czcxjh%3A5",  # 编码后的参数，对应主题筛选条件
        "user": "MDptdF83Y2kxOXBhYzk6Ok5vbmU6NTAwOjc5OTA5NjYyNzo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDo6Ojo3ODkwOTY2Mjc6MTc1MjkyNzg3MDo6OjE3NDk4NjYzNDA6MjY3ODQwMDowOjE1OWI5ZGUzMTgzOGEwNWRlNDg5ZDUwM2RhMDM0YjgyODo6MA%3D%3D",
        "ticket": "5f1ae7f729f9ea95ffa3cf97398d22c9",
        "source": "scwcznxg",
        "_": "1754128035294",  # 时间戳，用于防缓存
        "callback": "Zepto1754128035232"  # JSONP回调函数名
    }
    
    # 请求头
    headers = {
        "Host": "ms.10jqka.com.cn",
        "Connection": "keep-alive",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.30.02 (Royal Flush) hxtheme/0 innerversion/G037.09.033.1.32 followPhoneSystemTheme/0 userid/-789096627 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Accept": "*/*",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "no-cors",
        "Sec-Fetch-Dest": "script",
        "Referer": "https://search.10jqka.com.cn//wukong//mobile//themeinvestment.html",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "userid=789096627; u_name=mt_7ci19pac9; escapename=mt_7ci19pac9; user_status=0; user=MDptdF83Y2kxOXBhYzk6Ok5vbmU6NTAwOjc5OTA5NjYyNzo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDo6Ojo3ODkwOTY2Mjc6MTc1MjkyNzg3MDo6OjE3NDk4NjYzNDA6MjY3ODQwMDowOjE1OWI5ZGUzMTgzOGEwNWRlNDg5ZDUwM2RhMDM0YjgyODo6MA%3D%3D; ticket=5f1ae7f729f9ea95ffa3cf97398d22c9; _clck=lud4y2%7C2%7Cfxq%7C0%7C0; hxmPid=free_iwencai_redian_all; v=A00U2E35GaGljr2NISGkQDLCXmLHKoH8C17l0I_SieRThmKYV3qRzJuu9aMc"
    }
    
    try:
        # 发送GET请求
        response = requests.get(
            url,
            params=params,
            headers=headers,
            verify=True
        )
        response.raise_for_status()  # 检查响应状态码
        
        # 处理JSONP格式响应（去除回调函数包裹，提取JSON）
        response_text = response.text
        json_data = re.search(r'Zepto1754128035232\((.*?)\)', response_text).group(1)
        return json.loads(json_data)
        
    except requests.exceptions.RequestException as e:
        print(f"请求主题投资数据失败: {e}")
        return None
    except (re.error, json.JSONDecodeError) as e:
        print(f"解析主题投资数据失败: {e}")
        return None

# 测试函数
if __name__ == "__main__":
    theme_data = get_theme_investment_data()
    if theme_data:
        print("主题投资数据:")
        print(json.dumps(theme_data, indent=2, ensure_ascii=False))  # 格式化显示内容