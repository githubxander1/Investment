import requests
import json
import pprint

def get_chip_shape_stock_selection():
    """获取筹码形态选股数据（GET请求）"""
    # 请求URL
    url = "https://dq.10jqka.com.cn/fuyao/chip_shape_stock_selection/selection/v1/list"
    
    # URL参数
    params = {
        "offset_num": "0",
        "page_size": "5",
        "shape_type": "3",#1低位锁定2低位密集3双峰形态4高位密集
        "chip_type": "1",
        "sort_field": "closing_profit",
        "sort_order": "desc",
        "filter_selfstock": "0",
        "date": "2025-08-01"
    }
    
    # 请求头
    headers = {
        "cookie": "userid=789096627; u_name=mt_7ci19pac9; escapename=mt_7ci19pac9; user_status=0; user=MDptdF83Y2kxOXBhYzk6Ok5vbmU6NTAwOjc5OTA5NjYyNzo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDo6Ojo3ODkwOTY2Mjc6MTc1MjkyNzg3MDo6OjE3NDk4NjYzNDA6MjY3ODQwMDowOjE1OWI5ZGUzMTgzOGEwNWRlNDg5ZDUwM2RhMDM0YjgyODo6MA%3D%3D; ticket=5f1ae7f729f9ea95ffa3cf97398d22c9; _clck=lud4y2%7C2%7Cfxq%7C0%7C0; v=A8mQZOnlxfUpZbmBEMbotK6W2v4jFr1IJwrh3Gs-RbDvsuZks2bNGLda8bz4; hxmPid=ths_jeton_show",
        "content-type": "application/json",
        "Host": "dq.10jqka.com.cn",
        "Connection": "Keep-Alive",
        "Accept-Encoding": "gzip",
        "User-Agent": "okhttp/3.14.9"
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
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求筹码形态选股数据失败: {e}")
        return None

# 测试函数
if __name__ == "__main__":
    chip_data = get_chip_shape_stock_selection()
    if chip_data:
        print("筹码形态选股数据:")
        print(json.dumps(chip_data, indent=2, ensure_ascii=False))  # 格式化显示内容