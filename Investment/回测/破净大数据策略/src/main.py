import yaml
from src.backtest.backtester import Backtester

def load_config(config_path='config/params.yaml'):
    """加载配置文件"""
    with open(config_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)

def main():
    # 加载配置
    config = load_config()

    # 初始化回测引擎
    backtester = Backtester(config)

    # 运行回测
    results = backtester.run_backtest()

    # 输出结果
    print(f"最终资金: {results[0].analyzers.getvalue().get_analysis()['value']}")
    print(f"夏普比率: {results[0].analyzers.sharpe.get_analysis()['sharperatio']}")
    print(f"最大回撤: {results[0].analyzers.drawdown.get_analysis()['max']['drawdown']}%")

if __name__ == '__main__':
    main()
