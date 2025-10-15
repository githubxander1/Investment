# ChinaStock_TradeAPI/A股交易接口

通过系统底层控制交易软件，进行下单、撤单、查询等操作。

纯C++代码，生成dll供调用。下单速度可以极速至50ms。

## 使用说明

### 支持的交易软件
- 同花顺网上交易系统
- 川财证券等使用同花顺框架的券商软件

### 编译方法
使用Visual Studio打开pythonstock.vcxproj项目文件，配置为Release模式，编译生成DLL文件。

### 调用方法
```cpp
#include "pystock.h"

Pystock trader;
// 启动交易软件
trader.OpenTrade("D:\\Xander\\Applications\\THS\\同花顺\\xiadan.exe");
// 登录账户（需要输入账户名、交易密码、通讯密码）
trader.LoginTrade("account_name", "trade_password", "comm_password");
// 买入股票（股票代码、价格、数量）
trader.iBuy("601398", "5.00", "100");
```

### 注意事项
1. 程序需要管理员权限运行
2. 交易软件界面在操作期间不能被最小化或遮挡
3. 登录账户时使用的是证券账户而非同花顺账号
4. 买入价格需要根据实际行情填写