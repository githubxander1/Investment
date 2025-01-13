import requests
import requests


def get_stock_report_data():
    """
    该函数用于向指定接口发送请求，获取股票（代码为603118）的报告数据。
    """
    # 接口的URL地址，用于获取特定股票的报告数据，这里的17表示市场代码，603118是股票代码
    url = "https://basic.10jqka.com.cn/basicapi/report/data/17/603118/"
    # 请求头信息，包含了诸如浏览器标识、来源页面等多种信息，用于模拟正常的浏览器请求，使得服务器能够正确响应。
    headers = {
        "Host": "basic.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Referer": "https://basic.10jqka.com.cn/astockph/briefinfo/index.html?code=600188&marketid=17",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.hexin.plat.android"
    }
    # Cookie信息，通常包含了用户相关的一些标识、会话等信息，可能用于服务器识别用户、维持会话状态等（要注意其中隐私相关内容）
    cookies = {
        "user_status": "0",
        "user": "MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,MTExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMS,0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMS,0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox",
        "userid": "641926488",
        "u_name": "mo_641926488",
        "escapename": "mo_641926488",
        "ticket": "c9840d8b7eefc37ee4c5aa8dd6b90656",
        "IFUserCookieKey": '{"escapename":"mo_641926488","userid":"641926488"}',
        "hxmPid": "free_stock_600188.dstx",
        "v": "A5OFqiFpl7rRDLyyximlk70FKxy9SCcD4d9rPkWw7nXp-7zGzRi3WvGs--xW"
    }

    try:
        # 发送GET请求，向指定接口发起获取数据的请求，携带了相应的请求头和Cookie信息。
        response = requests.get(url, headers=headers, cookies=cookies)
        # 如果请求成功，即服务器返回的状态码为200，表示获取数据正常。
        if response.status_code == 200:
            # 尝试将返回的数据解析为JSON格式，方便后续对数据进行处理和分析，然后返回解析后的数据。
            return response.json()
        else:
            # 如果请求失败，打印出具体的失败状态码信息，方便排查问题，同时返回None，表示没有获取到有效数据。
            print(f"请求失败，状态码: {response.status_code}")
            return None
    except requests.RequestException as e:
        # 如果在请求过程中发生了其他异常（比如网络问题等），打印出异常信息，同样返回None。
        print(f"请求发生异常: {e}")
        return None

def save_to_excel(data, filename='stock_data.xlsx'):
    """
    将数据保存到Excel文件中
    """
    # 创建一个Excel writer对象
    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        # 保存count_data到Excel
        count_df = pd.DataFrame(data.get('count_data', []))
        count_df.to_excel(writer, sheet_name='count_data', index=False)

        # 保存forecast_data到Excel
        forecast_df = pd.DataFrame(data.get('forecast_data', []))
        forecast_df.to_excel(writer, sheet_name='forecast_data', index=False)

        # 保存quote_price到Excel
        quote_price_df = pd.DataFrame([data.get('quote_price', {})])
        quote_price_df.to_excel(writer, sheet_name='quote_price', index=False)

        # 保存select_data到Excel
        select_data = data.get('select_data', {})
        select_df = pd.DataFrame(select_data.get('data', []))
        select_df.to_excel(writer, sheet_name='select_data', index=False)

        # 保存select_data中的quote到Excel
        select_quote_df = pd.DataFrame(select_data.get('quote', []))
        select_quote_df.to_excel(writer, sheet_name='select_quote', index=False)

        print(f"数据已保存到 {filename}")

if __name__ == "__main__":
    # 调用函数来获取股票报告数据
    data = get_stock_report_data()
    if data:
        # 打印原始数据
        # pprint(data)

        # 提取count_data
        count_data = data['data']['count_data']
        count_summary = [
            {'时间范围': item['title'],
             '买入': round(item['buy'],0),
             '增持': item['over'],
             '中性': item['neutral'],
             '减持': item['reduce'],
             '卖出': item['sell']}
            for item in count_data
        ]

        # 提取forecast_data
        forecast_data = data['data']['forecast_data']
        forecast_summary = [
            {'年份': item['title'], '每股收益': item['stock_eps']}
            for item in forecast_data
        ]

        # 提取quote_price
        quote_price = data['data']['quote_price']
        quote_price_summary = [
            {'高': quote_price['high'], '低': quote_price['low']}
        ]
        #提取quote_price
        select_data = data['data']['select_data']['quote']
        select_quote_summary = [
            {'日期': item['date'], '价格': item['price']}
            for item in select_data
        ]

        # 合并所有数据到一个DataFrame
        # all_data = count_summary
        # forecast_data = forecast_summary + quote_price_summary
        count_summary_df = pd.DataFrame(count_summary)
        forecast_data_df = pd.DataFrame(forecast_data)
        quote_price_df = pd.DataFrame(quote_price_summary)
        select_data_df = pd.DataFrame(select_quote_summary)


        print(count_summary_df)
        print(forecast_data_df)
        print(quote_price_df)
        print(select_data_df)

        # 保存到Excel文件
        save_to_excel(data)
