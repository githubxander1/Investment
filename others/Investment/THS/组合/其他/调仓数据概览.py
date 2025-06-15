from pprint import pprint

import requests


def get_relocate_data_summary(id):
    # 接口URL
    url = "https://t.10jqka.com.cn/portfolio/relocate/v2/get_relocate_data_summary"

    # 请求头
    headers = {
        "Host": "估值.py.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme=0 innerversion=G037.08.983.1.32 followPhoneSystemTheme=0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://t.10jqka.com.cn/portfolioFront/historyTransfer.html?id=14533",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNj04ODoxNzMzMT0xMTExOjo6MTY1ODE0834NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_488; escapename=mo_488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_488\",\"userid\":\"641926488\"}; hxmPid=hqMarketPkgVersionControl; v=A2J0tXgycd9rQ22D-pDEtNQeuuPEs2bNGLda8az7jlWAfw1ZlEO23ehHqgJ_",
    }

    params = {
        "id": id,
    }

    # 发送GET请求
    response = requests.get(url, headers=headers, params=params)

    # 处理响应
    if response.status_code == 200:
        data = response.json()
        # pprint(testdata)
        # 提取调仓总次数
        relocate_total = data["testdata"]["relocateTotal"]
        # 提取盈利总次数
        profit_total = data["testdata"]["profitTotal"]
        # 提取利润率
        profit_margin = f'{data["testdata"]["profitMargin"] * 100:.2f}%'

        # print("调仓个股总数:", relocate_total)
        # print("盈利个股数:", profit_total)
        # print("胜率:", profit_margin)
        return relocate_total, profit_total, profit_margin
    else:
        print("请求失败，状态码:", response.status_code)


# pprint(get_relocate_data_summary(19347))

ids = [19347, 18565, 19880, 7152, 18868, 16281, 14980,
       13081, 11094, 12436, 6602, 6994, 20335, 18710,
       9564, 20244, 20245, 20442, 18669, 20205]
for id in ids:
    pprint(get_relocate_data_summary(id))