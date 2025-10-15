# ChinaStock_TradeAPI 使用指南

## 简介

ChinaStock_TradeAPI 是一个用于自动化控制国内股票交易软件（如同花顺）的 C++ 库。它通过 Windows API 直接操作交易软件界面，实现程序化交易功能。

## 环境要求

1. Windows 操作系统 (Windows 7/8/10/11)
2. 支持的交易软件（如同花顺网上交易系统）
3. Visual Studio 或其他 C++ 编译器
4. 管理员权限运行（用于访问其他进程内存）

## 编译说明

1. 使用 Visual Studio 打开 `pythonstock.vcxproj` 项目文件
2. 设置为 Release 模式
3. 编译生成 DLL 文件

## 基本使用流程

### 1. 初始化交易对象

```cpp
#include "pystock.h"

Pystock trader;
```

### 2. 启动交易软件

```cpp
int result = trader.OpenTrade("C:\\ths\\xiadan.exe");
// 返回值: 1 表示成功, 0 表示失败
```

### 3. 登录账户

```cpp
int result = trader.LoginTrade("account_name", "trade_password", "comm_password");
// 返回值: 1 表示成功, 0 表示失败
```

### 4. 预处理界面元素

```cpp
trader.PreHandle();
```

### 5. 执行交易操作

#### 买入股票
```cpp
bool result = trader.iBuy("600000", "10.00", "100");
// 参数: 股票代码, 价格, 数量
```

#### 卖出股票
```cpp
bool result = trader.iSell("600000", "10.50", "100");
// 参数: 股票代码, 价格, 数量
```

#### 撤单操作
```cpp
// 撤销指定股票委托
bool result = trader.iAbsort("600000", false);

// 撤销所有委托
bool result = trader.iAbsort(NULL, true);
```

### 6. 获取账户信息

#### 获取持仓信息
```cpp
PositionItem position = trader.iPosition();
cout << "总资产: " << position.accountequity << endl;
cout << "可用资金: " << position.accountfree << endl;
```

#### 获取详细数据列表
```cpp
// 获取持仓列表
int position_rows, position_cols;
trader.getAccountTicket(position_rows, position_cols);
// 数据存储在 trader.AccountTicket[row][col] 中

// 获取撤单列表
int absort_rows, absort_cols;
trader.getAbsortTicket(absort_rows, absort_cols);
// 数据存储在 trader.AbsortTicket[row][col] 中

// 获取成交列表
int deal_rows, deal_cols;
trader.getDealTicket(deal_rows, deal_cols);
// 数据存储在 trader.DealTicket[row][col] 中
```

### 7. 关闭交易软件

```cpp
int result = trader.CloseTrade();
// 返回值: 1 表示正常关闭, 0 表示关闭失败, 2 表示登录窗口关闭
```

## 错误处理

API 中的大部分函数都有返回值，用于指示操作是否成功：

- `OpenTrade`: 返回 1 表示成功，0 表示失败
- `LoginTrade`: 返回 1 表示成功，0 表示失败
- `iBuy/iSell`: 返回 true 表示操作完成
- `CloseTrade`: 返回 1 表示正常关闭，0 表示关闭失败，2 表示登录窗口关闭

## 注意事项

1. **权限要求**: 程序需要以管理员权限运行，以便访问交易软件进程内存

2. **界面可见性**: 交易软件界面在操作期间不能被最小化或遮挡

3. **时间延迟**: 在自动化操作中加入了适当的延迟，确保界面响应

4. **版本兼容性**: 当前实现针对特定版本的同花顺交易软件，其他版本可能需要调整

5. **安全性**: 在生产环境中使用时，确保账户信息的安全存储

6. **测试建议**: 强烈建议在实际交易前使用模拟盘进行充分测试

## 常见问题

### 1. 交易软件启动失败
- 检查交易软件路径是否正确
- 确保有足够的权限运行交易软件

### 2. 登录失败
- 检查账户信息是否正确
- 确认通讯密码是否正确
- 查看是否有验证码等额外验证步骤

### 3. 交易操作无响应
- 确保交易软件界面可见且未被遮挡
- 检查网络连接是否正常
- 确认交易时间是否在有效期内

### 4. 数据获取不完整
- 尝试增加操作间的延迟时间
- 确保对应的界面标签已正确切换（F1-F5键）

## 性能优化建议

1. **减少界面操作**: 尽量减少不必要的界面切换操作
2. **批量处理**: 对于批量交易操作，考虑合并处理以提高效率
3. **适当延迟**: 根据实际系统响应情况调整延迟时间
4. **错误重试**: 对于关键操作实现重试机制

## 扩展开发

开发者可以根据需要扩展以下功能：

1. 增加对其他交易软件的支持
2. 实现更复杂的风险控制机制
3. 添加日志记录功能
4. 开发图形化配置界面
5. 集成到量化交易策略系统中

## 法律声明

使用本接口进行股票交易时，请遵守相关法律法规，注意投资风险。本接口仅供技术研究使用，作者不对使用本接口造成的任何损失负责。