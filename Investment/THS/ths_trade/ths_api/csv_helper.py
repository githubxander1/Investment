"""
CSV工具接口
封装applications.tool.CSV_Helper中的功能
"""

from applications.tool.CSV_Helper import CSVHelper


def get_csv_data(path=None):
    """
    获取CSV数据
    
    Args:
        path (str, optional): CSV文件路径，默认使用配置中的路径
        
    Returns:
        pandas.DataFrame: CSV数据
    """
    csv_helper = CSVHelper()
    if path:
        # 注意：原CSVHelper类中的getCVS方法不支持path参数，这里仅为接口一致性
        return csv_helper.getCVS()
    else:
        return csv_helper.getCVS()


def save_csv_data(df, path=None):
    """
    保存数据到CSV文件
    
    Args:
        df (pandas.DataFrame): 要保存的数据
        path (str, optional): CSV文件路径，默认使用配置中的路径
    """
    csv_helper = CSVHelper()
    if path:
        # 注意：原CSVHelper类中的saveCSV方法不支持path参数，这里仅为接口一致性
        csv_helper.saveCSV(df)
    else:
        csv_helper.saveCSV(df)


def clear_csv_data(path=None):
    """
    清空CSV文件数据
    
    Args:
        path (str, optional): CSV文件路径，默认使用配置中的路径
    """
    csv_helper = CSVHelper()
    if path:
        # 注意：原CSVHelper类中的clearCSV方法不支持path参数，这里仅为接口一致性
        csv_helper.clearCSV()
    else:
        csv_helper.clearCSV()


def add_csv_data(df, new_row):
    """
    向CSV数据中添加新行
    
    Args:
        df (pandas.DataFrame): 原始数据
        new_row (pandas.DataFrame): 要添加的新行数据
        
    Returns:
        pandas.DataFrame: 添加新行后的数据
    """
    csv_helper = CSVHelper()
    return csv_helper.addCSV(df, new_row)