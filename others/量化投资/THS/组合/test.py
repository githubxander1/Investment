from pprint import pprint
import requests
import pandas as pd

def fetch_and_translate_data(portfolio_id):
    # 请求的URL
    url = f"https://t.10jqka.com.cn/portfolio/post/v2/get_newest_relocate_post?id={portfolio_id}"
    # 请求头，直接复制提供的内容
    headers = {
        "Host": "t.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": f"https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id={portfolio_id}",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.hexin.plat.android"
    }

    # 发送GET请求
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是200，会抛出HTTPError异常
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP 错误发生: {http_err}")
        return None
    except Exception as err:
        print(f"其他错误发生: {err}")
        return None

    try:
        result = response.json()
    except ValueError as json_err:
        print(f"JSON 解析错误: {json_err}")
        return None

    # 翻译字段
    translated_result = {
        "状态码": result.get("status_code"),
        "数据": {
            "头像": result.get("data", {}).get("avatar"),
            "频道名称": result.get("data", {}).get("channelName"),
            "评论数量": result.get("data", {}).get("commentNumber"),
            "内容": result.get("data", {}).get("content"),
            "创建时间": result.get("data", {}).get("createAt"),
            "创作者": result.get("data", {}).get("creator"),
            "动态ID": result.get("data", {}).get("dynamicId"),
            "调仓原因": result.get("data", {}).get("needRelocateReason"),
            "帖子ID": result.get("data", {}).get("pid"),
            "调仓列表": [
                {
                    "代码": item.get("code"),
                    "当前占比": item.get("currentRatio"),
                    "最终价格": item.get("finalPrice"),
                    "名称": item.get("name"),
                    "新占比": item.get("newRatio"),
                    "状态": item.get("state"),
                    "类型": item.get("type")
                }
                for item in result.get("data", {}).get("relocateList", [])
            ],
            "状态": result.get("data", {}).get("state"),
            "类型": result.get("data", {}).get("type"),
            "用户ID": result.get("data", {}).get("userId"),
            "有效": result.get("data", {}).get("valid")
        },
        "状态消息": result.get("status_msg")
    }
    pprint(translated_result)

    # 提取特定股票的信息
    specific_stock_info = next((item for item in translated_result["数据"]["调仓列表"] if item["代码"] == '688035'), None)

    # 构建结果字典
    result_dict = {
        "ID": portfolio_id,
        "内容": translated_result["数据"]["内容"],
        "创建时间": translated_result["数据"]["创建时间"],
        "调仓原因": translated_result["数据"]["调仓原因"],
        "频道名称": translated_result["数据"]["频道名称"],
        "特定股票信息": specific_stock_info
    }
    return result_dict

# 要查询的id列表
idids = [
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

# 存储所有结果的列表
all_results = []

for portfolio_id in idids:
    result = fetch_and_translate_data(portfolio_id)
    if result:
        all_results.append(result)

# 打印到控制台
pprint(all_results)

# 将结果转换为DataFrame
if all_results:
    df = pd.DataFrame(all_results)
    # 保存为Excel文件
    df.to_excel("newest_relocate_posts_comparison.xlsx", index=False)
else:
    print("没有成功获取任何数据")
