import tushare as ts

# 设置Tushare Pro的API Token
ts.set_token('2e9a7a0827b4c655aa6c267dc00484c6e76ab1022b5717092b44573e')

# 初始化Tushare API
pro = ts.pro_api()

def get_index_components(index_code):
    """
    获取指定指数的成分股
    :param index_code: 指数代码
    :return: 成分股数据框
    """
    df = pro.index_weight(index_code=index_code)
    return df

# 示例：获取159819和562500的成分股
index_codes = ['159819', '562500']

for code in index_codes:
    components = get_index_components(code)
    print(f"指数 {code} 的成分股:")
    print(components)
