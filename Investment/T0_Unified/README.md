# T0统一交易策略系统

一个模块化、可扩展的T0交易策略系统，整合了原有T0和T0_NewSystem两个系统的功能，支持不同指标的应用和配置。

## 项目结构

```
T0_Unified/
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
├── stock_data/            # 股票数据目录（自动创建）
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

本系统基于通达信T0交易策略，主要包含以下功能：

1. **支撑阻力计算**：根据前一日收盘价和当日最高最低价计算支撑位和阻力位
2. **买卖信号检测**：
   - 支撑位突破买入信号
   - 阻力位突破卖出信号
   - RSI、MACD、布林带等辅助指标信号
3. **实时监控**：在交易时间内自动监控股票池中的股票
4. **可视化分析**：生成包含价格、指标和信号的图表
5. **通知提醒**：当出现买卖信号时发送通知

## 版本历史

- v1.0.0 (2025-09-29): 初始版本，整合了原有T0和T0_NewSystem两个系统的功能