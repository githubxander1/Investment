from pprint import pprint

import pandas as pd
import requests

from others.Investment.THS.AutoTrade.config.settings import Combination_ids, Combination_ids_to_name


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
            product_name = result['testdata']['baseInfo']['productName']
            return product_name
        else:
            print(f"Failed to retrieve testdata for product_id: {product_id}")
            return None
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None
def get_showRelocateData(portfolioId):
    url = "https://t.10jqka.com.cn/portfolio/base/showRelocateData"
    params = {
        "portfolioId": portfolioId
    }
    headers = {
        "Host": "估值.py.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid=641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": f"https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id={portfolioId}",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "Cookie": "user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM0MDUzNTg5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTE3MTRjYTYwODhjNjRmYzZmNDFlZDRkOTJhMDU3NTMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=58d0f4bf66d65411bb8d8aa431e00721; user_status=0; IFUserCookieKey={'escapename':'mo_641926488','userid':'641926488'}; hxmPid=free_zhengu_002884; v=A16btkHntfVksuERtM-LYb1Hrf-gHyKZtOPWfQjnyqGcK_GlcK9yqYRzJorb",
        "X-Requested-With": "com.hexin.plat.android"
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()  # 假设返回的是JSON格式数据
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None

def get_newest_relocate_post(id):
    url = "https://t.10jqka.com.cn/portfolio/post/v2/get_newest_relocate_post"

    # 请求头
    headers = {
        "Host": "估值.py.10jqka.com.cn",
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
        "Cookie": "IFUserCookieKey={}; user=MDptb18yNDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM0MDUzNTg5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTE3MTRjYTYwODhjNjRmYzZmNDFlZDRkOTJhMDU3NTMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=58d0f4bf66d65411bb8d8aa431e00721; user_status=0; hxmPid=sns_my_pay_new; v=A8UAY_5aDh_T8CrD0hwDXwiQ1gr_gnkTwzZdaMcqgfwLXupwj9KJ5FOGbTdU"
    }
    params = {"id": id}
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        # pprint(response.json())
        return response.json()
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None

def process_newest_relocate_post_ids(ids):
    # with pd.ExcelWriter(r'/zothers/Investment/THS/组合/保存的数据/最新调仓_所有.xlsx') as writer:
    for id in ids:
        result = get_newest_relocate_post(id)
        if result and result['status_code'] == 0:
            data = result['testdata']
            content = data['content']
            relocate_list = data.get('relocateList', [])
            all_data = []
            for item in relocate_list:
                entry = {
                    # '内容': content,
                    '当前比例': item.get('currentRatio') * 100 if item.get('currentRatio') is not None else None,
                    '最终价格': item.get('finalPrice'),
                    '股票名称': item.get('name'),
                    '新比例': item.get('newRatio') * 100 if item.get('newRatio') is not None else None,
                    '组合ID': id
                }
                all_data.append(entry)

            df = pd.DataFrame(all_data)
            pprint(df)
            # df.to_excel(writer, sheet_name=get_product_info(id), index=False)
        else:
            print(f"Failed to retrieve testdata for id: {id}")
def process_showRelocateData_ids(ids):
    all_holding_info = []
    for portfolio_id in ids:
        result = get_showRelocateData(portfolio_id)
        # pprint(result)
        if result and result['errorMsg'] == 'Success':
            holding_info = result['result']['holdingInfo']
            relocateInfo = result['result']['relocateInfo']
            if relocateInfo is not None:
                profit_loss_rate_relocate = relocateInfo.get('profitLossRate')
                # pprint(relocateInfo)
                new_ratio = relocateInfo.get('newRatio')
                if profit_loss_rate_relocate is not None and new_ratio is not None:
                    relocateInfos = {
                        '组合id': portfolio_id,
                        '组合名称': id_to_name.get(portfolio_id, 'Unknown'),
                        '股票': relocateInfo.get('name'),
                        '成本价': relocateInfo.get('finalPrice'),
                        '盈亏率(%)': profit_loss_rate_relocate * 100,
                        '持仓比例(%)': new_ratio * 100,
                        '入仓时间': relocateInfo.get('relocateTime')
                    }
                    all_holding_info.append(relocateInfos)
                else:
                    print(f"Warning: Some fields in relocateInfo are None for combination_id: {portfolio_id}")
            else:
                print(f"Warning: relocateInfo is None for combination_id: {portfolio_id}")

            if holding_info is not None:
                profitLossRate = holding_info.get('profitLossRate')
                if profitLossRate is None:
                    profitLossRate = 0
                positionRealRatio = holding_info.get('positionRealRatio')
                if positionRealRatio is None:
                    positionRealRatio = 0

                all_holding_info.append({
                    '组合id': portfolio_id,
                    '组合名称': id_to_name.get(portfolio_id, 'Unknown'),
                    '股票': holding_info.get('name'),
                    '成本价': holding_info.get('costPrice'),
                    '现价': holding_info.get('presentPrice'),
                    '盈亏率(%)': profitLossRate * 100,
                    '持仓比例(%)': positionRealRatio * 100
                })
            else:
                print(f"Warning: holdingInfo is None for combination_id: {portfolio_id}")

        else:
            print(f"Failed to retrieve testdata for portfolioId: {portfolio_id}")

    df = pd.DataFrame(all_holding_info)
    print(df)
    df.to_excel(r'D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\组合\保存的数据\组合_持仓详情.xlsx', index=False)

if __name__ == '__main__':

    # combination_ids = [6994, 7152,18710, 16281, 19347, 13081, 14980]
    combination_ids = Combination_ids

    id_to_name = Combination_ids_to_name

    process_showRelocateData_ids(combination_ids)
    process_newest_relocate_post_ids(combination_ids)
