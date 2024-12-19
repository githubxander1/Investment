import re

import requests
import pandas as pd
from pprint import pprint

# 定义要请求的id列表
ids = [
        6994,18565,14980,16281,7152,13081,11094
    ]

# 定义英文列名到中文列名的映射
column_mapping = {
    "策略id": "策略id",
    "策略名称": "策略名称",
    "策略描述": "策略描述",
    "createAt": "创建时间",
    "dailyIncomeRate": "日收益率",
    "maxDrawdownRate": "最大回撤率",
    "totalIncomeRate": "总收益率",
    "product_name": "产品名称",
    "product_desc": "产品描述"
}

# 存储所有结果的列表
all_results = []

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
        # print(result)
        if result['status_code'] == 0:
            product_name = result['data']['baseInfo']['productName']
            product_desc = result['data']['baseInfo']['productDesc']
            userId = result['data']['userInfo']['userId']
            return {
                "策略id": product_id,
                "策略名称": product_name,
                "策略描述": product_desc,
                "主理人id": userId,

            }
        else:
            print(f"Failed to retrieve data for product_id: {product_id}")
            return None
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None


def get_position_income_info(portfolio_id):
    """
    根据组合ID获取组合收益信息
    :param portfolio_id: 组合ID
    :return: 包含收益信息的字典或None
    """
    url = "https://t.10jqka.com.cn/portfolio/v2/position/get_position_income_info"
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
    try:
        params = {"id": portfolio_id}
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['status_code'] == 0:
            result = data['data']
            result['策略ID'] = id
            createAt = result['createAt']
            dailyIncomeRate = result['dailyIncomeRate'] = f"{result['dailyIncomeRate'] * 100:.2f}%"
            maxDrawdownRate = result['maxDrawdownRate'] = f"{result['maxDrawdownRate'] * 100:.2f}%"
            totalIncomeRate = result['totalIncomeRate'] = f"{result['totalIncomeRate'] * 100:.2f}%"
            return {
                "创建时间": createAt,
                "日收益率": dailyIncomeRate,
                "最大回撤率": maxDrawdownRate,
                "总收益率": totalIncomeRate
            }
        else:
            print(f"请求错误 (id={id}): {data['status_msg']}")
            return None
    except requests.RequestException as e:
        print(f"请求出现错误 (id={id}): {e}")
        return None


def get_package_feature_info(product_id):
    """
    根据产品ID获取产品特性信息
    :param product_id: 产品ID
    :return: 包含产品特性信息的字典或None
    """
    url = "https://dq.10jqka.com.cn/fuyao/tg_package/package/v1/get_package_feature_info"
    headers = {
        "Host": "dq.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "Origin": "https://t.10jqka.com.cn",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=14533",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.hexin.plat.android"
    }
    params = {
        "product_id": product_id,
        "product_type": "portfolio"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        response = response.json()

        data = response['data']
        slogan = data['slogan']
        labels = data['labels']

        return {
            '累抓涨停次数': re.findall(r'\d+', slogan)[0],
            '标签': labels
        }
        # return response.json()
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None


def get_relocate_data_summary(portfolio_id):
    """
    根据组合ID获取调仓数据摘要
    :param portfolio_id: 组合ID
    :return: 包含调仓数据摘要的字典或None
    """
    url = "https://t.10jqka.com.cn/portfolio/relocate/v2/get_relocate_data_summary"

    # 请求头
    headers = {
        "Host": "t.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme=0 innerversion=G037.08.983.1.32 followPhoneSystemTheme=0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://t.10jqka.com.cn/portfolioFront/historyTransfer.html?id=14533",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNj04ODoxNzMzMT0xMTExOjo6MTY1ODE0834NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_488; escapename=mo_488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_488\",\"userid\":\"641926488\"}; hxmPid=hqMarketPkgVersionControl; v=A2J0tXgycd9rQ22D-pDEtNQeuuPEs2bNGLda8az7jlWAfw1ZlEO23ehHqgJ_",
    }
    params = {
        "id": portfolio_id,
    }
    response = requests.get(url, headers=headers, params=params)
    if response.status_code == 200:
        data = response.json()
        relocate_total = data["data"]["relocateTotal"]
        profit_total = data["data"]["profitTotal"]
        profit_margin = f'{data["data"]["profitMargin"] * 100:.2f}%'
        return {
            "调仓个股总数": relocate_total,
            "盈利个股数": profit_total,
            "胜率": profit_margin
        }
    else:
        print("请求失败，状态码:", response.status_code)


def get_position_industry_info(portfolio_id):
    """
    根据组合ID获取持仓行业信息
    :param portfolio_id: 组合ID
    :return: 包含持仓行业信息的字典或None
    """
    url = "https://t.10jqka.com.cn/portfolio/v2/position/get_position_industry_info"
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
        "Cookie": "IFUserCookieKey={}; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM0MDUzNTg5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTE3MTRjYTYwODhjNjRmYzZmNDFlZDRkOTJhMDU3NTMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=58d0f4bf66d65411bb8d8aa431e00721; user_status=0; hxmPid=sns_my_pay_new; v=A8oP8g1DmV6iqRXyZ91U_qvpGbtsu04VQD_CuVQDdp2oB2VhPEueJRDPEsAn"
    }
    params = {"id": portfolio_id}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        data = response.json()['data']
        return data
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None


def get_portfolio_profitability_period_win_hs300(portfolio_id):
    """
    根据组合ID获取组合与沪深300的收益对比
    :param portfolio_id: 组合ID
    :return: 包含收益对比信息的字典或None
    """
    url = "https://t.10jqka.com.cn/portfolioedge/calculate/v1/get_portfolio_profitability"
    headers = {
        "Host": "t.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=14533",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.hexin.plat.android"
    }
    params = {
        "id": portfolio_id
    }
    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        if 'data' in data and 'profitabilityDataList' in data['data']:
            profitability_data_list = data["data"]["profitabilityDataList"]
            result = {}
            for item in profitability_data_list:
                time_span = item["timeSpan"]
                portfolio_income = f'{item["portfolioIncome"] * 100:.2f}%'
                hs300_income = f'{item["hs300Income"] * 100:.2f}%'

                # 将时间跨度作为列标题
                # result[f'时间跨度_{time_span}'] = time_span
                result[f'收益比_{time_span}'] = {
                    '组合': portfolio_income,
                    '沪深3': hs300_income
                }
            return result
        else:
            print(f"API 响应格式不正确 (id={portfolio_id}): {data}")
            return None
    except requests.RequestException as e:
        print(f"请求出现错误 (id={portfolio_id}): {e}")
        return None
    except Exception as e:
        print(f"处理响应时出现错误 (id={portfolio_id}): {e}")
        return None

# 获取人气投顾的 userId 列表
def get_popular_advisors():
    """
    获取人气投顾的userId列表
    :return: 包含人气投顾userId的列表
    """
    url = "https://t.10jqka.com.cn/event/rank/popularity/v2"
    headers = {
        "Host": "t.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme=0 userid=641926488 getHXAPPAccessibilityMode=0 hxNewFont=1 isVip=0 getHXAPPFontSetting=normal getHXAPPAdaptOldSetting=0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": "https://t.10jqka.com.cn/tgactivity/portfolioSquare.html",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "user_status=0; user=MDptb18yNDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0,ExLDQwOzYsMSw0MDs1,ExsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1,ExsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzMzMTQxMTExOjo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MWEwZGI0MTE4MTk4NThiZDE2MDFjMDVmNDQ4N2M4ZjcxOjox; userid=641926488; u_name=mo_481926488; escapename=mo_481926488; ticket=c9840d8b7eefc37ee4c5aa8dd6b90656; IFUserCookieKey={\"escapename\":\"mo_481926488\",\"userid\":\"641926488\"}; hxmPid=sns_service_video_choice_detail_85853; v=Aw0bNHuLVti5yPKcsT7DJecHFSKH6kHtyxWlkE-SSIIT6SJYFzpRjFtutUDc",
        "X-Requested-With": "com.hexin.plat.android"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        data = response.json()
        if data['errorCode'] == 0:
            results = data['result']
            user_ids = [result['userId'] for result in results]
            return user_ids
        else:
            print(f"请求错误: {data['errorMsg']}")
            return []
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return []


# 循环请求每个id
for id in ids:
    product_info = get_product_info(id)
    position_income_info = get_position_income_info(id)
    relocate_data_summary = get_relocate_data_summary(id)
    package_feature_info = get_package_feature_info(id)
    industry_info = get_position_industry_info(id)
    profitability_info = get_portfolio_profitability_period_win_hs300(id)

    if profitability_info:
        combined_info = {
            **product_info,
            **position_income_info,
            **package_feature_info,
            **relocate_data_summary,
            **profitability_info
        }
        combined_info['持仓行业'] = industry_info

        # 获取人气投顾的 userId 列表
        popular_advisors = get_popular_advisors()
        if product_info and '主理人id' in product_info:
            combined_info['是否人气投顾'] = product_info['主理人id'] in popular_advisors
        else:
            combined_info['是否人气投顾'] = False

        all_results.append(combined_info)
    else:
        print(f"跳过，无法获取数据 (id={id})")


# 将所有结果转换为DataFrame
if all_results:
    df = pd.DataFrame(all_results)
    df.to_excel(r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\组合\保存的数据\组合_性价比_胜率_累涨停数_收益对比.xlsx', index=False)
    print("数据已成功保存到 '结合.xlsx'")
else:
    print("没有获取到任何数据")
