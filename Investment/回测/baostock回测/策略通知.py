import baostock as bs
import pandas as pd
import numpy as np

#### 登陆系统 ####
lg = bs.login()
# 显示登陆返回信息
print('login respond error_code:' + lg.error_code)
print('login respond  error_msg:' + lg.error_msg)

#### 获取历史K线数据 ####
# 详细指标参数，参见“历史行情指标参数”章节
rs = bs.query_history_k_data_plus("sh.600000",
                                  "date,code,open,high,low,close,preclose,volume,amount,adjustflag,turn,tradestatus,pctChg,peTTM,pbMRQ,psTTM,pcfNcfTTM,isST",
                                  start_date='2017-06-01', end_date='2017-12-31',
                                  frequency="d", adjustflag="3")  # frequency="d"取日k线，adjustflag="3"默认不复权
print('query_history_k_data_plus respond error_code:' + rs.error_code)
print('query_history_k_data_plus respond  error_msg:' + rs.error_msg)

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

#### 检查并转换数据类型 ####
result['最高价'] = pd.to_numeric(result['最高价'], errors='coerce')
result['最低价'] = pd.to_numeric(result['最低价'], errors='coerce')
result['收盘价'] = pd.to_numeric(result['收盘价'], errors='coerce')
result['前收盘价'] = pd.to_numeric(result['前收盘价'], errors='coerce')

# 处理缺失值（可以选择填充或删除）
result.dropna(subset=['最高价', '最低价', '收盘价', '前收盘价'], inplace=True)

#### 计算技术指标 ####
# A1 := MAX(DYNAINFO(3), DYNAINFO(5));
# B1 := MIN(DYNAINFO(3), DYNAINFO(6));
# C1 := A1 - B1;
# 阻力 := B1 + C1 * 7 / 8, COLORGREEN;
# 支撑 := B1 + C1 * 0.5 / 8, COLORRED;
# 中线 := (支撑 + 阻力) / 2, COLORWHITE, POINTDOT;

result['A1'] = result[['最高价', '前收盘价']].max(axis=1)
result['B1'] = result[['最低价', '收盘价']].min(axis=1)
result['C1'] = result['A1'] - result['B1']
result['阻力'] = result['B1'] + result['C1'] * 7 / 8
result['支撑'] = result['B1'] + result['C1'] * 0.5 / 8
result['中线'] = (result['支撑'] + result['阻力']) / 2

# V11 := 3 * SMA((C - LLV(L, 55)) / (HHV(H, 55) - LLV(L, 55)) * 100, 5, 1) - 2 * SMA(SMA((C - LLV(L, 55)) / (HHV(H, 55) - LLV(L, 55)) * 100, 5, 1), 3, 1);
# 趋势 := EMA(V11, 3), LINETHICK1, COLORYELLOW;
# V12 := (趋势 - REF(趋势, 1)) / REF(趋势, 1) * 100;
# 准备买入 := STICKLINE(趋势 < 11, 趋势, 11, 5, 0), COLORRED;
# AA := (趋势 < 11) AND FILTER((趋势 <= 11), 15) AND C < 中线;
# BB0 := REF(趋势, 1) < 11 AND CROSS(趋势, 11) AND C < 中线;
# BB1 := REF(趋势, 1) < 11 AND REF(趋势, 1) > 6 AND CROSS(趋势, 11);
# BB2 := REF(趋势, 1) < 6 AND REF(趋势, 1) > 3 AND CROSS(趋势, 6);
# BB3 := REF(趋势, 1) < 3 AND REF(趋势, 1) > 1 AND CROSS(趋势, 3);
# BB4 := REF(趋势, 1) < 1 AND REF(趋势, 1) > 0 AND CROSS(趋势, 1);
# BB5 := REF(趋势, 1) < 0 AND CROSS(趋势, 0);
# BB := BB1 = 1 OR BB2 = 1 OR BB3 = 1 OR BB4 = 1 OR BB5 = 1;
# 下单买入 := STICKLINE(BB = 1 AND C < 中线, 11, 52, 1, 0), COLORRED;
# DRAWICON(BB = 1 AND C < 中线, 55, 1);
# DRAWTEXT(BB0, 60, '抄底'), COLORRED;
# DRAWTEXT(AA, 16, '超卖见底'), , COLORWHITE;
# 准备卖出 := STICKLINE(趋势 > 89, 趋势, 89, 5, 0), COLORGREEN;
# CC := (趋势 > 89) AND FILTER((趋势 > 89), 15) AND C > 中线;
# DD0 := REF(趋势, 1) > 89 AND CROSS(89, 趋势) AND C > 中线;
# DD1 := REF(趋势, 1) > 89 AND REF(趋势, 1) < 94 AND CROSS(89, 趋势);
# DD2 := REF(趋势, 1) > 94 AND REF(趋势, 1) < 97 AND CROSS(94, 趋势);
# DD3 := REF(趋势, 1) > 97 AND REF(趋势, 1) > 99 AND CROSS(97, 趋势);
# DD4 := REF(趋势, 1) > 99 AND REF(趋势, 1) < 100 AND CROSS(99, 趋势);
# DD5 := REF(趋势, 1) > 100 AND CROSS(100, 趋势);
# DD := DD1 = 1 OR DD2 = 1 OR DD3 = 1 OR DD4 = 1 OR DD5 = 1;
# 下单卖出 := STICKLINE(DD = 1 AND C > 中线, 89, 49, 1, 0), COLORGREEN;
# DRAWICON(DD = 1 AND C > 中线, 55, 2);
# DRAWTEXT(DD0, 40, '逃顶'), COLORGREEN;
# DRAWTEXT(CC, 84, '超买见顶'), , COLORWHITE;
# 顶 := 89, COLORGREEN;
# 底 := 11, COLORRED;
# 中 := 50, POINTDOT, COLORWHITE;
# DRAWTEXT(ISLASTBAR, 顶, '顶'), COLORGREEN;
# DRAWTEXT(ISLASTBAR, 底, '底'), COLORRED;
# DRAWTEXT(ISLASTBAR, 中, '中'), COLORWHITE;

def sma(series, window):
    return series.rolling(window=window).mean()

def ema(series, span):
    return series.ewm(span=span, adjust=False).mean()

result['LLV_L_55'] = result['最低价'].rolling(window=55).min()
result['HHV_H_55'] = result['最高价'].rolling(window=55).max()
result['V11'] = 3 * sma((result['收盘价'] - result['LLV_L_55']) / (result['HHV_H_55'] - result['LLV_L_55']) * 100, 5) - \
              2 * sma(sma((result['收盘价'] - result['LLV_L_55']) / (result['HHV_H_55'] - result['LLV_L_55']) * 100, 5), 3)
result['趋势'] = ema(result['V11'], 3)

result['准备买入'] = (result['趋势'] < 11) & (result['收盘价'] < result['中线'])
result['AA'] = result['准备买入'] & result['趋势'].rolling(window=15).apply(lambda x: all(x <= 11), raw=True)
result['BB0'] = (result['趋势'].shift(1) < 11) & (result['趋势'] > 11) & (result['收盘价'] < result['中线'])
result['BB1'] = (result['趋势'].shift(1) < 11) & (result['趋势'].shift(1) > 6) & (result['趋势'] > 11)
result['BB2'] = (result['趋势'].shift(1) < 6) & (result['趋势'].shift(1) > 3) & (result['趋势'] > 6)
result['BB3'] = (result['趋势'].shift(1) < 3) & (result['趋势'].shift(1) > 1) & (result['趋势'] > 3)
result['BB4'] = (result['趋势'].shift(1) < 1) & (result['趋势'].shift(1) > 0) & (result['趋势'] > 1)
result['BB5'] = (result['趋势'].shift(1) < 0) & (result['趋势'] > 0)
result['BB'] = result[['BB1', 'BB2', 'BB3', 'BB4', 'BB5']].any(axis=1)
result['下单买入'] = result['BB'] & (result['收盘价'] < result['中线'])

result['准备卖出'] = (result['趋势'] > 89) & (result['收盘价'] > result['中线'])
result['CC'] = result['准备卖出'] & result['趋势'].rolling(window=15).apply(lambda x: all(x >= 89), raw=True)
result['DD0'] = (result['趋势'].shift(1) > 89) & (result['趋势'] < 89) & (result['收盘价'] > result['中线'])
result['DD1'] = (result['趋势'].shift(1) > 89) & (result['趋势'].shift(1) < 94) & (result['趋势'] < 89)
result['DD2'] = (result['趋势'].shift(1) > 94) & (result['趋势'].shift(1) < 97) & (result['趋势'] < 94)
result['DD3'] = (result['趋势'].shift(1) > 97) & (result['趋势'].shift(1) > 99) & (result['趋势'] < 97)
result['DD4'] = (result['趋势'].shift(1) > 99) & (result['趋势'].shift(1) < 100) & (result['趋势'] < 99)
result['DD5'] = (result['趋势'].shift(1) > 100) & (result['趋势'] < 100)
result['DD'] = result[['DD1', 'DD2', 'DD3', 'DD4', 'DD5']].any(axis=1)
result['下单卖出'] = result['DD'] & (result['收盘价'] > result['中线'])

#### 输出结果集 ####
result.to_excel("bao_history_k_data_with_signals.xlsx", index=False)
print(result)

#### 提示买卖信号 ####
for index, row in result.iterrows():
    if row['下单买入']:
        print(f"买入信号: 日期 {row['日期']}，收盘价 {row['收盘价']}")
    elif row['下单卖出']:
        print(f"卖出信号: 日期 {row['日期']}，收盘价 {row['收盘价']}")

#### 登出系统 ####
bs.logout()
