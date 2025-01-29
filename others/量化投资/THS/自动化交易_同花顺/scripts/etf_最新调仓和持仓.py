from pprint import pprint

import pandas as pd
import requests

from others.量化投资.THS.自动化交易_同花顺.config.settings import ETF_ids, ETF_ids_to_name, ETF_info_file


def send_request(id):
    url = 'https://t.10jqka.com.cn/portfolio/base/showRelocateData'
    params = {
        'portfolioId': id
    }
    headers = {
        'Host': 't.10jqka.com.cn',
        'Connection': 'keep-alive',
        'Accept': 'application/json, text/plain, */*',
        'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.19.03 (Royal Flush) hxtheme/1 innerversion/G037.08.990.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0',
        'Content-Type': 'application/x-www-form-urlencoded',
        'X-Requested-With': 'com.hexin.plat.android',
        'Sec-Fetch-Site': 'same-origin',
        'Sec-Fetch-Mode': 'cors',
        'Sec-Fetch-Dest': 'empty',
        'Referer': 'https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=29617',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        # 'Cookie': 'user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM3MzM4ODA5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTJiMmY0NGE2ODgxYjg0Nzc1YzY2MzM2MGM2NGUxZjMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=ee119caec220dd3e984ad47c01216b5f; user_status=0; IFUserCookieKey={"escapename":"mo_641926488","userid":"641926488"}; hxmPid=hqMarketPkgVersionControl; v=A9wZOK8t13tZQ6Mni-zpRystr_GOVYB9AvmUQ7bd6EeqAXMr3mVQD1IJZMIF'
        'Cookie': 'user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM3MzM4ODA5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTJiMmY0NGE2ODgxYjg0Nzc1YzY2MzM2MGM2NGUxZjMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=ee119caec220dd3e984ad47c01216b5f; user_status=0; IFUserCookieKey={"escapename":"mo_641926488","userid":"641926488"}; hxmPid=hqMarketPkgVersionControl; v=A3671mFHlbGOHsGVwLBrwZ3nzZ_Av0I51IP2HSiH6kG8yxEFkE-SSaQTRif7'
    }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None

def extract_result(data, id):
    result = data.get('result', None)
    pprint(result)
    if not result:
        print(f"ID: {id} 无数据")
        return None, None

    holding_data = result.get('holdingInfo', None)
    relocation_data = result.get('relocationData', None)

    relocation_data_infos = []  # 最新调仓
    if relocation_data:
        pprint(relocation_data)
        if isinstance(relocation_data, dict):
            relocation_data = [relocation_data]  # 将字典转换为列表
        for relocateInfo in relocation_data:
            relocation_data_infos.append({
                'ETF组合': ETF_ids_to_name.get(id, '未知ETF'),
                '股票代码': relocateInfo.get('code'),
                '市场': relocateInfo.get('marketCode'),
                '名称': relocateInfo.get('name'),
                '持仓比例%': round(relocateInfo.get('positionRealRatio') * 100, 2),
                '当前价': relocateInfo.get('presentPrice'),
                '盈亏率%': round(relocateInfo.get('profitLossRate') * 100, 2),
                '持仓时间': relocateInfo.get('relocateTime'),
            })
    else:
        print(f"{ETF_ids_to_name.get(id, '未知ETF')}数据中未找到'relocationData'字段")

    holding_data_infos = []  # 最新持仓
    if holding_data:
        if isinstance(holding_data, dict):
            holding_data = [holding_data]  # 将字典转换为列表
        for holdingInfo in holding_data:
            holding_data_infos.append({
                'ETF组合': ETF_ids_to_name.get(id, '未知ETF'),
                '股票代码': holdingInfo.get('code'),
                '市场': holdingInfo.get('marketCode'),
                '名称': holdingInfo.get('name'),
                '持仓比例%': round(holdingInfo.get('positionRealRatio') * 100, 2),
                '当前价': holdingInfo.get('presentPrice'),
                '盈亏率%': round(holdingInfo.get('profitLossRate') * 100, 2),
            })
    else:
        print(f"{ETF_ids_to_name.get(id, '未知ETF')}数据中未找到'holdingInfo'字段")

    return relocation_data_infos, holding_data_infos

def save_results_to_xlsx(relocation_data, holding_data, filename):
    # 检查文件是否存在
    try:
        with pd.ExcelFile(filename) as _:
            # 文件存在，追加模式
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                if relocation_data:
                    df_relocation = pd.DataFrame(relocation_data)
                    print(df_relocation)
                    df_relocation.to_excel(writer, sheet_name='ETF组合调仓', index=False)
                    print(f"调仓结果已保存到 {filename}")
                else:
                    print("没有调仓数据")

                if holding_data:
                    df_holding = pd.DataFrame(holding_data)
                    print(df_holding)
                    df_holding.to_excel(writer, sheet_name='ETF组合持仓', index=False)
                    print(f"持仓结果已保存到 {filename}")
                else:
                    print("没有持仓数据")
    except FileNotFoundError:
        # 文件不存在，创建新文件
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            if relocation_data:
                df_relocation = pd.DataFrame(relocation_data)
                print(df_relocation)
                df_relocation.to_excel(writer, sheet_name='ETF组合调仓', index=False)
                print(f"调仓结果已保存到 {filename}")
            else:
                print("没有调仓数据")

            if holding_data:
                df_holding = pd.DataFrame(holding_data)
                print(df_holding)
                df_holding.to_excel(writer, sheet_name='ETF组合持仓', index=False)
                print(f"持仓结果已保存到 {filename}")
            else:
                print("没有持仓数据")

def main():
    all_relocation_data = []
    all_holding_data = []
    for id in ETF_ids:
        result = send_request(id)
        # pprint(result)
        if result:
            relocation_data, holding_data = extract_result(result, id)
            if relocation_data:
                all_relocation_data.extend(relocation_data)
            if holding_data:
                all_holding_data.extend(holding_data)
        else:
            print(f"未获取到有效数据 (ID: {id})")

    save_path = ETF_info_file
    save_results_to_xlsx(all_relocation_data, all_holding_data, save_path)

if __name__ == "__main__":
    main()
