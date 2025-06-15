import pandas as pd

def fetch_data(source='lhb'):
    if source == 'lhb':
        return pd.read_excel("龙虎榜综合分析.xlsx")
    elif source == 'zt_pool':
        return pd.DataFrame({'stock_code': ['000001', '600000'], 'price': [10.0, 15.0]})
    elif source == 'lb_pool':
        return pd.DataFrame({'stock_code': ['000001'], 'zt_days': [3]})
    else:
        return pd.DataFrame()

def generate_trading_signals(df_lhb, df_zt, df_lb):
    # 合并数据
    df = pd.merge(df_lhb, df_zt, on='stock_code', how='left')
    df = pd.merge(df, df_lb, on='stock_code', how='left')

    # 定义因子权重
    df['hot_score'] = 100 / (df['hot_rank'].fillna(999) + 1)
    df['zt_strength'] = df['zt_days'] * 10
    df['org_net_value'] = df['org_net_value'].fillna(0)
    df['hot_money_net_value'] = df['hot_money_net_value'].fillna(0)

    # 总分计算
    df['final_score'] = (
        df['hot_score'] * 0.3 +
        df['zt_strength'] * 0.2 +
        df['org_net_value'] * 0.25 +
        df['hot_money_net_value'] * 0.25
    )

    # 筛选得分前20的股票作为候选股
    candidates = df.sort_values(by='final_score', ascending=False).head(20)
    return candidates[['stock_name', 'stock_code', 'final_score']]
