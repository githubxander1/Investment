import requests
import json


def get_daily_data(stock_code):
    """
    获取指定股票的日线数据
    
    Args:
        stock_code (str): 股票代码
    
    Returns:
        dict: 日线数据
    """
    url = f"https://finance.pae.baidu.com/sapi/v1/get_candlestick_event?financeType=stock&code={stock_code}&market=ab&period=dayK&activeType=active&finClientType=pc"
    
    headers = {
        "Accept": "application/vnd.finance-web.v1+json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Referer": "https://gushitong.baidu.com/",
        "Acs-Token": "1760072660909_1760086616767_LQgcNrIWP0Qw6xLgSQTfi4d9zGAqHr6inW4p4RBAFQWZEaoUOuVQDs6eUHigslzPutTUOcl1xYUyZ3NqW4GuSfN3O+vnTnwTF1ZRm30LndcgCC4tDzQ7KDV/PLIA4cp4coXTfaOJbYKvLXa5yzzwrBrcbsfjd1rpZbnUGNZOXuJiH6zOFj/F6e10qkkPiZAJt0crp+UrIAIe82buf92OvcIvh4tpt8AeeqEv2jDzcunCZeOP5ZXApaNJiuF4uIIEuC3ia0OIWf4WZ1lAsNfdQmiXRCrdVb5YSIHtU1OEJAvCRAxJKBljvlFqPEql/bX45CCB4T1AQ1Vl793o+/YYCuhCEd0tq1Em+jyuBwwQcVDP3X6PRbDcq/JidX+v4bHUorE+pOFsiC/QSmODvJYqIFuDkL97e8u0austfwmoB+8DzkOV0jNyRjeLuwgTcRgUoEwQCM7fmTGtriCN9dCYolWRp/z1amMmaMRLCmdQUpU="
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"获取日线数据失败，状态码: {response.status_code}")
        return None


def get_minute_data(stock_code, stock_name):
    """
    获取指定股票的分时图数据
    
    Args:
        stock_code (str): 股票代码
        stock_name (str): 股票名称
    
    Returns:
        dict: 分时图数据
    """
    url = f"https://finance.pae.baidu.com/vapi/v1/getquotation?srcid=5353&pointType=string&group=quotation_minute_ab&query={stock_code}&code={stock_code}&market_type=ab&newFormat=1&name={stock_name}&is_kc=0&finClientType=pc&finClientType=pc"
    
    headers = {
        "Accept": "application/vnd.finance-web.v1+json",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
        "Referer": "https://gushitong.baidu.com/",
        "Acs-Token": "1760072660909_1760086629958_1nCI8El/Rsx3k1LgGRvpFImEKiJVSozYvmGXDa7jBp8jpraVnPRHfo2NXOoF2l/JVLrOjr9bhZDQDGFTIwY8XkxQCuf5jTcYEinKMm3QXbCh2Ws6T2tH43bMQXKHXxThtpLvsLim1oXxkCXHzD4jRr/BngTN329E0RdVn+9UWmCCE6+ZB4W7ba+NjRY5InRBJy7sR7jQnVWS5m/YFffGeASpBAVd9HbvjaINigluivYV34wFsysv6io05n1c6j3HbZkLIfyzycS5qI1Lx2ZQvAwuD9rzbb9NbZDLGDa79Rp959MD0iCisExlOMAkt2xCEUAJmNkgEpyXWUUg9gnrRz1n9oLrTh2tY44Xkal9TFS6TQd2zEZNPHxTpuPo8rQKpWQ6nBUxeX6YjfAZtPok9wAy9IwPvOjKzjrr7IXEbOuVX0+tp8xH9PNCxw+oL/oNJtnYY6ot9Pemj07yPDJmaclF3x0Xc13hGxqZFcZD9zo="
    }
    
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"获取分时图数据失败，状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        return None


def save_data_to_file(data, filename):
    """
    将数据保存到文件
    
    Args:
        data (dict): 要保存的数据
        filename (str): 文件名
    """
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print(f"数据已保存到 {filename}")


def main():
    # 获取美的集团的日线数据和分时图数据
    stock_code = "000333"
    stock_name = "美的集团"
    
    print("正在获取日线数据...")
    daily_data = get_daily_data(stock_code)
    if daily_data:
        save_data_to_file(daily_data, f"{stock_code}_daily_data.json")
        print("日线数据获取成功")
    
    print("正在获取分时图数据...")
    minute_data = get_minute_data(stock_code, stock_name)
    if minute_data:
        save_data_to_file(minute_data, f"{stock_code}_minute_data.json")
        print("分时图数据获取成功")


if __name__ == "__main__":
    main()