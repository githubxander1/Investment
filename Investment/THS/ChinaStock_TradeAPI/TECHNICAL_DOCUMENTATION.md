# ChinaStock_TradeAPI 技术文档

## 项目概述

ChinaStock_TradeAPI 是一个基于 C++ 的 A 股交易接口库，通过系统底层控制同花顺等交易软件，实现下单、撤单、查询等功能。该库以 DLL 形式提供接口，下单速度可达到 50ms 级别。

## 项目结构

```
ChinaStock_TradeAPI/
├── pystock.h              // 主要头文件，定义了 Pystock 类和相关结构体
├── pystock.cpp            // 主要实现文件，包含所有功能的实现
├── stdafx.h               // 预编译头文件
├── stdafx.cpp             // 预编译源文件
├── targetver.h            // Windows 版本定义
├── dllmain.cpp            // DLL 入口点
├── README.md              // 项目说明
└── pythonstock.vcxproj    // Visual Studio 项目文件
```

## 核心类与结构

### Pystock 类

Pystock 是核心类，提供了与交易软件交互的所有功能。

#### 成员变量

1. 窗口句柄相关：
   - `h_mainLogin`: 登录窗口句柄
   - `h_mainTrade`: 交易主窗口句柄
   - `h_buybtn[30]`: 买入按钮相关窗口句柄数组
   - `h_sellbtn[6]`: 卖出按钮相关窗口句柄数组
   - `h_Hposition[10]`: 持仓状态窗口句柄数组
   - `h_Absortticket[10]`: 撤单状态窗口句柄数组
   - `h_Dealticket[10]`: 成交列表窗口句柄数组

2. 数据存储：
   - `AccountTicket[GP][25]`: 持仓列表数据
   - `AbsortTicket[GP][25]`: 撤单列表数据
   - `DealTicket[GP][25]`: 成交列表数据

3. 进程信息：
   - `id_login`: 登录进程 ID

#### 主要方法

##### 1. 交易软件控制方法

- `int OpenTrade(char *filename)`: 启动交易软件
- `int LoginTrade(char *accName, char *secret, char *conSecret)`: 登录交易账户
- `int CloseTrade()`: 关闭交易软件
- `int HideTrade()`: 隐藏/显示交易窗口
- `int CloseAdWindow()`: 关闭广告窗口

##### 2. 界面元素获取方法

- `void getToolBar()`: 获取工具栏窗口句柄
- `void getBtnBar()`: 获取按钮栏窗口句柄
- `void getBuy()`: 获取买入按钮相关窗口句柄
- `void getSell()`: 获取卖出按钮相关窗口句柄
- `void getPosition()`: 获取持仓列表窗口句柄
- `void getAbsort()`: 获取撤单窗口句柄
- `void getDeal()`: 获取成交列表窗口句柄

##### 3. 数据获取方法

- `void getAccountTicket(int &rows, int &cols)`: 获取持仓列表数据
- `void getAbsortTicket(int &rows, int &cols)`: 获取撤单列表数据
- `void getDealTicket(int &rows, int &cols)`: 获取成交列表数据
- `PositionItem iPosition()`: 获取账户持仓信息

##### 4. 交易操作方法

- `bool iBuy(char* _stockcode, char* _orderprice, char* _orderlots)`: 买入股票
- `bool iSell(char* _stockcode, char* _orderprice, char* _orderlots)`: 卖出股票
- `bool iAbsort(char* _stockcode, bool AbsortAll)`: 撤单操作

### PositionItem 结构体

用于存储账户持仓信息：
```cpp
struct PositionItem {
    char* accountequity;    // 总资产
    char* accountfree;      // 可用资金
    char* marketvalue;      // 市值
    char* opsitionloss;     // 持仓盈亏
    char* opsitionrange;    // 仓位
    char* profitratio;      // 盈亏比例
};
```

## 技术实现原理

### 1. 窗口句柄获取

通过 Windows API 的 `EnumWindows` 函数遍历所有窗口，根据进程 ID 和窗口标题查找特定窗口句柄。

### 2. 控件操作

使用 `GetDlgItem`、`SendMessage`、`PostMessage` 等 Windows API 函数操作交易软件界面控件，实现自动填写和点击功能。

### 3. 数据读取

通过 `VirtualAllocEx`、`WriteProcessMemory`、`ReadProcessMemory` 等函数读取交易软件 ListView 控件中的数据。

### 4. 字符编码转换

实现了 `UnicodeToAnsi` 函数用于 Unicode 和 ANSI 字符串之间的转换。

## 使用方法

### 1. 编译生成 DLL

使用 Visual Studio 打开 `pythonstock.vcxproj` 项目文件，配置为 Release 模式，编译生成 DLL 文件。

### 2. 在其他语言中调用

#### Python 调用示例：

```python
import ctypes

# 加载 DLL
trade_api = ctypes.windll.LoadLibrary('pystock.dll')

# 创建 Pystock 对象
pystock = trade_api.Pystock()

# 启动交易软件
trade_api.OpenTrade.argtypes = [ctypes.c_char_p]
trade_api.OpenTrade.restype = ctypes.c_int
result = trade_api.OpenTrade(b"C:\\ths\\xiadan.exe")

# 登录账户
trade_api.LoginTrade.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
trade_api.LoginTrade.restype = ctypes.c_int
result = trade_api.LoginTrade(b"account", b"password", b"comm_password")

# 买入股票
trade_api.iBuy.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
trade_api.iBuy.restype = ctypes.c_bool
result = trade_api.iBuy(b"600000", b"10.00", b"100")

# 卖出股票
trade_api.iSell.argtypes = [ctypes.c_char_p, ctypes.c_char_p, ctypes.c_char_p]
trade_api.iSell.restype = ctypes.c_bool
result = trade_api.iSell(b"600000", b"10.50", b"100")

# 关闭交易软件
trade_api.CloseTrade()
```

#### C++ 调用示例：

```cpp
#include "pystock.h"

int main() {
    Pystock trader;
    
    // 启动交易软件
    int result = trader.OpenTrade("C:\\ths\\xiadan.exe");
    
    // 登录账户
    result = trader.LoginTrade("account", "password", "comm_password");
    
    // 买入股票
    bool buy_result = trader.iBuy("600000", "10.00", "100");
    
    // 卖出股票
    bool sell_result = trader.iSell("600000", "10.50", "100");
    
    // 关闭交易软件
    trader.CloseTrade();
    
    return 0;
}
```

## 注意事项

1. 该接口依赖于特定版本的交易软件（如同花顺），不同版本可能需要调整窗口查找逻辑。
2. 使用时需要确保交易软件安装在正确位置，并且账户信息正确。
3. 由于使用了 Windows API 直接操作界面控件，运行时不能最小化或遮挡交易软件窗口。
4. 建议在实际交易前进行充分测试，确保操作准确无误。

## 性能特点

- 下单速度可达 50ms 级别
- 支持全自动交易流程
- 可以获取实时持仓、成交、撤单等信息
- 提供完善的错误处理机制

## 适用范围

该接口适用于需要进行程序化交易的投资者，可以集成到各种量化交易系统中，实现自动化交易策略。