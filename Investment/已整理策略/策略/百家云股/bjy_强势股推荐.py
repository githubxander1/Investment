from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import base64
import requests
import pandas as pd
import json
from datetime import datetime
import os

# ========================  加密解密配置与工具函数  ========================
# AES 算法相关配置（需与服务端保持一致）
AES_KEY = "romaway2015-bjcf"       # 加密密钥
AES_IV = "bjcf-romaway2015"        # 初始向量（CBC 模式需要）
AES_MODE = AES.MODE_CBC            # 加密模式
AES_BLOCK_SIZE = AES.block_size    # PKCS5Padding 填充的块大小（固定 16 字节）


def aes_encrypt(plaintext: str) -> str:
    """
    AES/CBC/PKCS5Padding 加密函数
    :param plaintext: 待加密的明文（字符串）
    :return: 加密后经 Base64 编码的字符串
    """
    cipher = AES.new(AES_KEY.encode("utf-8"), AES_MODE, AES_IV.encode("utf-8"))
    padded_data = pad(plaintext.encode("utf-8"), AES_BLOCK_SIZE)
    ciphertext = cipher.encrypt(padded_data)
    return base64.b64encode(ciphertext).decode("utf-8")


def aes_decrypt(ciphertext_base64: str) -> str:
    """
    AES/CBC/PKCS5Padding 解密函数
    :param ciphertext_base64: 经 Base64 编码的密文字符串
    :return: 解密后的明文字符串
    """
    ciphertext = base64.b64decode(ciphertext_base64)
    cipher = AES.new(AES_KEY.encode("utf-8"), AES_MODE, AES_IV.encode("utf-8"))
    plaintext = unpad(cipher.decrypt(ciphertext), AES_BLOCK_SIZE)
    return plaintext.decode("utf-8")


# ========================  HTTP 请求函数  ========================
def send_encrypted_request(data_time_ymd="0"):
    """
    发送加密 POST 请求并处理响应解密的完整流程
    1. 构造原始请求参数 → 2. AES 加密参数 → 3. 发送 POST 请求 → 4. 解密响应内容
    :param data_time_ymd: 数据日期，0表示最新，具体日期如"20251117"表示指定日期
    :return: 包含股票推荐数据的DataFrame
    """
    # 1. 构造原始请求参数（与加密内容文本一致）
    raw_param = f'{{"action":"strongRecommendStockIndex","member_id":"0","app_version":187,"n":1,"sign_level":0,"data_time_ymd":"{data_time_ymd}"}}'

    # 2. AES 加密请求参数
    encrypted_param = aes_encrypt(raw_param)

    # 3. 构造 HTTP 请求
    url = "https://www.baijiayungu.cn/bjcf/Interface6720"
    headers = {
        "content-type": "application/x-www-form-urlencoded; charset=utf-8",
        "accept-encoding": "gzip",
        "user-agent": "okhttp/3.3.1"
    }
    data = {
        "para": encrypted_param  # 参数名需与服务端接口约定一致
    }

    try:
        # 发送 POST 请求
        response = requests.post(url, headers=headers, data=data, timeout=10)
        response.raise_for_status()  # 检查 HTTP 状态码（非 200 会抛异常）

        # 4. 解密响应内容（假设响应体是 Base64 编码的 AES 密文）
        encrypted_response = response.text
        decrypted_response = aes_decrypt(encrypted_response)
        
        # 解析完整的原始响应数据
        raw_data = json.loads(decrypted_response)

        print("=== 解密后的响应内容 ===")
        print(json.dumps(raw_data, ensure_ascii=False, indent=2))

        # 提取数据并处理（新的返回值格式：df, available_dates）
        df, available_dates = extract_response_data(decrypted_response, data_time_ymd)
        if df is not None:
            print("\n=== 提取的DataFrame数据 ===")
            print(df.to_string(index=False))
            # 传递完整的原始数据给save_data函数
            save_data(df, available_dates=available_dates, raw_data=raw_data)
            return df
        return None

    except requests.RequestException as e:
        print(f"请求失败：{str(e)}")
        # 保存失败的请求信息
        error_filename = f"请求失败_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(error_filename, 'w', encoding='utf-8') as f:
            f.write(f"Error: {str(e)}\n\nURL: {url}\n\nRequest data: {raw_param}")
        print(f"请求失败信息已保存到: {error_filename}")
        return None


# ========================  主程序入口  ========================
def extract_response_data(decrypted_response: str, data_time_ymd: str) -> tuple:    
    """
    从解密后的响应中提取数据并返回完整的信息
    :param decrypted_response: 解密后的响应字符串
    :param data_time_ymd: 请求的数据日期
    :return: 包含股票推荐数据的DataFrame和可用日期列表
    """
    try:
        data = json.loads(decrypted_response)
        if data.get("result") != "0":
            print(f"响应数据格式异常 (result: {data.get('result')}, data_time_ymd: {data_time_ymd})")
            return None, None

        # 提取可用日期列表（data1字段）
        available_dates = []
        if "data1" in data and data["data1"]:
            available_dates = data["data1"]
            print(f"提取到{len(available_dates)}个可用历史日期")

        # 提取股票数据
        stocks = data.get("data", [])
        if not stocks:
            print(f"没有推荐股票数据 (data_time_ymd: {data_time_ymd})")
            return None, available_dates

        df = pd.DataFrame(stocks)

        # 添加数据日期和提取日期
        if data_time_ymd != "0":
            df["数据日期"] = data_time_ymd
        else:
            # 从响应中提取最新日期
            if available_dates:
                latest_date = available_dates[0].get("data_time", datetime.now().strftime("%Y%m%d"))
                df["数据日期"] = latest_date

        df["提取日期"] = datetime.now().strftime("%Y%m%d %H:%M:%S")

        # 处理data_type字段，将列表转换为字符串
        if "data_type" in df.columns:
            df["推荐类型"] = df["data_type"].apply(lambda x: ",".join(x) if isinstance(x, list) else x)
            
        # 重命名其他列
        df = df.rename(columns={
            "SecurityID": "股票代码",
            "Symbol": "股票名称",
            "addtime": "推荐时间",
            "addtimes": "时间戳"
        })

        # 确保所有必要的列存在
        required_columns = ["数据日期", "股票代码", "股票名称", "推荐时间", "推荐类型", "时间戳", "提取日期"]
        for col in required_columns:
            if col not in df.columns:
                df[col] = "-"

        # 重新排序列
        df = df[required_columns]

        # 将原始响应保存为JSON供后续分析
        raw_response_filename = f"原始响应_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        with open(raw_response_filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"原始响应已保存到: {raw_response_filename}")

        return df, available_dates

    except Exception as e:
        print(f"数据处理失败: {str(e)}")
        # 保存异常响应到文件以便分析
        error_filename = f"异常响应_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
        with open(error_filename, 'w', encoding='utf-8') as f:
            f.write(f"Error: {str(e)}\n\nResponse: {decrypted_response}")
        print(f"异常响应已保存到: {error_filename}")
        return None, None


def save_data(df: pd.DataFrame, filename_prefix="百家云股推荐", available_dates=None, raw_data=None):
    """
    增强版数据保存函数
    :param df: 要保存的DataFrame
    :param filename_prefix: 文件名前缀
    :param available_dates: 可用日期列表（可选）
    :param raw_data: 原始响应数据（可选）
    """
    try:
        # 创建数据保存目录结构
        base_dir = "bjy_data"
        today = datetime.now().strftime("%Y%m%d")
        save_dir = os.path.join(base_dir, today)
        os.makedirs(save_dir, exist_ok=True)
        
        # 生成带时间戳的文件名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = os.path.join(save_dir, f"{filename_prefix}_{timestamp}.csv")

        # 为DataFrame添加额外的元数据信息
        df_copy = df.copy()
        df_copy["数据来源"] = "百家云股"
        df_copy["API接口"] = "Interface6720"
        
        # 保存股票数据到CSV
        df_copy.to_csv(filename, index=False, encoding="utf_8_sig")
        print(f"股票数据已保存到: {filename}")

        # 如果有可用日期列表，也保存起来
        if available_dates:
            dates_df = pd.DataFrame(available_dates)
            dates_filename = os.path.join(save_dir, f"可用历史日期_{timestamp}.csv")
            dates_df.to_csv(dates_filename, index=False, encoding="utf_8_sig")
            print(f"可用历史日期已保存到: {dates_filename}")
        
        # 如果提供了原始数据，保存为JSON格式
        if raw_data:
            raw_filename = os.path.join(save_dir, f"原始响应_{timestamp}.json")
            with open(raw_filename, 'w', encoding='utf-8') as f:
                json.dump(raw_data, f, ensure_ascii=False, indent=2)
            print(f"原始完整响应已保存到: {raw_filename}")
        
        # 生成汇总报告文件
        generate_summary_report(df_copy, available_dates, save_dir, timestamp)

    except Exception as e:
        print(f"数据保存失败: {str(e)}")
        # 即使保存失败也尝试记录错误
        error_log = os.path.join("bjy_data", f"保存错误日志_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt")
        os.makedirs(os.path.dirname(error_log), exist_ok=True)
        with open(error_log, 'w', encoding='utf-8') as f:
            f.write(f"保存数据失败: {str(e)}")


def generate_summary_report(df: pd.DataFrame, available_dates, save_dir, timestamp):
    """
    生成数据汇总报告
    """
    try:
        report_filename = os.path.join(save_dir, f"数据汇总报告_{timestamp}.txt")
        
        with open(report_filename, 'w', encoding='utf-8') as f:
            f.write(f"=== 百家云股数据提取汇总报告 ===\n")
            f.write(f"生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 数据基本信息
            f.write("【数据基本信息】\n")
            f.write(f"股票数据数量: {len(df)}条\n")
            f.write(f"数据日期范围: {df['数据日期'].min()} 至 {df['数据日期'].max()}\n")
            
            # 股票代码列表
            f.write("\n【股票代码列表】\n")
            for code, name in zip(df['股票代码'], df['股票名称']):
                f.write(f"{code}: {name}\n")
            
            # 推荐类型统计
            if '推荐类型' in df.columns:
                f.write("\n【推荐类型统计】\n")
                type_counts = df['推荐类型'].value_counts()
                for type_name, count in type_counts.items():
                    f.write(f"{type_name}: {count}条\n")
            
            # 可用历史日期信息
            if available_dates:
                f.write(f"\n【可用历史日期信息】\n")
                f.write(f"可用日期总数: {len(available_dates)}\n")
                f.write(f"最新可用日期: {available_dates[0]['data_time']} ({available_dates[0]['show_ymd']})\n")
                f.write(f"最早可用日期: {available_dates[-1]['data_time']} ({available_dates[-1]['show_ymd']})\n")
        
        print(f"数据汇总报告已生成: {report_filename}")
    except Exception as e:
        print(f"生成汇总报告失败: {str(e)}")


def get_all_historical_data():
    """
    获取所有可用历史日期数据
    """
    all_data = []
    all_available_dates = []

    # 先获取最新数据以获取可用日期列表
    latest_df = send_encrypted_request("0")
    if latest_df is not None and not latest_df.empty:
        print(f"\n获取到最新数据，共{len(latest_df)}条记录")
        all_data.append(latest_df)

    # 尝试获取历史数据（这里可以根据实际需求调整日期范围）
    # 注意：实际API可能不支持所有日期，需要根据响应调整
    return pd.concat(all_data, ignore_index=True) if all_data else None


if __name__ == "__main__":
    # 获取最新数据
    df = send_encrypted_request("0")

    if df is not None:
        print(f"\n数据提取完成，共{len(df)}条记录")

        # 可以选择是否获取更多历史数据
        print("\n是否获取历史数据？可能需要更长时间...")
        # 如果需要获取更多历史数据，可以取消下面的注释
        # all_data = get_all_historical_data()
        # if all_data is not None:
        #     print(f"总共获取了{len(all_data)}条历史记录")
        #     save_data(all_data, "百家云股推荐_历史数据")