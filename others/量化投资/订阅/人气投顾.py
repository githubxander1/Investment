from pprint import pprint
import requests
import pandas as pd

url = "https://t.10jqka.com.cn/event/rank/popularity/v2"
headers = {
    "Host": "t.10jqka.com.cn",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://t.10jqka.com.cn/tgactivity/portfolioSquare.html",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "Cookie": "user_status=0; user=MDptb18yNDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0,ExLDQwOzYsMSw0MDs1,ExsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1,ExsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_641926488\",\"userid\":\"641926488\"}; hxmPid=sns_service_video_choice_detail_85853; v=Aw0bNHuLVti5yPKcsT7DJecHFSKH6kHtyxWlkE-SSIIT6SJYFzpRjFtutUDc",
    "X-Requested-With": "com.hexin.plat.android"
}

try:
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    if data['errorCode'] == 0:
        # 提取结果部分
        results = data['result']

        # 将结果转换为DataFrame
        df = pd.DataFrame(results)

        # 打印到终端
        pprint(df)

        # 保存到Excel文件
        df.to_excel('人气投顾.xlsx', index=False)
        print("数据已成功保存到 '人气投顾.xlsx'")
    else:
        print(f"请求错误: {data['errorMsg']}")
except requests.RequestException as e:
    print(f"请求出现错误: {e}")
