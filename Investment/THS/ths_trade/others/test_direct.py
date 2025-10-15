#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
直接测试脚本：不通过HTTP服务，直接调用核心模块获取川财证券的持仓数据
"""
import os
import sys
import time
import pandas as pd

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("===== ths_trade直接测试工具 =====\n")
    print("正在尝试直接调用核心模块获取持仓数据...")
    
    try:
        # 直接导入核心交易执行模块
        from applications.trade.Exec_Auto_Trade import exec_run
        print("成功导入exec_run模块")
        
        # 创建一个获取持仓的请求对象
        request_item = {
            "operate": "get_position"
        }
        
        print("\n正在调用get_position方法获取持仓数据...")
        print("这将直接连接到已运行的同花顺交易软件")
        
        # 调用exec_run方法获取持仓数据
        position_data = exec_run(request_item)
        
        if position_data is not None:
            print("\n✓ 成功获取持仓数据！")
            print("\n持仓数据详情：")
            
            # 检查返回的数据类型
            if isinstance(position_data, pd.DataFrame):
                print(f"数据类型：pandas DataFrame")
                print(f"数据行数：{len(position_data)}")
                print(f"\n数据列名：")
                for col in position_data.columns:
                    print(f"  - {col}")
                
                print("\n持仓数据内容：")
                print(position_data.to_string(index=False))
                
                # 保存数据到文件
                output_file = "position_data.csv"
                position_data.to_csv(output_file, index=False, encoding='utf-8-sig')
                print(f"\n数据已保存到：{output_file}")
            else:
                print(f"数据类型：{type(position_data)}")
                print(f"数据内容：{position_data}")
        else:
            print("\n✗ 获取持仓数据失败，返回None")
            
    except ImportError as e:
        print(f"\n✗ 导入模块失败: {e}")
        print("请检查项目结构和依赖是否正确")
    except Exception as e:
        print(f"\n✗ 执行过程中发生错误: {e}")
        import traceback
        print("\n详细错误信息：")
        traceback.print_exc()
    finally:
        print("\n测试完成！")
        input("按Enter键退出...")

if __name__ == "__main__":
    main()