# Pages 模块说明

该目录包含所有与页面操作和业务逻辑相关的模块，按照功能进行了重新组织和优化。

## 目录结构

```
pages/
├── __init__.py                  # 包初始化文件，导出主要类
├── base/                        # 基础类模块
│   ├── __init__.py
│   ├── page_base.py            # 页面基础类
│   └── page_common.py          # 通用页面操作类
├── account/                     # 账户相关模块
│   ├── __init__.py
│   ├── account_info.py         # 账户信息管理类
│   └── account_info_hybrid.py  # 混合数据提取类
├── trading/                     # 交易相关模块
│   ├── __init__.py
│   ├── page_trading.py         # 交易页面类
│   ├── page_national_debt.py   # 国债逆回购页面类
│   └── trade_logic.py          # 交易逻辑类
└── devices/                     # 设备管理模块
    ├── __init__.py
    └── device_manager.py       # 设备管理类
```

## 模块说明

### base 模块
- `page_base.py`: 提供所有页面类的基础功能，如元素点击、文本获取等通用操作
- `page_common.py`: 提供各页面通用的操作方法，如页面跳转、账户切换等

### account 模块
- `account_info.py`: 负责账户数据的获取和处理，包括持仓信息、资金信息等
- `account_info_hybrid.py`: 使用XML解析和OCR技术相结合的方式提取账户数据，提高准确性

### trading 模块
- `page_trading.py`: 提供交易相关的页面操作，如买入、卖出、搜索股票等
- `page_national_debt.py`: 提供国债逆回购相关的页面操作
- `trade_logic.py`: 处理交易相关的业务逻辑，如计算买卖数量、执行交易等

### devices 模块
- `device_manager.py`: 负责设备连接和应用启动等设备相关操作

## 使用示例

```python
# 导入需要的类
from pages.account import AccountInfo
from pages.trading import TradeLogic

# 创建实例
account_info = AccountInfo()
trade_logic = TradeLogic()

# 使用功能
account_info.update_holding_info_all()
trade_logic.operate_stock("买入", "中国电信", 100)
```

## 优化说明

1. **模块化重构**：将原先单一文件中的功能拆分到不同模块中，提高代码可维护性
2. **功能分类**：按照业务功能将代码分类，便于查找和管理
3. **依赖清晰**：明确各模块之间的依赖关系，避免循环依赖
4. **命名规范**：统一命名规范，提高代码可读性
5. **注释完善**：为所有公共方法添加详细的文档字符串