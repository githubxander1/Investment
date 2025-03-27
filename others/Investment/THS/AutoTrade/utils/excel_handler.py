import os
from pprint import pprint

import openpyxl
import pandas as pd

from others.Investment.THS.AutoTrade.utils.scheduler import logger

def read_excel(file_path, sheet_name):
    try:
        # 读取Excel文件
        if os.path.exists(file_path):
            df = pd.read_excel(file_path, sheet_name=sheet_name)
            pprint(f"成功读取文件: {file_path}, 表名称: {sheet_name}")
            return df
        else:
            logger.warning(f"文件 {file_path} 不存在，返回空DataFrame")
            return pd.DataFrame()
    except Exception as e:
        logger.error(f"读取文件失败: {e}")
        return pd.DataFrame()

def save_to_excel(df, filename, sheet_name, index=False):
    """将DataFrame保存到Excel文件中"""
    try:
        # 检查文件是否存在
        if os.path.exists(filename):
            # 文件存在，追加模式
            with pd.ExcelWriter(filename, engine='openpyxl', mode='a', if_sheet_exists='replace') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=index)
                pprint(f"成功保存数据到文件: {filename}, 表名称: {sheet_name}")
        else:
            # 文件不存在，创建新文件
            with pd.ExcelWriter(filename, engine='openpyxl') as writer:
                df.to_excel(writer, sheet_name=sheet_name, index=index)
                pprint(f"文件不存在，新建文件成功: {filename}, 表名称: {sheet_name}")
    except Exception as e:
        logger.error(f"保存数据到文件失败: {e}")

def clear_sheet(filename, sheet_name):
    """清空指定Excel文件中的指定表格"""
    try:
        # 检查文件是否存在
        if os.path.exists(filename):
            wb = openpyxl.load_workbook(filename)
            if sheet_name in wb.sheetnames:
                ws = wb[sheet_name]
                # 删除所有行
                ws.delete_rows(1, ws.max_row)
                wb.save(filename)
                pprint(f"成功清空表格: {sheet_name} 文件: {filename}")
            else:
                logger.warning(f"表格 {sheet_name} 不存在于文件: {filename}")
        else:
            logger.warning(f"文件 {filename} 不存在，无需清空")
    except Exception as e:
        logger.error(f"清空表格失败: {e}")
