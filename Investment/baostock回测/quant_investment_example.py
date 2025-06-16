import baostock as bs
import pandas as pd

def determine_market(code):
    """根据股票代码判断是深市还是沪市
    上海市场的A股股票代码以60开头，
    深圳市场的A股股票代码则以00或30开头
    ETF：
        上海证券交易所 (SH)：ETF代码以 51 开头。
        深圳证券交易所 (SZ)：ETF代码以 15、16 开头。
    REITs：
        上海证券交易所 (SH)：REITs代码以 50 开头。
        深圳证券交易所 (SZ)：REITs代码以 18 开头。"""
    if code.startswith(('00', '30', '15', '16', '18')):
        return 'sz'
    elif code.startswith(('60', '51', '50')):
        return 'sh'
    else:
        raise ValueError("无法识别的股票代码")

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('登录返回信息:' + lg.error_code)
print('登录返回error_msg:' + lg.error_msg)

# 输入股票代码
# stock_code = input("请输入股票代码: ")
stock_code = '600900'
market = determine_market(stock_code)
full_code = f"{market}.{stock_code}"
print(f"完整代码: {full_code}")

#### 获取历史K线数据 ####
# 详细指标参数，参见“历史行情指标参数”章节
rs = bs.query_history_k_data_plus(full_code,
                                  "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
                                  start_date='2024-12-01', end_date='2024-12-11',
                                  frequency="d", adjustflag="3")  # frequency="d"取日k线，adjustflag="3"默认不复权
print('查询返回 error_code:' + rs.error_code)
print('查询日线数据返回  error_msg:' + rs.error_msg)

#### 打印结果集 ####
data_list = []
while (rs.error_code == '0') & rs.next():
    # 获取一条记录，将记录合并在一起
    data_list.append(rs.get_row_data())
result = pd.DataFrame(data_list, columns=rs.fields)

# 将输出的列名从英文替换为中文
column_mapping = {
    'date': '日期',
    'code': '股票代码',
    'open': '开盘价',
    'high': '最高价',
    'low': '最低价',
    'close': '收盘价',
    'preclose': '前收盘价',
    'volume': '成交量',
    'amount': '成交额',
    'adjustflag': '复权状态',
    'turn': '换手率',
    'tradestatus': '交易状态',
    'pctChg': '涨跌幅',
    'peTTM': '市盈率TTM',
    'pbMRQ': '市净率MRQ',
    'psTTM': '市销率TTM',
    'pcfNcfTTM': '市现率TTM',
    'isST': '是否ST'
}

result.rename(columns=column_mapping, inplace=True)

#### 结果集输出到csv文件 ####
result.to_excel("bao_history_k_data.xlsx",  index=False)
print(result)

#### 登出系统 ####
bs.logout()
