#notifier.py
def send_notification(message, title="系统通知"):
    """发送通知"""
    # 这里可以实现具体的推送逻辑
    print(f"[{title}] {message}")

def format_notification(dataframe, count, detail_limit=5):
    """格式化通知内容"""
    if dataframe.empty:
        return f"{count} 条更新：\n暂无详细信息"

    summary = f"{count} 条更新：\n"
    details = dataframe.head(detail_limit).to_string(index=False)
    return summary + details
