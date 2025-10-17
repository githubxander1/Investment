# T0策略回测系统

## 系统概述

T0策略回测系统是一个专门用于测试和评估T0交易策略的框架。该系统支持对三种主要技术指标进行回测分析：

1. **阻力支撑指标** - 基于通达信公式的阻力位和支撑位策略
2. **扩展指标** - 包含MACD、移动平均线等多种技术指标的综合策略
3. **量价指标** - 基于成交量和价格关系的交易策略

## 系统架构

```
backtest/
├── __init__.py              # 包初始化文件
├── config.py               # 回测配置参数
├── models.py               # 数据模型定义
├── data_loader.py          # 数据加载模块
├── strategies.py           # 策略实现模块
├── engine.py               # 回测引擎
├── main.py                 # 主程序入口
└── README_backtest.md      # 回测系统说明文档
```

## 安装和配置

### 依赖安装

确保已安装T0交易系统所需的所有依赖包：

```bash
cd Investment/T0
pip install -r requirements.txt
```

### 配置参数

在[config.py](file:///E:/git_documents/Investment/Investment/T0/backtest/config.py)文件中可以配置以下参数：

- `DEFAULT_INITIAL_CAPITAL`: 初始资金
- `DEFAULT_TRADE_AMOUNT`: 每次交易股数
- `DEFAULT_COMMISSION_RATE`: 手续费率
- `DEFAULT_SLIPPAGE`: 滑点
- `DEFAULT_BACKTEST_STOCKS`: 默认回测股票池
- `DEFAULT_START_DATE`: 默认回测开始日期
- `DEFAULT_END_DATE`: 默认回测结束日期

## 使用方法

### 基本使用

在T0目录下运行回测：

```bash
cd Investment/T0
python -m backtest.main
```

### 自定义参数

可以通过修改[main.py](file:///E:/git_documents/Investment/Investment/T0/backtest/main.py)中的参数来自定义回测：

```python
# 指定股票和日期范围
run_backtest(
    stocks=['000333', '600036'],
    indicators=['resistance_support', 'extended'],
    start_date='20250901',
    end_date='20250930'
)
```

## 回测指标说明

系统会计算并输出以下回测指标：

1. **收益率** - 策略的总收益率
2. **胜率** - 盈利交易占总交易数的比例
3. **最大回撤** - 账户资金的最大回撤幅度
4. **夏普比率** - 风险调整后的收益率
5. **交易次数** - 策略产生的交易信号数量

## 输出结果

回测结果将保存在以下位置：

- **CSV数据** - `backtest/results/backtest_results_YYYYMMDD_HHMMSS.csv`
- **分析图表** - `backtest/results/backtest_analysis.png`

## 扩展指南

### 添加新指标

要添加新的回测指标，请按以下步骤操作：

1. 在[strategies.py](file:///E:/git_documents/Investment/Investment/T0/backtest/strategies.py)中实现新的信号检测函数
2. 在[engine.py](file:///E:/git_documents/Investment/Investment/T0/backtest/engine.py)的`run_backtest`方法中添加对应的条件分支
3. 在[main.py](file:///E:/git_documents/Investment/Investment/T0/backtest/main.py)的默认指标列表中添加新指标

### 修改交易逻辑

如需修改交易执行逻辑，可以修改[engine.py](file:///E:/git_documents/Investment/Investment/T0/backtest/engine.py)中的[_execute_trades](file:///E:/git_documents/Investment/Investment/T0/backtest/engine.py#L79-L148)方法。

## 注意事项

1. 回测结果仅供参考，实际交易中可能因市场变化、滑点、手续费等因素导致结果差异
2. 确保网络连接正常，以便获取历史数据
3. 回测数据会被缓存到`backtest/data/`目录，以提高重复回测的效率
4. 建议使用较长时间段的数据进行回测，以获得更可靠的统计结果