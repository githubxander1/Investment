
def normalize_time(time_str):
    """统一时间格式为 YYYY-MM-DD HH:MM"""
    if not time_str or time_str == 'N/A':
        return ''

    try:
        # 处理 float 类型（如 20250509.0）
        if isinstance(time_str, float) and not pd.isna(time_str):
            time_str = str(int(time_str))
        elif isinstance(time_str, str) and '.' in time_str:
            time_str = time_str.split('.')[0]  # 去掉小数点后内容

        time_str = " ".join(str(time_str).split())  # 清除多余空格

        # 处理纯数字日期（如 20250509）
        if len(time_str) == 8 and time_str.isdigit():
            return f"{time_str[:4]}-{time_str[4:6]}-{time_str[6:8]}"

        # 如果包含秒字段，去掉秒部分
        if len(time_str.split()) > 1:
            date_part, time_part = time_str.split(" ", 1)
            time_part = ":".join(time_part.split(":")[:2])  # 只取小时和分钟
            return f"{date_part} {time_part}"
        else:
            return time_str
    except Exception as e:
        print(f"时间标准化失败: {e}")
        return ''