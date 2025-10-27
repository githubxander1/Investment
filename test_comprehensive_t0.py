#!/usr/bin/env python3
# 测试脚本：验证综合体T0策略的时间显示修复

import sys
import os
import shutil
from datetime import datetime

# 添加项目路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from Investment.T0.indicators.comprehensive_t0_strategy import plot_comprehensive_t0, get_fenshi_data

def clear_cache(stock_code, date):
    """清除指定股票的缓存文件"""
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 清除T0目录的缓存
    cache_dir1 = os.path.join(project_root, 'Investment', 'T0', 'cache', 'fenshi_data')
    cache_file1 = os.path.join(cache_dir1, f'{stock_code}_{date}_fenshi.csv')
    if os.path.exists(cache_file1):
        os.remove(cache_file1)
        print(f"已删除缓存文件: {cache_file1}")
    
    # 清除T0_Optimized目录的缓存
    cache_dir2 = os.path.join(project_root, 'Investment', 'T0_Optimized', 'cache', 'fenshi_data')
    cache_file2 = os.path.join(cache_dir2, f'{stock_code}_{date}_fenshi.csv')
    if os.path.exists(cache_file2):
        os.remove(cache_file2)
        print(f"已删除缓存文件: {cache_file2}")

def main():
    print("=== 测试综合体T0策略时间显示 ===")
    
    # 获取当前时间
    now = datetime.now()
    today = now.strftime('%Y-%m-%d')
    today_date_format = now.strftime('%Y%m%d')
    current_time = now.strftime('%H:%M:%S')
    current_hour_minute = now.strftime('%H:%M')
    
    print(f"当前日期: {today}")
    print(f"当前时间: {current_time}")
    print(f"当前系统时间应该只生成到 {current_hour_minute} 的数据")
    print(f"注意：由于当前是上午10:30左右，不应该生成任何下午的数据")
    
    # 测试股票代码
    stock_code = "600030"
    
    try:
        # 清除缓存
        print("\n清除缓存文件:")
        clear_cache(stock_code, today_date_format)
        
        # 强制重新生成数据 - 创建一个临时脚本来直接调用并捕获完整输出
        temp_script = """
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Investment.T0.indicators.comprehensive_t0_strategy import get_fenshi_data
from datetime import datetime

# 获取当前时间
now = datetime.now()
today_date_format = now.strftime('%Y%m%d')
stock_code = "600030"

# 清除缓存
cache_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'Investment', 'T0', 'cache', 'fenshi_data')
cache_file = os.path.join(cache_dir, f'{stock_code}_{today_date_format}_fenshi.csv')
if os.path.exists(cache_file):
    os.remove(cache_file)
    print(f"已删除缓存文件: {cache_file}")

# 生成新数据
print("\n开始生成新数据...")
df = get_fenshi_data(stock_code, today_date_format)

# 输出数据信息
print("\n=== 数据验证结果 ===")
print(f"数据行数: {len(df)}")
first_time = df['时间'].iloc[0]
last_time = df['时间'].iloc[-1]
print(f"生成的数据时间范围: {first_time} 到 {last_time}")

# 检查是否包含下午的数据
has_afternoon_data = False
for time_str in df['时间']:
    time_str = str(time_str)
    if ':' in time_str:
        hour = int(time_str.split(':')[0])
        if hour >= 13:
            has_afternoon_data = True
            print(f"发现下午数据: {time_str}")
            break

if not has_afternoon_data:
    print("✅ 验证成功：没有生成任何下午的数据")
else:
    print("❌ 验证失败：生成了下午的数据")

print("\n数据验证完成")
"""
        
        # 写入临时脚本
        temp_script_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'temp_verify_data.py')
        with open(temp_script_path, 'w', encoding='utf-8') as f:
            f.write(temp_script)
        
        print("\n运行临时验证脚本:")
        os.system(f'python "{temp_script_path}"')
        
        # 删除临时脚本
        os.remove(temp_script_path)
        
        # 调用绘图函数
        print("\n调用plot_comprehensive_t0函数生成图表:")
        chart_path = plot_comprehensive_t0(
            stock_code=stock_code,
            trade_date=today
        )
        
        print(f"\n✅ 测试成功！图表已保存至: {chart_path}")
        print(f"✅ 生成的数据应该只包含到当前时间 {current_hour_minute} 的分时数据，不包含下午数据")
        
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
