def 今日推荐(page_size=10, index=1, cmd="9034"):
    url = "http://portal.api.traderwin.com/api/report/forecast/earning.json"

    headers = {
        "Content-Type": "application/json",
        "from": "Android",
        "token": "27129c04fb43a33723a9f7720f280ff9",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 7 Pro MIUI/V12.5.4.0.QFHCNXM)",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive"
    }

    payload = {
        "pageSize": page_size,
        "index": index,
        "cmd": cmd
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(payload))
        response.raise_for_status()
        response_data = response.json()
        pprint(response_data)
        return response_data
    except requests.exceptions.RequestException as e:
        print(f"请求失败: {e}")
        return None


# 请求今日推荐数据
result = 今日推荐()

if result and result.get("message", {}).get("state") == 0:
    data_list = result.get("data", {}).get("data", [])

    recommend_records = []

    for item in data_list:
        recommend_info = {
            "报告ID": item.get("id"),
            "股票代码": item.get("symbol"),
            "股票名称": item.get("name"),
            "行业": item.get("industry"),
            "推荐理由": item.get("reason"),
            "目标收益": item.get("targetReturn"),
            "发布时间": convert_timestamp(item.get("publishTime")),
            "有效期": item.get("validPeriod")
        }
        recommend_records.append(recommend_info)

    # 转换为 DataFrame
    df_recommends = pd.DataFrame(recommend_records)

    # 保存到 Excel 文件
    output_path = r"D:\1document\Investment\Investment\THS\大决策app\玩股成金\今日推荐数据.xlsx"
    df_recommends.to_excel(output_path, sheet_name='今日推荐', index=False)

    print(f"✅ 数据已成功保存到：{output_path}")

else:
    print("未收到有效响应或状态码错误")
