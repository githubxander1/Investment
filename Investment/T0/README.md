# T0交易策略系统

一个模块化、可扩展的T0交易策略系统，支持不同指标的应用和配置。

## 回测系统

系统还包含一个完整的回测框架，用于测试和评估各种T0交易策略。详细信息请查看 [回测系统说明](backtest/README_backtest.md)。
有关回测系统的开发过程和实现细节，请查看 [回测开发文档](BACKTEST_DEVELOPMENT.md)。

## 项目结构

```
T0/
├── backtest/            # 回测系统模块
│   ├── __init__.py       # 包初始化文件
│   ├── config.py         # 回测配置
│   ├── models.py         # 数据模型
│   ├── data_loader.py    # 数据加载器
│   ├── strategies.py     # 策略实现
│   ├── engine.py         # 回测引擎
│   ├── main.py           # 回测主程序
│   └── README_backtest.md # 回测系统说明
├── config/              # 配置文件
│   └── settings.py       # 系统配置
├── indicators/          # 指标计算模块
│   ├── resistance_support_indicators.py  # 阻力支撑指标计算
│   ├── extended_indicators.py            # 扩展指标计算
│   ├── volume_price_indicators.py        # 量价指标计算
│   └── tdx_indicators.py # 通达信指标计算
├── monitor/             # 监控系统模块
│   ├── gui.py            # 图形界面监控
│   ├── main.py           # 命令行监控主程序
│   ├── signal_detector.py# 信号检测器
│   └── trade_executor.py # 交易执行器
├── utils/               # 工具函数模块
│   ├── data_handler.py   # 数据获取和缓存
│   ├── logger.py         # 日志记录
│   └── tools.py          # 辅助功能（时间检查、通知等）
├── visualization/       # 可视化模块
│   └── plotting.py       # 图表绘制功能
├── examples/            # 使用示例
├── cache/               # 数据缓存目录
├── logs/                # 日志文件目录
├── output/              # 输出文件目录
│   └── charts/           # 图表输出目录
├── main.py              # 主程序入口
├── run_t0_system.py     # 实际交易运行脚本
├── __init__.py          # 包初始化文件
├── requirements.txt     # 项目依赖
└── README.md            # 项目说明文档
```

## 功能模块说明

### 1. 配置模块 (config/)
- **settings.py**: 系统配置文件，包括股票池、监控间隔等参数

### 2. 指标计算模块 (indicators/)
- **resistance_support_indicators.py**: 阻力支撑指标计算，基于通达信公式计算支撑位和阻力位
- **extended_indicators.py**: 扩展指标计算，包括MACD、资金流向等
- **volume_price_indicators.py**: 量价指标计算
- **tdx_indicators.py**: 实现通达信指标计算，包括H1/L1/P1、支撑位、阻力位和交易信号计算

### 3. 监控系统模块 (monitor/)
- **gui.py**: 图形界面监控程序，提供可视化图表和信号日志
- **main.py**: 命令行监控主程序，适合后台运行
- **signal_detector.py**: 信号检测器，检测各类技术指标信号
- **trade_executor.py**: 交易执行器，执行买卖交易

### 4. 数据处理模块 (utils/)
- **data_handler.py**: 处理股票数据的获取、缓存、预处理等功能
- **logger.py**: 日志记录模块
- **tools.py**: 提供时间检查、信号通知等辅助功能

### 5. 可视化模块 (visualization/)
- **plotting.py**: 实现分时图的绘制，包括价格曲线、指标线和交易信号标记
- 支持交互式功能，如鼠标悬浮显示详情

### 6. 输出目录
- **cache/**: 存储获取的股票数据缓存，避免重复请求
- **logs/**: 存储系统运行日志和信号记录
- **output/charts/**: 存储生成的图表文件

## 安装和配置

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置通知功能

确保已经配置好`notification.py`文件中的通知参数（如钉钉Webhook、邮件设置等）

## 使用方法

### 实际交易模式（推荐）

在交易时间内持续运行系统：

```bash
python main.py run
```

或

```bash
python run_t0_system.py
```

### 测试模式

立即运行一次信号检测（用于测试）：

```bash
python main.py monitor
```

### 图形界面模式

启动图形界面监控程序：

```bash
python main.py gui
```

### 自定义股票池

可以通过命令行参数指定要监控的股票代码：

```bash
python main.py run 601398 600900 601728
python main.py gui 601088
python main.py monitor 601088 600900
```

### 修改源码配置

也可以直接在`config/settings.py`中修改配置参数来自定义系统行为。

## 策略说明

当前系统实现了基于多个技术指标的T0交易监控，主要包括：

1. **阻力支撑指标**：基于通达信公式计算支撑位和阻力位
2. **扩展指标**：包括MACD、移动平均线等技术指标
3. **量价指标**：基于成交量和价格关系的指标

系统会在交易时间内（9:30-11:30 和 13:00-15:00）按配置间隔检测信号，
并在发现交易信号时发送通知和执行交易（默认每笔交易100股）。

## 扩展指南

### 添加新指标

要添加新的指标计算逻辑：

1. 在`indicators/`目录下创建新的指标计算文件
2. 实现指标计算函数
3. 在`monitor/signal_detector.py`中集成新的指标检测逻辑

### 修改交易策略

要修改交易策略逻辑：

1. 修改`monitor/signal_detector.py`中的信号检测方法
2. 调整信号生成和过滤条件

## 注意事项

1. 本系统仅供参考，不构成投资建议
2. 请确保在交易时间运行系统
3. 定期更新数据和依赖包以确保系统正常运行
4. 使用前请备份好配置和数据文件

## 版本历史

- v1.0.0: 初始版本，实现基本的T0策略和模块化结构