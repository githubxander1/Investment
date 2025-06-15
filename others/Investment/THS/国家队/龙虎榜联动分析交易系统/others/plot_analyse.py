import matplotlib.pyplot as plt

def plot_equity_curve(history):
    equity = [h['value'] for h in history]
    dates = [h['date'] for h in history]
    plt.figure(figsize=(10, 6))
    plt.plot(dates, equity)
    plt.title("账户净值曲线")
    plt.xlabel("日期")
    plt.ylabel("净值")
    plt.grid(True)
    plt.show()

def plot_positions(simulator):
    labels = list(simulator.position.keys())
    sizes = [simulator.position[s]['size'] for s in labels]
    plt.figure(figsize=(8, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%')
    plt.title("当前持仓分布")
    plt.show()
