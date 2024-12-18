import requests
import pandas as pd

# 定义 listType 和对应的 Sheet 名称
list_types = {
    1: "日收益",
    2: "周收益",
    3: "月收益",
    4: "总收益"
}

# 接口的URL
url = "https://t.10jqka.com.cn/portfoliolist/tgserv/v1/blockList"

# 请求头信息
headers = {
    "Host": "t.10jqka.com.cn",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode/0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
    "Content-Type": "application/x-www-form-urlencoded",
    "Referer": "https://t.10jqka.com.cn/tgactivity/portfolioSquare.html",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0,ExLDQwOzYsMS,0MDs1,ExsNDA7MS,xMDEsNDA7Mi,xLDQwOzMs,ExsNDA7NS,ExsNDA7OC,wwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMS,0MDsxMDIs,ExsNDAoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_641926488\",\"userid\":\"641926488\"}; hxmPid=hqMarketPkgVersionControl; v=A8nfSB_XyhoyhrZuY3TPETuT0f4jFr1OJw_h3Gs-RF3vQeZks2bNGLda8aP4",
    "X-Requested-With": "com.hexin.plat.android"
}

# 使用 ExcelWriter 将数据写入同一个 Excel 文件的不同 Sheet
with pd.ExcelWriter(r"D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\组合\保存的数据\榜单数据.xlsx") as writer:
    for list_type, sheet_name in list_types.items():
        # 请求参数
        params = {
            "offset": 0,
            "pageSize": 300,
            "matchId": 0,
            "blockId": 0,
            "listType": list_type
        }

        # 发送GET请求
        response = requests.get(url, params=params, headers=headers)

        # 检查响应状态码
        if response.status_code == 200:
            data = response.json()
            # 将数据转换为DataFrame
            df = pd.DataFrame(data["result"]["list"])
            # 将 DataFrame 写入指定的 Sheet
            df.to_excel(writer, sheet_name=sheet_name, index=False)
            print(f"{sheet_name} 数据已保存")
        else:
            print(f"请求失败，listType: {list_type}, 状态码: {response.status_code}")
