class Simulator:
    def __init__(self, initial_capital=100000):
        self.capital = initial_capital
        self.position = {}
        self.history = []

    def buy(self, symbol, price, size):
        cost = price * size
        if cost > self.capital:
            print("资金不足，无法买入")
            return
        self.capital -= cost
        if symbol in self.position:
            self.position[symbol]['size'] += size
        else:
            self.position[symbol] = {'size': size, 'price': price}
        self.history.append({
            'type': 'buy',
            'symbol': symbol,
            'price': price,
            'size': size,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        print(f"买入 {symbol} @ {price} 共 {size} 股")

    def sell(self, symbol, price, size):
        if symbol not in self.position or self.position[symbol]['size'] < size:
            print("持仓不足，无法卖出")
            return
        gain = price * size
        self.capital += gain
        avg_price = self.position[symbol]['price']
        profit = (price - avg_price) / avg_price * 100
        self.position[symbol]['size'] -= size
        if self.position[symbol]['size'] == 0:
            del self.position[symbol]
        self.history.append({
            'type': 'sell',
            'symbol': symbol,
            'price': price,
            'size': size,
            'profit_pct': profit,
            'date': datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        })
        print(f"卖出 {symbol} @ {price} 共 {size} 股，收益率: {profit:.2f}%")

    def status(self):
        print(f"当前资金: {self.capital:.2f}")
        print("持仓:")
        for symbol, info in self.position.items():
            print(f"{symbol}: {info['size']}股，成本价: {info['price']:.2f}")
