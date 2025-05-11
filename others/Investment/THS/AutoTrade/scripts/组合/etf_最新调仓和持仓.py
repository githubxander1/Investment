from pprint import pprint

import pandas as pd
import requests

from others.Investment.THS.AutoTrade.config.settings import ETF_ids, ETF_ids_to_name, \
    Combination_ids, Combination_ids_to_name, ETF_adjustment_holding_file, Combination_headers


def send_request(id):
    url = 'https://t.10jqka.com.cn/portfolio/base/showRelocateData'
    params = {
        'portfolioId': id
    }
    headers = Combination_headers
    # {
    #     'Host': 't.10jqka.com.cn',
    #     'Connection': 'keep-alive',
    #     'Accept': 'application/json, text/plain, */*',
    #     'User-Agent': 'Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.19.03 (Royal Flush) hxtheme/1 innerversion/G037.08.990.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0',
    #     'Content-Type': 'application/x-www-form-urlencoded',
    #     'X-Requested-With': 'com.hexin.plat.android',
    #     'Sec-Fetch-Site': 'same-origin',
    #     'Sec-Fetch-Mode': 'cors',
    #     'Sec-Fetch-Dest': 'empty',
    #     'Referer': 'https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=29617',
    #     'Accept-Encoding': 'gzip, deflate',
    #     'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
    #     "Cookie": 'userid=641926488; u_name=mo_641926488; escapename=mo_641926488; user_status=0; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzQwNzA2ODQ0Ojo6MTY1ODE0Mjc4MDo2MDQ4MDA6MDoxOTMwZmRiNzY5ZDZlMTk5MjQxY2RhZWVkYThiYWJjMDk6OjA%3D; ticket=1cac108f03adacab2cb19bf208226df5; IFUserCookieKey={"escapename":"mo_641926488","userid":"641926488"}; hxmPid=seq_666442234; v=A6RhQNdFn9G32-ud_WqRL5OFd6mWPcinimFc677FMG8yaUuT5k2YN9pxLGoN'
    #
    # }

    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        print(f"请求出错: {e}")
        return None

def extract_result(data, id):
    result = data.get('result', {})
    if not result:
        print(f"ID: {id} 无有效结果数据")
        return None, None, None

    # 安全获取嵌套数据
    holdingInfo = result.get('holdingInfo', {}) or {}
    relocateInfo = result.get('relocateInfo', {}) or {}

    # 处理holding_count
    holding_count = result.get('holdingCount', 0)
    if holding_count is None:
        holding_count = 0
    print(f"{Combination_ids_to_name.get(id, ETF_ids_to_name.get(id, '未知ETF'))} 的持仓数量为: {holding_count}")

    # 处理调仓信息
    relocate_Info = []
    if relocateInfo.get('code'):
        current_ratio = relocateInfo.get('currentRatio', 0) or 0
        new_ratio = relocateInfo.get('newRatio', 0) or 0
        profitLossRate = relocateInfo.get('profitLossRate', 0) or 0

        relocate_Info.append({
            # 'ETF组合': ETF_ids_to_name.get(id, '未知ETF'),
            'ETF组合': Combination_ids_to_name.get(id, '未知ETF'),
            '股票代码': relocateInfo.get('code'),
            # '市场': relocateInfo.get('marketCode'),
            '名称': relocateInfo.get('name'),
            '当前比例%': round(float(current_ratio) * 100, 2),
            '新比例%': round(float(new_ratio) * 100, 2),
            '当前价': relocateInfo.get('finalPrice'),
            '盈亏率%': round(float(profitLossRate) * 100, 2),
            '调仓时间': relocateInfo.get('relocateTime'),
        })

    # 处理持仓信息
    holding_Info = []
    if holdingInfo.get('code'):
        holding_Info.append({
            'ETF组合': ETF_ids_to_name.get(id, '未知ETF'),
            '股票代码': holdingInfo.get('code'),
            # '市场': holdingInfo.get('marketCode'),
            '名称': holdingInfo.get('name'),
            '新比例%': round(float(holdingInfo.get('positionRealRatio', 0)) * 100, 2),
            '当前价': holdingInfo.get('presentPrice'),
            '成本价': holdingInfo.get('costPrice'),
            '盈亏率%': round(float(holdingInfo.get('profitLossRate', 0)) * 100, 2),
        })

    return relocate_Info, holding_Info, holding_count

def save_results_to_xlsx(relocation_data, holding_data, filename):
    # 检查文件是否存在
    try:
        with pd.ExcelFile(filename) as _:
            # 文件存在，追加模式
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                if relocation_data:
                    df_relocation = pd.DataFrame(relocation_data)
                    # print(df_relocation)
                    df_relocation.to_excel(writer, sheet_name='ETF组合调仓', index=False)
                    print(f"调仓结果已保存到 {filename}")
                else:
                    print("没有调仓数据")

                if holding_data:
                    df_holding = pd.DataFrame(holding_data)
                    # print(df_holding)
                    df_holding.to_excel(writer, sheet_name='ETF组合持仓', index=False)
                    print(f"持仓结果已保存到 {filename}")
                else:
                    print("没有持仓数据")
    except FileNotFoundError:
        # 文件不存在，创建新文件
        with pd.ExcelWriter(filename, engine='openpyxl') as writer:
            if relocation_data:
                df_relocation = pd.DataFrame(relocation_data)
                # print(df_relocation)
                df_relocation.to_excel(writer, sheet_name='ETF组合调仓', index=False)
                print(f"调仓结果已保存到 {filename}")
            else:
                print("没有调仓数据")

            if holding_data:
                df_holding = pd.DataFrame(holding_data)
                # print(df_holding)
                df_holding.to_excel(writer, sheet_name='ETF组合持仓', index=False)
                print(f"持仓结果已保存到 {filename}")
            else:
                print("没有持仓数据")

def main():
    all_relocation_data = []
    all_holding_data = []
    # for id in ETF_ids:
    for id in Combination_ids:
        result = send_request(id)
        # pprint(result)
        if not result or not result.get('result'):
            print(f"ID {id} 返回无效数据")
            continue  # 跳过无效数据

        try:
            relocation_data, holding_data, holding_count = extract_result(result, id)
            # print(relocation_data)
            # print(holding_data)
            if relocation_data:
                all_relocation_data.extend(relocation_data)
                # pprint(all_relocation_data)
            if holding_data:
                all_holding_data.extend(holding_data)
                all_holding_data.extend(relocation_data)
                # pprint(all_holding_data)
        except Exception as e:
            print(f"处理ID {id} 时发生异常: {str(e)}")
            continue

    df = pd.DataFrame(all_holding_data)
    print(df)

    save_path = ETF_adjustment_holding_file
    save_results_to_xlsx(all_relocation_data, all_holding_data, save_path)

if __name__ == "__main__":
    main()
