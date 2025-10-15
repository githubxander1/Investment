import uiautomator2
import pandas as pd
import os
import json
from datetime import datetime

d = uiautomator2.connect()

print(d.info)
# 打印dump信息
xml = d.dump_hierarchy()
print(xml)
# 保存到 文件
with open('dump.xml', 'w', encoding='utf-8') as f:
    f.write(xml)

def send_instruction_to_autoglm(instruction):
    """将指令发送到AutoGLM输入框"""
    # 在输入框里输入指令
    input_box = d(resourceId="", className="android.widget.EditText")
    input_box.click()
    input_box.clear_text()
    input_box.send_keys(instruction)
    print(f'输入指令到输入框: {instruction}')

    # 点击发送按钮
    # 修复：使用正确的uiautomator2 XPath语法并添加异常处理
    try:
        send_button = d.xpath('//*[@content-desc="action_icon"]')
        if send_button.exists:
            send_button.click()
            print('点击发送按钮')
        else:
            print('未找到发送按钮')
    except Exception as e:
        print(f'点击发送按钮时出错: {e}')

def format_trade_instruction(account_name, operation, stock_name, volume):
    """格式化交易指令"""
    # 格式：打开同花顺，用xx证券执行xx（买入或卖出）xxx(股票），xx股
    instruction = f"打开同花顺，用{account_name}执行{operation}{stock_name}{volume}股"
    return instruction

def execute_trade_via_autoglm(account_name, operation, stock_name, volume):
    """通过AutoGLM执行交易指令"""
    instruction = format_trade_instruction(account_name, operation, stock_name, volume)
    send_instruction_to_autoglm(instruction)
    
    # 记录执行的指令到文件
    log_entry = {
        "timestamp": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "account": account_name,
        "operation": operation,
        "stock": stock_name,
        "volume": volume,
        "instruction": instruction
    }
    
    # 写入日志文件
    log_file = "autoglm_trade_log.json"
    logs = []
    if os.path.exists(log_file):
        with open(log_file, 'r', encoding='utf-8') as f:
            try:
                logs = json.load(f)
            except:
                logs = []
    
    logs.append(log_entry)
    with open(log_file, 'w', encoding='utf-8') as f:
        json.dump(logs, f, ensure_ascii=False, indent=2)

# 监听交易指令文件并执行
def listen_for_trade_instructions():
    """监听交易指令文件并执行"""
    instruction_file = "trade_instructions.json"
    
    if os.path.exists(instruction_file):
        try:
            with open(instruction_file, 'r', encoding='utf-8') as f:
                instructions = json.load(f)
            
            # 执行每条指令
            for instruction in instructions:
                execute_trade_via_autoglm(
                    instruction["account"],
                    instruction["operation"],
                    instruction["stock"],
                    instruction["volume"]
                )
            
            # 执行完后删除指令文件
            os.remove(instruction_file)
            print(f"已执行{len(instructions)}条交易指令并删除指令文件")
            
        except Exception as e:
            print(f"处理交易指令文件时出错: {e}")

if __name__ == "__main__":
    # 监听并执行交易指令
    listen_for_trade_instructions()
    
    # 示例交易操作（如果需要手动测试）
    # sample_operations = [
    #     {"account": "中泰证券", "operation": "买入", "stock": "格力电器", "volume": 100},
    #     {"account": "中泰证券", "operation": "卖出", "stock": "美的集团", "volume": 200}
    # ]
    # 
    # # 将交易操作发送给AutoGLM执行
    # for op in sample_operations:
    #     execute_trade_via_autoglm(
    #         op["account"], 
    #         op["operation"], 
    #         op["stock"], 
    #         op["volume"]
    #     )