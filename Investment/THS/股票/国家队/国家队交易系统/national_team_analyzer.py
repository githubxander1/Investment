import pandas as pd

def national_team_scoring(filename="国家队持股.xlsx"):
    """
    对国家队持股数据进行多因子评分选股
    """
    # 读取 Excel 文件中所有 sheet
    sheets = pd.read_excel(filename, sheet_name=None)

    # 合并所有 sheet stock_data
    combined_df = pd.DataFrame()
    for sheet_name, df in sheets.items():
        df['source'] = sheet_name  # 添加来源标识
        combined_df = pd.concat([combined_df, df], ignore_index=True)

    # 处理缺失值
    combined_df['总持股比例'] = combined_df['总持股比例'].fillna(0).astype(float)

    # 统一处理 '社保'、'养老金'、'证金' 和 '汇金' 列
    columns_to_process = ['社保', '养老金', '证金', '汇金']
    for col in columns_to_process:
        combined_df[col] = combined_df[col].apply(lambda x: 1 if x == col else 0)

    # 统一股票代码格式
    combined_df['股票代码'] = combined_df['股票代码'].apply(lambda x: str(x).zfill(6))

    # 构造因子
    combined_df['duration_score'] = combined_df['source'].map({
        '持有最久': 1.0,
        '最新公布': 0.8,
        '增持最多': 0.7,
        '持有最多': 0.6
    }).fillna(0.5)

    combined_df['holder_count'] = (
        combined_df[columns_to_process].apply(lambda x: x > 0).sum(axis=1)
    ).astype(float)

    combined_df['total_scale'] = combined_df['总持股比例'].astype(float)

    # 权重分配
    combined_df['score'] = (
        combined_df['duration_score'] * 0.3 +
        combined_df['holder_count'] * 0.2 +
        combined_df['total_scale'] * 0.5
    )

    # 排序并选取前5名（排除ST股票）
    top_stocks = combined_df[
        ~combined_df['股票名称'].str.contains('ST')
    ].sort_values(by='score', ascending=False).head(5)

    return top_stocks[['股票代码', '股票名称', 'score']]
