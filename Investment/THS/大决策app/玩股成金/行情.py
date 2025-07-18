def 行情数据():
    url = "http://stock.api.traderwin.com/api/stock/ticket/quote.json"

    headers = {
        "Content-Type": "application/json",
        "from": "Android",
        "token": "27129c04fb43a33723a9f7720f280ff9",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 7 Pro MIUI/V12.5.4.0.QFHCNXM)",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive"
    }

    symbols = [
        "sh510050","sh510110","sh510170","sh510300","sh510410","sh510650","sh512170","sh512200","sh512290","sh512400",
        "sh512660","sh512690","sh512720","sh512800","sh512880","sh512980","sh515030","sh515120","sh515210","sh515220",
        "sh515710","sh515880","sh515920","sh516010","sh516020","sh516090","sh516180","sh516320","sh516500","sh516550",
        "sh516560","sh516760","sh516770","sh516910","sh560800","sh561800","sh562300","sh588000","sz159708","sz159713",
        "sz159731","sz159745","sz159813","sz159819","SZ159840","sz159852","sz159855","sz159867","sz159890","sz159928",
        "sz159945","sz159995","sz159996"
    ]

    payload = {
        "cmd": "9003",
        "symbols": symbols
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


# 请求行情数据
result = 行情数据()

if result and result.get("message", {}).get("state") == 0:
    data_list = result.get("data", [])

    quote_records = []

    for quote in data_list:
        quote_info = {
            "股票代码": quote.get("symbol"),
            "股票名称": quote.get("name"),
            "最新价": quote.get("price"),
            "涨跌幅": quote.get("changeRate"),
            "涨跌额": quote.get("changeAmount"),
            "开盘价": quote.get("open"),
            "最高价": quote.get("high"),
            "最低价": quote.get("low"),
            "成交量": quote.get("volume"),
            "成交额": quote.get("turnover"),
            "时间戳": convert_timestamp(quote.get("time"))
        }
        quote_records.append(quote_info)

    # 转换为 DataFrame
    df_quotes = pd.DataFrame(quote_records)

    # 保存到 Excel 文件
    output_path = r"D:\1document\Investment\Investment\THS\大决策app\玩股成金\行情数据.xlsx"
    df_quotes.to_excel(output_path, sheet_name='行情数据', index=False)

    print(f"✅ 数据已成功保存到：{output_path}")

else:
    print("未收到有效响应或状态码错误")
