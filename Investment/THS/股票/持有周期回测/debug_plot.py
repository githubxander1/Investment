import os
import pandas as pd
import matplotlib.pyplot as plt

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False

def load_stock_data(stock_name, data_dir):
    """加载指定股票的历史价格数据"""
    file_path = os.path.join(data_dir, f"{stock_name}.csv")
    if os.path.exists(file_path):
        df = pd.read_csv(file_path, encoding='utf-8-sig', parse_dates=['日期'])
        df.set_index('日期', inplace=True)
        return df
    else:
        print(f"⚠️ 文件不存在: {file_path}")
        return None

def plot_price_trend(stock_name, df, output_path):
    """绘制股票价格走势图"""
    if df is not None and not df.empty:
        plt.figure(figsize=(12, 6))
        plt.plot(df.index, df['收盘'], color='green', linewidth=1)
        plt.title(f'{stock_name} - 价格走势')
        plt.xlabel('日期')
        plt.ylabel('价格')
        plt.grid(True)

        # 保存图表
        chart_path = os.path.join(output_path, f"{stock_name}_price_trend.png")
        plt.savefig(chart_path)
        plt.close()
        print(f"📈 价格走势图已保存至: {chart_path}")
    else:
        print("无价格数据可绘制")

if __name__ == '__main__':
    # 设置路径
    data_dir = 'stock_data/双峰形态/2025-08-13'
    output_path = 'debug_plots'

    # 确保输出目录存在
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    # 指定股票名称
    # stock_name = '000011深物业A'
    stock_name = '601869长飞光纤'

    # 加载股票数据
    df = load_stock_data(stock_name, data_dir)

    # 绘制价格走势图
    plot_price_trend(stock_name, df, output_path)
