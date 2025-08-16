import requests
import json


def get_shareholder_reduction_announcements(annoucement_type):
    """获取股东减持相关公告（POST请求）"""
    # 请求URL
    url = "https://open.hscloud.cn/isee/v1/get_hedge_announcement_arr"

    # 请求头
    headers = {
        "Host": "open.hscloud.cn",
        "Connection": "keep-alive",
        "Pragma": "no-cache",
        "Cache-Control": "no-cache",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36;/sdsg",
        "Content-Type": "application/x-www-form-urlencoded; charset=UTF-8",
        "Origin": "https://vo5d17lv4.lightyy.com",
        "X-Requested-With": "com.shenguang.smartadvisor",
        "Sec-Fetch-Site": "cross-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://vo5d17lv4.lightyy.com/index.html?login_flag=0",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7"
    }

    # 请求体（表单数据，annoucement_type=1对应股东减持）
    payload = {
        "annoucement_type": annoucement_type,  # 明确指定为股东减持类型
        "page_size": "2",
        "page_num": "1",
        "chnl": "4009",
        "channel_id": "4009",
        "access_token": "A33BD8234D2C4A4BB84AA09A3877BAFF20250714104455463B610B"
    }

    try:
        # 发送POST请求（表单数据用data参数传递）
        response = requests.post(
            url,
            headers=headers,
            data=payload,
            verify=True
        )
        response_json =  response.json()
        print(response_json)
        response.raise_for_status()  # 检查HTTP状态码
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"请求股东减持公告失败: {e}")
        return None


# 测试函数
if __name__ == "__main__":
    name_to_id = {
        "1": "股东减持",
        "2": "业绩暴雷",
        "3": "大宗交易",
        "4": "限售解禁"
    }
    for annoucement_type, name in name_to_id.items():
        reduction_announcements = get_shareholder_reduction_announcements(annoucement_type)
        if reduction_announcements:
            print(f"（{name}）相关公告:")
            print(json.dumps(reduction_announcements, indent=2, ensure_ascii=False))  # 格式化显示内容
    # for annoucement_type in [1,2,3,4]:
    #
    #     reduction_announcements = get_shareholder_reduction_announcements(annoucement_type)
    #     if reduction_announcements:
    #         print("股东减持相关公告:")
    #         print(json.dumps(reduction_announcements, indent=2, ensure_ascii=False))  # 格式化显示内容