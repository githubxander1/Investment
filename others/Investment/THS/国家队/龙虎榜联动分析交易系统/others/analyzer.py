import pandas as pd
import pandas as pd

def multi_factor_scoring(df_lhb, df_zt, df_lb):
    # 合并数据
    df = pd.merge(df_lhb, df_zt, on='stock_code', how='left')
    df = pd.merge(df, df_lb, on='stock_code', how='left')

    # 因子加权打分
    df['hot_score'] = 100 / (df['hot_rank'].fillna(999) + 1)
    df['zt_strength'] = df['zt_days'].fillna(0) * 10
    df['org_net_value'] = df['机构净买'].fillna(0)
    df['hot_money_net_value'] = df['游资净买'].fillna(0)

    # 权重分配
    df['score'] = (
        df['hot_score'] * 0.3 +
        df['zt_strength'] * 0.2 +
        df['org_net_value'] * 0.25 +
        df['hot_money_net_value'] * 0.25
    )

    # 排序取前20
    top_stocks = df.sort_values(by='score', ascending=False).head(20)
    return top_stocks[['股票名称', '股票代码', 'score']]

def analyze_concepts(db_path='stock_data.db'):
    query = "SELECT date, concept FROM lhb_data WHERE date='2025-06-13'"
    df = pd.read_sql_query(query, sqlite3.connect(db_path))

    # 拆分多个概念为单独行
    df_expanded = df.assign(concept=df['concept'].str.split(' + ')).explode('concept')

    # 统计出现次数
    concept_counts = df_expanded['concept'].value_counts().reset_index()
    concept_counts.columns = ['concept', 'count']

    return concept_counts.head(10)

print(analyze_concepts())
