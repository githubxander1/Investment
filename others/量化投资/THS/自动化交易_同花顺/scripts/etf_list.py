import requests


def send_request():
    url = 'https://t.10jqka.com.cn/portfoliolist/tgserv/v2/block_list'
    params = {
        'offset': 0,
        'page_size': 8,
        'block_id': 0,
        'list_type': 4,
      'match_id': 14
    }
    headers = {
        'Host': 't.10jqka.com.cn',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.19.03 (Royal Flush) hxtheme/1 innerversion/G037.08.990.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'com.hexin.plat.android',
        'Sec-Fetch-Site':'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://t.10jqka.com.cn/rankfront/portfolioSquare/index.html',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        'Cookie': 'user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM3MzM4ODA5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTJiMmY0NGE2ODgxYjg0Nzc1YzY2MzM2MGM2NGUxZjMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=ee119caec220dd3e984ad47c01216b5f; user_status=0; IFUserCookieKey={"escapename":"mo_641926488","userid":"641926488"}; hxmPid=hqMarketPkgVersionControl; v=A6tuLRSYSGb6z5Qy7FMGakAwOMSVwL9XOdOD9h0ohohBOMS-pZBPkkmkE1Iu'
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        print(response)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None


def extract_result(data):
    data = data.get('data', {})
    etf_list=data.get('list', [])
    extracted_data = []
    for item in etf_list:
        portfo_labels = item.get('portfolio_labels', [])
        label = portfo_labels[0]['label'] if portfo_labels else '无标签'
        etf_info = {
            '组合id': item.get('portfolio_id', 0),
            '组合名称': item.get('portfolio_name', ''),
            '盈亏率%': item.get('income_rate', 0) * 100,
            '标签': label
        }
        extracted_data.append(etf_info)
        # pprint(extracted_data)
    return extracted_data


def main():
    result = send_request()
    # pprint(result)
    extracted_result = extract_result(result)
    # extract_datas = f'提取{result}里的income_rate（用百分比表示），portfolio_id，portfolio_name，label，用pandas表格样式展示'
    # print(AIchat(extract_datas))
    # ids = [etf.get('portfolio_id') for etf in extracted_result]
    # print(ids)

    # df = pd.DataFrame(extracted_result)
    # df.to_excel('etf_list.xlsx', index=False)
    # print(df)
    # print(extracted_result)


if __name__ == "__main__":
    main()
