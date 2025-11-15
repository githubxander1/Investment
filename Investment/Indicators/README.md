# 技术指标回测框架

## 项目结构

```
Indicators/
├── Data/                   # 统一数据存储目录
├── T0/                     # T0交易相关指标
├── Technology/             # 技术指标回测
│   ├── top_bottom_strategy.py      # 顶底指标策略实现
│   ├── 主力建仓回测.py              # 主力建仓指标回测
│   ├── 优化CCI回测.py               # 优化CCI指标回测
│   └── 顶底指标回测.py              # 顶底指标回测（使用新框架）
├── utils/                  # 通用工具模块
│   ├── data_manager.py     # 数据管理器
│   └── backtest_engine.py  # 通用回测引擎
├── run_all_backtests.py    # 运行所有回测的主文件
├── README.md               # 项目说明文档
└── 优化总结报告.md           # 优化总结报告
```

## 使用说明

### 1. 数据管理
所有股票数据通过 `utils/data_manager.py` 统一管理：
- 自动从网络获取数据（优先使用 akshare）
- 本地缓存数据以避免重复下载
- 提供模拟数据生成功能

### 2. 回测引擎
通用回测引擎 `utils/backtest_engine.py` 提供：
- 标准化的回测流程
- 资金和持仓管理
- 交易记录和日志生成
- 结果可视化和图表生成

### 3. 策略实现
每个策略需要继承 `BacktestEngine` 类并实现：
- `calculate_indicators()`: 计算技术指标
- `calculate_signals()`: 计算买卖信号

### 4. 运行回测

#### 运行单个回测：
```python
# 运行顶底指标回测
python Technology/top_bottom_strategy.py
```

#### 运行所有回测：
```python
python run_all_backtests.py
```

## 新增功能

1. **统一数据源**: 所有指标回测使用相同的数据源，确保结果一致性
2. **模块化设计**: 指标计算、信号生成、回测执行分离，便于维护和扩展
3. **缓存机制**: 避免重复下载数据，提高回测效率
4. **标准化输出**: 统一的回测结果格式和可视化图表
5. 所有结果自动保存到 `e:/git_documents/Investment/回测/` 目录

## 指标列表

1. **顶底指标** (`Technology/top_bottom_strategy.py`)
2. **主力建仓指标** (`Technology/主力建仓回测.py`)
3. **优化CCI指标** (`Technology/优化CCI回测.py`)

## 数据目录

所有数据文件保存在 `Indicators/Data/` 目录下，按 `股票代码_开始日期_结束日期.csv` 格式命名。

## 回测结果目录

所有回测结果保存在 `e:/git_documents/Investment/回测/` 目录下：
- 交易记录：`回测记录_股票代码_时间戳.csv`
- 每日详细记录：`回测记录_每日记录_股票代码_时间戳.csv`
- 回测图表：`回测结果_股票代码_时间戳.png`

## 最新回测结果示例

### 中概互联ETF (513050)
- 回测期间：2024-11-15 至 2025-11-15
- 总收益率：-99.52%
- 胜率：0.00%

### 恒生互联网ETF (513330)
- 回测期间：2024-11-15 至 2025-11-15
- 总收益率：51.01%
- 胜率：100.00%