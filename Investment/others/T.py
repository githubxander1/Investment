import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import os
from datetime import datetime

# 设置中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'WenQuanYi Micro Hei', 'Heiti TC']
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题


class StockPriceChart:
    def __init__(self):
        # 初始化图表配置
        self.fig = None
        self.ax = None
        self.has_avg_price = False

    def load_data(self, file_path):
        """
        加载CSV文件数据

        参数:
            file_path: CSV文件路径

        返回:
            加载好的数据DataFrame
        """
        if not os.path.exists(file_path):
            print(f"错误: 文件 '{file_path}' 不存在")
            return None

        try:
            # 读取CSV文件
            df = pd.read_csv(file_path)

            # 检查必要的列是否存在
            required_columns = ['时间', '收盘']
            for col in required_columns:
                if col not in df.columns:
                    print(f"错误: 文件中缺少必要的列 '{col}'")
                    return None

            # 检查均价列是否存在
            self.has_avg_price = '均价' in df.columns

            # 转换时间列为datetime类型
            try:
                df['时间'] = pd.to_datetime(df['时间'])
            except Exception as e:
                print(f"错误: 时间列格式不正确，无法转换为datetime类型: {e}")
                return None

            # 确保收盘列为数值类型
            df['收盘'] = pd.to_numeric(df['收盘'], errors='coerce')

            # 确保均价列为数值类型(如果存在)
            if self.has_avg_price:
                df['均价'] = pd.to_numeric(df['均价'], errors='coerce')

            # 去除空值
            df = df.dropna(subset=['时间', '收盘'])

            # 按时间排序
            df = df.sort_values('时间')

            return df
        except Exception as e:
            print(f"错误: 加载文件时发生异常: {e}")
            return None

    def plot_chart(self, df, file_path=None):
        """
        绘制价格曲线图表

        参数:
            df: 包含时间和收盘价格的数据DataFrame
            file_path: 可选，用于在图表标题中显示文件名
        """
        if df is None or df.empty:
            print("错误: 没有数据可绘制")
            return False

        try:
            # 创建图表
            self.fig, self.ax = plt.subplots(figsize=(12, 6))

            # 使用数据点索引作为x轴坐标，确保所有数据点之间的距离均匀
            x_values = list(range(len(df)))

            # 绘制收盘价曲线，严格按照文件中的实际时间点连接
            self.ax.plot(x_values, df['收盘'], marker='', linestyle='-', color='blue', linewidth=2, label='收盘价')

            # 绘制均价线(如果数据中存在均价列)
            if self.has_avg_price and not df['均价'].isna().all():
                self.ax.plot(x_values, df['均价'], marker='', linestyle='-', color='yellow', linewidth=1.5,
                             label='均价线')

            # 设置图表标题
            title = '分时图'
            if file_path:
                file_name = os.path.basename(file_path)
                stock_code = os.path.splitext(file_name)[0]
                title = f'{stock_code} 分时图'
            self.ax.set_title(title, fontsize=16, fontweight='bold')

            # 设置坐标轴标签
            self.ax.set_xlabel('时间', fontsize=12)
            self.ax.set_ylabel('收盘价', fontsize=12)

            # 严格按照CSV文件中的实际时间点设置x轴刻度，不添加CSV中不存在的时间点
            # 只选择部分时间点作为刻度，避免标签过多重叠
            total_points = len(df)
            if total_points > 100:
                # 数据点非常多时，间隔选择更多点
                step = max(1, total_points // 20)
            elif total_points > 50:
                # 数据点较多时，间隔选择一些点
                step = max(1, total_points // 15)
            elif total_points > 20:
                # 数据点适中时，间隔选择较少点
                step = max(1, total_points // 10)
            else:
                # 数据点较少时，显示所有点
                step = 1

            # 选择要显示的时间点和对应的索引位置
            selected_indices = list(range(0, total_points, step))
            selected_times = df['时间'].iloc[selected_indices]

            # 设置x轴刻度为数据点索引位置，但显示对应的时间标签
            self.ax.set_xticks(selected_indices)
            self.ax.set_xticklabels([t.strftime('%m-%d %H:%M') for t in selected_times])

            # 自动旋转x轴标签以避免重叠
            plt.xticks(rotation=45)

            # 添加网格线
            self.ax.grid(True, linestyle='--', alpha=0.7)

            # 添加图例
            self.ax.legend(loc='best')

            # 调整布局
            plt.tight_layout()

            return True
        except Exception as e:
            print(f"错误: 绘制图表时发生异常: {e}")
            return False

    def show_chart(self):
        """显示图表"""
        if self.fig:
            plt.show()

    def save_chart(self, output_path='stock_price_chart.png'):
        """
        保存图表为图片文件

        参数:
            output_path: 输出文件路径
        """
        if self.fig:
            try:
                self.fig.savefig(output_path, dpi=300, bbox_inches='tight')
                print(f"图表已保存到: {output_path}")
                return True
            except Exception as e:
                print(f"错误: 保存图表时发生异常: {e}")
                return False
        return False

    def analyze_data(self, df):
        """
        对数据进行简单分析

        参数:
            df: 包含时间和收盘价格的数据DataFrame
        """
        if df is None or df.empty:
            return

        # 计算基本统计信息
        start_date = df['时间'].min().strftime('%Y-%m-%d')
        end_date = df['时间'].max().strftime('%Y-%m-%d')
        start_price = df['收盘'].iloc[0]
        end_price = df['收盘'].iloc[-1]
        max_price = df['收盘'].max()
        min_price = df['收盘'].min()
        price_change = end_price - start_price
        percent_change = (price_change / start_price) * 100

        print("\n===== 数据统计分析 =====")
        print(f"数据范围: {start_date} 至 {end_date}")
        print(f"起始价格: {start_price:.2f}")
        print(f"结束价格: {end_price:.2f}")
        print(f"最高价格: {max_price:.2f}")
        print(f"最低价格: {min_price:.2f}")
        print(f"价格变化: {price_change:.2f} ({percent_change:.2f}%)")
        print(f"数据点数: {len(df)}")


if __name__ == "__main__":
    # 创建StockPriceChart实例
    chart = StockPriceChart()

    # 自动使用默认的CSV文件路径
    file_path = r"/Investment/T0/stock_data/601728_中国电信.csv"

    # 加载数据
    print(f"正在加载文件: {file_path}")
    data = chart.load_data(file_path)

    if data is not None and not data.empty:
        # 分析数据
        chart.analyze_data(data)

        # 绘制图表
        print("正在绘制价格曲线图表...")
        if chart.plot_chart(data, file_path):
            # 保存图表
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            stock_code = os.path.splitext(os.path.basename(file_path))[0]
            output_file = f"{stock_code}_price_chart_{timestamp}.png"
            chart.save_chart(output_file)

            # 显示图表
            print("正在显示图表...")
            chart.show_chart()
    else:
        print("无法加载数据或数据为空，程序退出。")