# -*- coding: utf-8 -*-
# 功能：底层HTTP请求，持续监听东方财富网分时数据更新（实时获取新数据）
#https://youle.zhipin.com/articles/65dc904f019f799fqxB73tm1EA~~.html
from http.client import HTTPConnection
import time


def listen_eastmoney_fenshi_realtime(secid="0.300059", interval=1):
    """
    持续监听分时数据更新
    :param secid: 股票标识（0.300059=深市300059，1=沪市）
    :param interval: 监听间隔（秒，默认1秒请求一次）
    """
    # 1. 接口配置（IP和Host需匹配，原文IP为119.3.12.115，Host为97.push2.eastmoney.com）
    api_ip = "119.3.12.115"  # 注意：IP可能随网站调整而变化，需重新抓包确认
    api_port = 80
    api_host = "97.push2.eastmoney.com"

    # 2. 构造请求参数（分时数据接口路径）
    request_params = (
        f"/api/qt/stock/details/sse"
        f"?fields1=f1,f2,f3,f4&fields2=f51,f52,f53,f54,f55"
        f"&mpi=2000&ut=bd1d9ddb04089700cf9c27f6f7426281"
        f"&fltt=2&pos=-0&secid={secid}"
    )

    # 3. 构造Headers（模拟浏览器请求，避免被反爬拦截）
    headers = {
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Encoding": "gzip, deflate",  # 若响应为压缩格式，需额外处理解压
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "no-cache",  # 禁止缓存，确保获取最新数据
        "Connection": "keep-alive",  # 保持长连接
        "Host": api_host,  # 必须与接口Host一致
        "Pragma": "no-cache",
        "Upgrade-Insecure-Requests": "1",
        # User-Agent：模拟Chrome浏览器（建议替换为自己的浏览器UA）
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }

    print(f"开始持续监听股票{secid}的分时数据（间隔{interval}秒），按Ctrl+C停止...")

    try:
        while True:
            # 4. 建立HTTP连接并发送请求
            conn = HTTPConnection(api_ip, api_port, timeout=10)
            try:
                conn.request(method="GET", url=request_params, headers=headers)
                # 获取响应
                response = conn.getresponse()
                print(f"\n【{time.strftime('%Y-%m-%d %H:%M:%S')}】响应状态码：{response.status}")

                if response.status == 200:
                    # 读取并解码响应内容（按行读取，适合流数据）
                    for line in response:
                        line_str = line.decode("utf-8").strip()
                        if line_str and line_str.startswith("data:"):
                            # 提取并打印实时数据
                            realtime_data = line_str.lstrip("data:")
                            print(f"实时数据：{realtime_data[:200]}...")  # 打印前200字符避免过长
                else:
                    print(f"请求失败，响应状态码：{response.status}，原因：{response.reason}")

            except Exception as e:
                print(f"请求过程出错：{e}")
            finally:
                conn.close()  # 关闭连接

            # 5. 间隔指定时间后再次请求
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n已停止监听")


# ------------------- 调用示例 -------------------
if __name__ == "__main__":
    # 监听深市股票300059的分时数据（间隔1秒）
    listen_eastmoney_fenshi_realtime(secid="1.688103", interval=1)