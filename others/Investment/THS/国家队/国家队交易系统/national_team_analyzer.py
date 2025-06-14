import pandas as pd

def national_team_scoring(filename="国家队持股.xlsx"):
    """
    对国家队持股数据进行多因子评分选股
    """
    # 读取 Excel 文件中所有 sheet
    sheets = pd.read_excel(filename, sheet_name=None)

    # 合并所有 sheet 数据
    combined_df = pd.DataFrame()
    for sheet_name, df in sheets.items():
        df['source'] = sheet_name  # 添加来源标识
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    # 处理缺失值
    combined_df['总持股比例'] = combined_df['总持股比例'].fillna(0).astype(float)
    combined_df['社保'] = combined_df['社保'].fillna(0).astype(int)
    combined_df['养老金'] = combined_df['养老金'].fillna(0).astype(int)
    combined_df['证金'] = combined_df['证金'].fillna(0).astype(int)
    combined_df['汇金'] = combined_df['汇金'].fillna(0).astype(int)

    # 构造因子
    combined_df['duration_score'] = combined_df['source'].map({
        '持有最久': 1.0,
        '最新公布': 0.8,
        '增持最多': 0.7,
        '持有最多': 0.6
    }).fillna(0.5)

    combined_df['holder_count'] = (
        combined_df[['社保', '养老金', '证金', '汇金']].apply(lambda x: x > 0).sum(axis=1)
    ).astype(float)

    combined_df['total_scale'] = combined_df['总持股比例'].astype(float)

    # 权重分配
    combined_df['score'] = (
        combined_df['duration_score'] * 0.3 +
        combined_df['holder_count'] * 0.2 +
        combined_df['total_scale'] * 0.5
    )

    # 排序并选取前20名
    top_stocks = combined_df.sort_values(by='score', ascending=False).head(20)

    return top_stocks[['股票代码', '股票名称', 'score']]
