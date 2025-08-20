from datetime import datetime
from pprint import pprint

import pandas as pd
import requests
import json

from Investment.THS.AutoTrade.utils.format_data import determine_market
from Investment.已整理策略.策略.玩股成金.trade_history import convert_timestamp


def get_trade_details(robot_id):
   url = "http://ai.api.traderwin.com/api/ai/robot/history.json"

   headers = {
      "Content-Type": "application/json",
      "from": "Android",
      "token": "27129c04fb43a33723a9f7720f280ff9",
      "User-Agent": "Dalvik/2.1.0 (Linux; U; Android 10; Redmi Note 7 Pro MIUI/V12.5.4.0.QFHCNXM)",
      "Accept-Encoding": "gzip",
      "Connection": "Keep-Alive"
   }

   payload = {
      "index": 1,
      "pageSize": 5,
      "cmd": "9013",
      "robotId": robot_id,
      "type": -1  # 查询全部交易
   }

   try:
      response = requests.post(url, headers=headers, data=json.dumps(payload))
      response.raise_for_status()
      response_data = response.json()
      # pprint(response_data)
      return response_data
   except requests.exceptions.RequestException as e:
      print(f"请求失败: {e}")
      return None


def extract_trade_data(robots):
   today = datetime.now().date().strftime("%Y-%m-%d")

   all_today_trades = []
   for robot_name, robot_id in robots.items():
      result = get_trade_details(robot_id)
      pprint(result)
      if result and result.get("message", {}).get("state") == 0:
         data_list = result.get("data", {}).get("data", [])

         for trade in data_list:
            code = trade.get("symbol")
            market = determine_market(code)
            trade_date = convert_timestamp(trade.get("tradeDate"))
            if trade_date and trade_date.startswith(today):
               trade_info = {
                  # "交易ID": trade.get("logId"),
                  # "机器人ID": trade.get("robotId"),
                  "名称": robot_name,
                  "操作": "买入" if trade.get("type") == 1 else "卖出" if trade.get("type") == 0 else "已取消",
                  "标的名称": trade.get("symbolNmae"),
                  "代码": code,
                  "最新价": trade.get("price"),  # 原成交价格
                  "新比例%": 0,
                  "市场": market,
                  "时间": convert_timestamp(trade.get("created")),
                  "交易数量": trade.get("shares"),
                  # "买入价格": trade.get("buyPrice"),
                  # "交易金额": trade.get("balance"),
                  # "完成时间": convert_timestamp(trade.get("tradeTime"))
                  # "时间": convert_timestamp(trade.get("buyDate")),#原买入时间
               }
               all_today_trades.append(trade_info)
               # 通知格式输出
               # print(f"[{datetime.now().strftime('%Y-%m-%d')}] "
               #       f"名称：{trade_info['名称']}，"
               #       f"操作：{trade_info['操作']}，"
               #       f"标的名称：{trade_info['标的名称']}，"
               #       f"市场：{trade_info['市场']}，"
               #       f"最新价：{trade_info['最新价']}，"
               #       f"时间：{trade_info['时间']},"
               #       f"新比例%：{trade_info['新比例%']}")
               # f"代码：{trade_info['代码']}，"
               # f"数量：{trade_info['交易数量']}，"
               # f"买入价格：{trade_info['买入价格']}，"

      else:
         print(f"⚠️ 获取 {robot_name} 成交记录失败")

   if all_today_trades:  # 列表非空（空列表 [] 会被视为 False，所以 if my_list 等价于"非空"）
      df = pd.DataFrame(all_today_trades)
      return df
   # 当没有数据时，返回一个空的 DataFrame，列名与有数据时一致
   return pd.DataFrame(columns=['名称', '操作', '标的名称', '代码', '最新价', '新比例%', '市场', '时间'])

if __name__ == '__main__':
    robots = {
        "传媒娱乐": "13450b18-1df4-495e-a45a-f27428c16ae3",
    }
    df = extract_trade_data(robots)
    print(df)