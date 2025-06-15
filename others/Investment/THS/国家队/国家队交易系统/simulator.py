import pandas as pd
import numpy as np
from datetime import datetime

class Simulator:  # 修复：统一类名
    def __init__(self, initial_capital=100000):
        self.capital = initial_capital
        self.position = {}
        self.history = []
        self.transaction_fee_rate = 0.001  # 交易手续费

    def buy(self, symbol, price, size):
        cost = price * size * (1 + self.transaction_fee_rate)
        if cost > self.capital:
            print("资金不足，无法买入")
            return False

        self.capital -= cost
        if symbol in self.position:
            self.position[symbol]['size'] += size
            # 更新平均价格
            total_cost = self.position[symbol]['size'] * self.position[symbol]['avg_price'] + cost
            total_size = self.position[symbol]['size'] + size
            self.position[symbol]['avg_price'] = total_cost / total_size
        else:
            self.position[symbol] = {'size': size, 'avg_price': price}

        trade_record = {
            'type': 'buy',
            'symbol': symbol,
            'price': price,
            'size': size,
            'cost': cost,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'current_capital': self.capital
        }

        self.history.append(trade_record)
        print(f"买入 {symbol} @ {price:.2f} 共 {size} 股，花费: {cost:.2f}")
        return True

    def sell(self, symbol, price, size):
        """执行卖出操作"""
        if symbol not in self.position or self.position[symbol]['size'] < size:
            print("持仓不足，无法卖出")
            return False

        gain = price * size * (1 - self.transaction_fee_rate)
        avg_price = self.position[symbol]['avg_price']
        returns = (price - avg_price) / avg_price

        self.capital += gain
        self.position[symbol]['size'] -= size

        if self.position[symbol]['size'] == 0:
            del self.position[symbol]

        trade_record = {
            'type': 'sell',
            'symbol': symbol,
            'price': price,
            'size': size,
            'gain': gain,
            'returns': returns,
            'date': datetime.now().strftime("%Y-%m-%d %H:%M"),
            'current_capital': self.capital
        }

        self.history.append(trade_record)
        print(f"卖出 {symbol} @ {price:.2f} 共 {size} 股，收益率: {returns:.2%}")
        return True

    def get_position_summary(self):
        """获取持仓摘要"""
        summary = {
            'total_value': self.capital,
            'positions': {}
        }

        total_returns = 0
        for symbol, info in self.position.items():
            # 简化实时价格获取（实际应用中需实现）
            current_price = info['avg_price']  # 临时方案
            position_value = current_price * info['size']
            returns = (current_price - info['avg_price']) / info['avg_price']

            summary['positions'][symbol] = {
                'size': info['size'],
                'avg_price': info['avg_price'],
                'current_price': current_price,
                'value': position_value,
                'returns': returns
            }
            summary['total_value'] += position_value

        return summary  # 修复：添加返回值
