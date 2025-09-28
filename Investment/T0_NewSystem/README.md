# T0交易策略系统

一个基于Python的T0交易策略分析系统，用于实时监控股票市场、计算技术指标、生成交易信号并提供可视化分析。

## 项目结构

```
T0_NewSystem/
├── src/                   # 源代码目录
│   ├── indicators/        # 技术指标计算模块
│   │   └── tdx_indicators.py  # 通达信指标计算
│   ├── data/              # 数据处理模块
│   │   └── data_handler.py    # 数据获取和处理
│   ├── visualization/     # 数据可视化模块
│   │   └── plotting.py        # 图表绘制
│   ├── utils/             # 工具函数模块
│   │   └── tools.py           # 通用工具函数
│   ├── main.py            # 主程序入口
│   └── __init__.py        # 包初始化文件
├── examples/              # 示例代码
├── output/                # 输出目录（自动创建）
├── cache/                 # 数据缓存目录（自动创建）
├── requirements.txt       # 项目依赖
└── README.md              # 项目说明文档
```

## 功能模块

### 1. 指标计算模块 (`src/indicators/`)
- 通达信指标计算（支撑线、阻力线、买卖信号）
- RSI指标计算
- MACD指标计算
- 布林带指标计算

### 2. 数据处理模块 (`src/data/`)
- 股票分时数据获取
- 前一日收盘价获取
- 交易时间段数据处理
- 缺失数据填充
- 数据有效性验证
- 数据缓存机制

### 3. 数据可视化模块 (`src/visualization/`)
- 股票分时图绘制
- 带指标的分时图绘制
- 带买卖信号的分时图绘制
- 量价关系图绘制
- RSI指标图绘制
- 中文字体支持设置

### 4. 工具函数模块 (`src/utils/`)
- 交易时间检查
- 等待交易时间开始
- 信号通知发送
- 目录创建
- 日期时间处理
- 百分比变化计算
- 波动率计算

### 5. 主程序模块 (`src/main.py`)
- T0Strategy类：T0交易策略的主要实现
  - 股票池管理
  - 多指标分析
  - 交易信号检测
  - 图表生成
  - 信号通知
  - 自动运行和刷新

## 安装与配置

### 1. 环境要求
- Python 3.7 或更高版本
- pip 包管理工具

### 2. 安装依赖

```bash
# 安装所有依赖
pip install -r requirements.txt
```

### 3. 配置通知功能（可选）

如果需要使用通知功能，可以创建一个notification模块，实现send_notification函数。例如：

```python
# notification.py
import requests

def send_notification(title, content):
    """发送通知的具体实现"""
    # 这里可以集成各种通知方式，如微信、邮件、短信等
    # 示例：使用Server酱发送微信通知
    # requests.post("https://sctapi.ftqq.com/[YOUR_KEY].send", 
    #               data={"title": title, "desp": content})
    print(f"发送通知: {title}\n{content}")
```

## 使用方法

### 基本使用

1. 运行主程序

```bash
python src/main.py
```

2. 默认情况下，系统会监控以下股票：
   - 600000（浦发银行）
   - 000001（平安银行）
   - 601318（中国平安）
   - 000858（五粮液）
   - 600519（贵州茅台）

3. 系统会每60秒刷新一次数据，并在交易时间内自动运行

### 自定义股票池

可以在运行时指定自定义的股票池：

```python
from src import T0Strategy

# 创建自定义股票池的策略实例
strategy = T0Strategy(
    stock_pool=['600036', '600519', '000002'],  # 招商银行、贵州茅台、万科A
    refresh_interval=30,  # 30秒刷新一次
    save_charts=True,     # 保存图表
    notification_enabled=True  # 启用通知
)

# 运行策略
strategy.run()
```

### 单独分析单只股票

```python
from src import T0Strategy

# 创建策略实例
strategy = T0Strategy(save_charts=True)

# 分析单只股票
result = strategy.analyze_stock('600519')

# 查看分析结果
if result:
    print(f"股票代码: {result['stock_code']}")
    print(f"最新价格: {result['data'].iloc[-1]['收盘']}")
    print(f"买入信号数量: {len(result['signals']['buy_signals'])}")
    print(f"卖出信号数量: {len(result['signals']['sell_signals'])}")
```

## 策略说明

### 买入信号
- **支撑线突破**：当价格从支撑线下方突破到上方时（LONGCROSS(支撑,现价,2)）
- **RSI超卖回升**：当RSI指标从30以下回升到30以上时
- **MACD金叉**：当MACD线从下方穿越信号线时
- **布林带下轨反弹**：当价格触及布林带下轨后反弹时

### 卖出信号
- **阻力线突破**：当价格从阻力线下方突破到上方时（LONGCROSS(现价,阻力,2)）
- **RSI超买回落**：当RSI指标从70以上回落到70以下时
- **MACD死叉**：当MACD线从上方穿越信号线时
- **布林带上轨回落**：当价格触及布林带上轨后回落时

### 交易时间
- 系统会自动在交易时间（9:30-11:30, 13:00-15:00）运行
- 非交易时间会自动等待直到下一个交易时段开始

## 扩展指南

### 添加新的技术指标

1. 在`src/indicators/tdx_indicators.py`中添加新的指标计算函数

```python
def calculate_new_indicator(df, params):
    """
    计算新的技术指标
    """
    # 实现指标计算逻辑
    # ...
    return df
```

2. 在`T0Strategy.analyze_stock`方法中调用新的指标计算函数

### 修改策略逻辑

可以通过继承`T0Strategy`类并重写相应方法来修改策略逻辑：

```python
class MyCustomStrategy(T0Strategy):
    def _check_signals(self, df):
        """
        自定义信号检查逻辑
        """
        # 实现自定义的信号检查逻辑
        # ...
        return signals
```

## 注意事项

1. 本系统仅用于学习和研究目的，不构成任何投资建议
2. 实盘交易前请务必进行充分的测试和风险评估
3. 系统依赖akshare库获取数据，请确保网络连接正常
4. 大量请求可能会触发API限制，请合理设置刷新间隔
5. 数据缓存机制可以减少API调用，但可能占用一定的磁盘空间

## 版本历史

- v1.0.0 (2025-09-28): 初始版本，实现了基本的T0交易策略功能