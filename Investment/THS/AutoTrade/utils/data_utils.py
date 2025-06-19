def standardize_dataframe(df):
    """标准化DataFrame格式"""
    # 列对齐
    # df = df.reindex(columns=EXPECTED_COLUMNS, fill_value=None)

    # 格式标准化
    if not df.empty:
        # 清理代码字段
        df['代码'] = df['代码'].astype(str).str.zfill(6)

        # 清理时间字段
        df['时间'] = df['时间'].astype(str).apply(normalize_time)
        df['时间'] = df['时间'].replace('nan', '').replace('', None)

    return df