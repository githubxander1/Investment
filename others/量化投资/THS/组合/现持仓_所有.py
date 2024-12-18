from pprint import pprint

import requests
import pandas as pd

def get_product_info(product_id):
    url = "https://dq.10jqka.com.cn/fuyao/tg_package/package/v1/get_package_portfolio_infos"
    headers = {
        "Host": "dq.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.16.10 (Royal Flush) hxtheme/1 innerversion/G037.08.980.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://t.10jqka.com.cn",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=19483",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "IFUserCookieKey={}; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM0MDUzNTg5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTE3MTRjYTYwODhjNjRmYzZmNDFlZDRkOTJhMDU3NTMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=58d0f4bf66d65411bb8d8aa431e00721; user_status=0; hxmPid=sns_my_pay_new; v=AxLXmrX7ofaqkd2K73acRpPBYdP0Ixa9SCcK4dxrPkWw771JxLNmzRi3WvOv"
    }
    params = {
        "product_id": product_id,
        "product_type": "portfolio"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        result = response.json()
        # pprint(result)
        if result['status_code'] == 0:
            product_name = result['data']['baseInfo']['productName']
            return product_name
        else:
            print(f"Failed to retrieve data for product_id: {product_id}")
            return None
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None

def now_position_info(portfolio_id):
    headers = {
        "Host": "t.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme=0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=14533",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0834NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_488\",\"userid\":\"641926488\"}; hxmPid=hqMarketPkgVersionControl; v=A-74WWxOBbvQTHHfb2LwELiaNk-w77LBxLJmzRi3Wxqu5oH1gH8C-ZRDtsvr",
        "X-Requested-With": "com.hexin.plat.android"
    }
    url = f"https://t.10jqka.com.cn/portfolio/relocate/user/getPortfolioHoldingData?id={portfolio_id}"

    params = {
        "id": portfolio_id
    }
    response = requests.get(url, headers=headers, params=params)

    # 判断请求是否成功（状态码为200）
    if response.status_code == 200:
        data = response.json()
        pprint(data)
        positions = data["result"]["positions"]
        for item in positions:
            # profitLossRate = item["profitLossRate"]
            item["incomeRate"] = f'{item["incomeRate"] * 100:.2f}%'
            item["positionRealRatio"] = f'{item["positionRealRatio"] * 100:.2f}%'
            item["positionRelocatedRatio"] = f'{item["positionRelocatedRatio"] * 100:.2f}%'
            # item["profitLossRate"] = f'{item["profitLossRate"] * 100:.2f}%'
            item["profitLossRate"] = item["profitLossRate"]   # 修改这里

        return positions
    else:
        print(f"请求失败，ID: {portfolio_id}")
        return None

ids = [
        19483,14533, 16281, 23768, 8426, 9564, 6994, 7152,
        20335, 21302, 19347, 8187, 18565, 14980, 16428
    ]

import pandas as pd

# 创建一个空的汇总表 DataFrame
summary_df = pd.DataFrame(columns=['code', 'costPrice', 'freezeRatio', 'incomeRate', 'marketCode', 'name',
                                   'positionRealRatio', 'positionRelocatedRatio', 'price', 'profitLossRate'])

# 循环遍历每个 id
for portfolio_id in ids:
    positions = now_position_info(portfolio_id)

    # 将持仓数据转换为 DataFrame
    df = pd.DataFrame(positions)
    df['profitLossRate'] = df['profitLossRate'].astype(float)

    # 检查 DataFrame 是否为空
    if not df.empty:
        # 将当前组合的数据追加到汇总表中
        summary_df = pd.concat([summary_df, df], ignore_index=True)

# 计算正负收益数量
positive_count = (summary_df['profitLossRate'] > 0).sum()
negative_count = (summary_df['profitLossRate'] < 0).sum()

# 打印结果
print(f"正收益数量: {positive_count}")
print(f"负收益数量: {negative_count}")

# 创建一个 ExcelWriter 对象
with pd.ExcelWriter(r"D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\组合\保存的数据\现持仓信息_所有.xlsx") as writer:
    # 将汇总表写入 Excel 文件
    summary_df.to_excel(writer, sheet_name="汇总表", index=False)

    # 循环遍历每个 id
    for portfolio_id in ids:
        positions = now_position_info(portfolio_id)

        sheetName = get_product_info(portfolio_id)
        if sheetName is not None:
            # 将持仓数据转换为 DataFrame
            df = pd.DataFrame(positions)

            # 将 DataFrame 写入 Excel 文件的不同工作表中
            df.to_excel(writer, sheet_name=sheetName, index=False)
        else:
            print(f"无法获取策略名称，ID: {portfolio_id}")

print("已成功保存到 '现持仓信息_所有.xlsx' 文件中。")
