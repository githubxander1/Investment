import os
import logging
from Investment.THS.AutoTrade.utils.logger import setup_logger

# 使用 setup_logger 获取统一的 logger 实例
logger = setup_logger("etf_relocation_holding.log")

import pandas as pd
import requests

from Investment.THS.AutoTrade.config.settings import ETF_ids_to_name, \
    Combination_ids_to_name, Combination_holding_file, Combination_headers, \
    all_ids, id_to_name


def send_request(id):
    # 示例请求逻辑，需根据实际接口实现
    url = "https://api.example.com/data"
    try:
        response = requests.get(url, params={"id": id})
        response.raise_for_status()
        return response.json()
    except requests.RequestException as e:
        logger.error(f"请求失败 (ID: {id}): {e}")
        return {}


def extract_result(data, id):
    result = data.get('result', {})
    if not result:
        logger.warning(f"ID: {id} 无有效结果数据")
        return None, None, None

    # 安全获取嵌套数据
    holdingInfo = result.get('holdingInfo', {}) or {}
    relocateInfo = result.get('relocateInfo', {}) or {}

    # 处理holding_count
    holding_count = result.get('holdingCount', 0)
    if holding_count is None:
        holding_count = 0
    logger.info(f"{Combination_ids_to_name.get(id, ETF_ids_to_name.get(id, '未知ETF'))} 的持仓数量为: {holding_count}")

    # 处理调仓信息
    relocate_Info = []
    if relocateInfo.get('code'):
        current_ratio = relocateInfo.get('currentRatio', 0) or 0
        new_ratio = relocateInfo.get('newRatio', 0) or 0
        profitLossRate = relocateInfo.get('profitLossRate', 0) or 0

        relocate_Info.append({
            # '组合': ETF_ids_to_name.get(id, '未知ETF'),
            '组合': id_to_name.get(id, '未知ETF'),
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
            '组合': ETF_ids_to_name.get(id, '未知ETF'),
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
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    etf_relocation = [item for item in relocation_data if item['组合'] in ETF_ids_to_name.values()]
    combo_relocation = [item for item in relocation_data if item['组合'] in Combination_ids_to_name.values()]

    etf_holding = [item for item in holding_data if item['组合'] in ETF_ids_to_name.values()]
    combo_holding = [item for item in holding_data if item['组合'] in Combination_ids_to_name.values()]

    with pd.ExcelWriter(filename, engine='openpyxl') as writer:
        if etf_relocation:
            pd.DataFrame(etf_relocation).to_excel(writer, sheet_name='ETF调仓', index=False)
        if combo_relocation:
            pd.DataFrame(combo_relocation).to_excel(writer, sheet_name='组合调仓', index=False)
        if etf_holding:
            pd.DataFrame(etf_holding).to_excel(writer, sheet_name='ETF持仓', index=False)
        if combo_holding:
            pd.DataFrame(combo_holding).to_excel(writer, sheet_name='组合持仓', index=False)

    logger.info(f"数据已分类保存至 {filename}")

def main():
    all_relocation_data = []
    all_holding_data = []
    # for id in ETF_ids:
    for id in all_ids:
        result = send_request(id)
        # pprint(result)
        if not result or not result.get('result'):
            logger.warning(f"ID {id} 返回无效数据")
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
            logger.error(f"处理ID {id} 时发生异常: {str(e)}")
            continue

    df = pd.DataFrame(all_holding_data)
    print(df)

    save_path = Combination_holding_file
    save_results_to_xlsx(all_relocation_data, all_holding_data, save_path)

if __name__ == "__main__":
    main()
