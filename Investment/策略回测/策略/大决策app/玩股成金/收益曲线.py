def 收益曲线(robot_id="9a09cbd9-be78-469c-b3d2-b2d07ad50862"):
    url = "http://ai.api.traderwin.com/api/ai/robot/report.json"

    headers = {
        "Content-Type": "application/json",
        "from": "Android",
        "token": "27129c04fb43a33723a9f7720f280ff9",
        "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 7 Pro MIUI/V12.5.4.0.QFHCNXM)",
        "Accept-Encoding": "gzip",
        "Connection": "Keep-Alive"
    }

    payload = {
        "cmd": "9016",
        "robotId": robot_id
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


# 请求收益曲线数据
result = 收益曲线()

if result and result.get("message", {}).get("state") == 0:
    data_list = result.get("data", [])

    report_records = []

    for report in data_list:
        report_info = {
            "日期": convert_timestamp(report.get("date")),
            "收益率": report.get("rate"),
            "累计收益": report.get("totalProfit"),
            "基准收益率": report.get("baseRate"),
            "基准累计收益": report.get("baseTotalProfit")
        }
        report_records.append(report_info)

    # 转换为 DataFrame
    df_reports = pd.DataFrame(report_records)

    # 保存到 Excel 文件
    output_path = r"D:\1document\Investment\Investment\THS\大决策app\玩股成金\收益曲线数据.xlsx"
    df_reports.to_excel(output_path, sheet_name='收益曲线', index=False)

    print(f"✅ 数据已成功保存到：{output_path}")

else:
    print("未收到有效响应或状态码错误")
