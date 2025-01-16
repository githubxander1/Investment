from pprint import pprint

import requests

# 请求的URL
url = "https://ms.10jqka.com.cn/index/robotindex/"
# 请求参数
params = {
    "tag": "策略详情选股表格",
    "q": "TMT概念，近三日资金净流入大于5000万，非ST，非停牌"
}
# 请求头，直接复制提供内容
headers = {
    "Host": "ms.10jqka.com.cn",
    "Connection": "keep-alive",
    "Origin": "https://bowerbird.10jqka.com.cn",
    "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
    "Accept": "*/*",
    "Referer": "https://bowerbird.10jqka.com.cn/thslc/editor/view/15f2E0a579?strategyId=155259",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,en-US;q=0.9",
    "X-Requested-With": "com.hexin.plat.android"
}

# 发送GET请求
response = requests.get(url, params=params, headers=headers)

# 判断请求是否成功（状态码为200表示成功）
if response.status_code == 200:
    result = response.json()
    # pprint(result)
    # 提取数据
    try:
        data = result["answer"]["components"][0]["testdata"]
        # pprint(testdata)
        for row in data:
            columns = data["columns"]
            columns_names = ["label"]

            datas = data["datas"]

            pprint(columns)
            pprint(datas)
            # df = pd.DataFrame(datas, columns=columns)


            # print(df)
        # columns = [col["label"] for col in testdata["columns"]]
        # rows = []
        # for row in testdata["datas"]:
        #     rows.append([row[col["key"]] for col in testdata["columns"]])
        #
        # # 提取重要字段
        # important_columns = ["code", "股票简称", "最新价", "涨跌幅", "所属概念", "区间资金流向[20241212-20241216]", "交易状态[20241216]"]
        # important_data = []
        # for row in testdata["datas"]:
        #     important_row = {col["label"]: row[col["key"]] for col in testdata["columns"] if col["label"] in important_columns}
        #     important_data.append(important_row)
        #
        # # 创建DataFrame并保存为Excel
        # df = pd.DataFrame(important_data)
        # save_path = "D:\\1document\\1test\\PycharmProject_gitee\\zothers\\量化投资\\THS\\策略\\选股结果.xlsx"
        # df.to_excel(save_path, index=False)
        # print(f"文件已保存到: {save_path}")
        # # 控制台展示
        # print(df)
    except KeyError as e:
        print(f"KeyError: {e}")
        print("Received JSON testdata:")
        pprint(result)
else:
    print(f"请求失败，状态码: {response.status_code}")
