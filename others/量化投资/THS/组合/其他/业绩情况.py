from pprint import pprint

import pandas as pd
import requests

# 接口URL
url = "https://t.10jqka.com.cn/portfolio/v2/position/get_position_income_info"

# 请求头
headers = {
    "Host": "t.10jqka.com.cn",
    "Connection": "keep-alive",
    "Accept": "application/json, text/plain, */*",
    "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.16.10 (Royal Flush) hxtheme/1 innerversion/G037.08.980.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
    "Content-Type": "application/x-www-form-urlencoded",
    "X-Requested-With": "com.hexin.plat.android",
    "Sec-Fetch-Site": "same-origin",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Dest": "empty",
    "Referer": "https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=19483",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
    "Cookie": "IFUserCookieKey={}; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM0MDUzNTg5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTE3MTRjYTYwODhjNjRmYzZmNDFlZDRkOTJhMDU3NTMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=58d0f4bf66d65411bb8d8aa431e00721; user_status=0; hxmPid=sns_my_pay_new; v=Ax_acQjchI2vDoCRe4xZjXburHiphHMmjdh3GrFsu04VQDBiuVQDdp2oB2PC"
}

# 定义要请求的id列表
ids = [
    19483,
    14533,
    16281,
    23768,
    8426,
    9564,
    6994,
    7152,
    20335,
    21302,
    19347,
    8187,
    18565,
    14980,
    16428
]

# 定义英文列名到中文列名的映射
column_mapping = {
    "createAt": "创建时间",
    "totalIncomeRate": "总收益率",
    "dailyIncomeRate": "日收益率",
    "maxDrawdownRate": "最大回撤率"
}

# 存储所有结果的列表
all_results = []

# 循环请求每个id
for id in ids:
    params = {"id": id}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()

        if data['status_code'] == 0:
            # 提取结果部分
            result = data['testdata']
            # 添加id信息以便区分
            result['策略ID'] = id
            # 将收益率转换为百分比
            result['dailyIncomeRate'] = f"{result['dailyIncomeRate'] * 100:.2f}%"
            result['maxDrawdownRate'] = f"{result['maxDrawdownRate'] * 100:.2f}%"
            result['totalIncomeRate'] = f"{result['totalIncomeRate'] * 100:.2f}%"
            all_results.append(result)
        else:
            print(f"请求错误 (id={id}): {data['status_msg']}")
    except requests.RequestException as e:
        print(f"请求出现错误 (id={id}): {e}")

# 将所有结果转换为DataFrame
if all_results:
    df = pd.DataFrame(all_results)
    # 重命名列
    df.rename(columns=column_mapping, inplace=True)
    # 打印到终端
    pprint(df)
    # 保存到Excel文件
    df.to_excel(r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\组合\保存的数据\业绩情况.xlsx', index=False)
    print("数据已成功保存到 '业绩情况.xlsx'")
else:
    print("没有获取到任何数据")
