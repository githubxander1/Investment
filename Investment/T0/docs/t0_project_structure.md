 # T0交易系统项目结构说明

## 项目概述

T0交易系统是一个用于实时监控股票交易信号并执行交易的量化交易系统。系统包含多个模块，每个模块负责不同的功能。

## 项目结构图

由于图形文件生成存在问题，以下是文字形式的项目结构描述：

```
T0交易系统
├── 监控模块 (monitor)
│   ├── 信号检测器 (signal_detector.py)
│   │   ├── 阻力支撑指标
│   │   ├── 扩展指标
│   │   └── 量价指标
│   ├── 交易执行器 (trade_executor.py)
│   ├── 图形界面 (gui.py)
│   └── 主监控程序 (T0_main.py)
├── 指标计算模块 (indicators)
│   ├── 阻力支撑指标 (resistance_support_indicators.py)
│   ├── 扩展指标 (extended_indicators.py)
│   ├── 量价指标 (volume_price_indicators.py)
│   └── 通达信指标 (tdx_indicators.py)
├── 工具模块 (utils)
│   ├── 数据处理 (data_handler.py)
│   ├── 日志模块 (logger.py)
│   └── 工具函数 (tools.py)
├── 配置模块 (config)
│   └── 系统配置 (settings.py)
├── 回测模块 (backtest)
│   ├── 回测引擎 (engine.py)
│   └── 回测策略 (strategies.py)
├── 可视化模块 (visualization)
│   └── 图表绘制 (plotting.py)
└── 入口文件
    ├── 主程序入口 (main.py)
    └── 运行脚本 (run_t0_system.py)
```

## 模块功能说明

### 监控模块 (monitor)
负责系统的实时监控功能，包括信号检测、交易执行和用户界面展示。

### 指标计算模块 (indicators)
计算各种技术指标，为信号检测提供数据支持。

### 工具模块 (utils)
提供系统运行所需的各种工具函数和辅助功能。

### 配置模块 (config)
管理系统配置参数。

### 回测模块 (backtest)
用于策略回测和验证。

### 可视化模块 (visualization)
负责图表绘制和数据可视化。

### 入口文件
系统的启动入口，包括主程序和运行脚本。