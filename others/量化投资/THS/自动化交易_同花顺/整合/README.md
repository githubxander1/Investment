量化投资自动化交易/
├── config/                  # 配置文件
│   └── settings.py          # 全局配置
├── logs/                    # 日志文件
│   ├── ths_auto_trade.log
│   ├── 策略_今天调仓.log
│   └── 组合_今天调仓.log
├── data/                    # 数据文件
│   ├── operation_history.csv
│   ├── 策略今天调仓.xlsx
│   └── 组合今天调仓.xlsx
├── scripts/                 # 脚本文件
│   ├── ths_main.py          # 主程序
│   ├── 策略_今天调仓.py      # 策略调仓脚本
│   └── 组合_今天调仓.py      # 组合调仓脚本
├── utils/                   # 工具类和辅助函数
│   ├── file_monitor.py      # 文件监控工具
│   ├── notification.py      # 通知工具
│   ├── scheduler.py         # 定时任务工具
│   └── ths_logger.py        # 日志工具
├── pages/                   # 页面操作类
│   └── ths_page.py          # 同花顺页面操作类
└── README.md                # 项目说明文档
