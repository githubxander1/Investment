# 同花顺交易API文档

## 概述

本项目提供基于同花顺交易客户端的自动化交易API服务，通过tornado框架构建Web服务，支持股票买入卖出和各类查询功能。服务通过操作xiadan.exe（同花顺下单程序）实现自动化交易。

## 服务信息

- **服务地址**：http://127.0.0.1:6003
- **主要接口**：
  - `/api/queue` - 交易操作接口（买入/卖出）
  - `/api/search` - 查询接口

## 1. 交易接口 `/api/queue`

### 描述

用于提交交易请求（买入/卖出股票），请求会被加入到交易队列中等待执行。

### 请求方法

`POST`

### 请求参数

需要提交JSON格式的数据，包含以下字段：

| 字段名 | 类型 | 描述 | 是否必填 |
|-------|------|------|---------|
| code | string | 股票代码 | 是 |
| name | string | 股票名称 | 是 |
| ct_amount | number | 交易数量 | 是 |
| strategy_no | string | 策略编号 | 是 |

### 内部处理流程

1. 接收请求并解析JSON数据
2. 为每个交易项添加必要信息：
   - stock_no: 股票代码（去掉后缀）
   - stock_name: 股票名称
   - amount: 交易数量（字符串格式）
   - key: 唯一标识符（UUID）
   - status: 初始状态设为0
3. 将交易信息写入ActiveWork.csv文件
4. 返回策略编号作为响应

### 响应格式

成功时返回：
```json
{
  "success": true,
  "data": "策略编号",
  "error": null
}
```

## 2. 查询接口 `/api/search`

### 描述

用于查询交易结果和各类交易相关信息。

### 请求方法

`POST`

### 请求参数

需要提交JSON格式的数据，包含以下字段：

| 字段名 | 类型 | 描述 | 是否必填 |
|-------|------|------|---------|
| strategy_no | string | 策略编号 | 是 |

### 内部处理流程

1. 接收请求并解析JSON数据
2. 检查系统是否正在执行交易，如正在执行则等待
3. 调用`SearchWorkLog.searchWorkLog()`方法查询结果：
   - 读取工作数据记录
   - 根据策略编号筛选数据
   - 调用`ExecAutoTrade.exec_run()`获取最新的市价委托数据
   - 更新成交状态信息
4. 返回查询结果

### 响应格式

成功时返回查询到的数据记录列表：
```json
{
  "success": true,
  "data": [
    {
      "字段1": "值1",
      "字段2": "值2",
      ...
    }
  ],
  "error": null
}
```

## 3. 查询子功能

`/api/search`接口支持以下查询子功能，通过传入不同的参数实现：

### 3.1 F6持仓查询

用于查询当前账户的股票持仓情况。

**请求参数示例**：
```json
{
  "strategy_no": "get_position"
}
```

**返回数据**：包含持仓股票的代码、名称、持仓数量、可用数量、成本价、现价等信息。

### 3.2 F7当日成交查询

用于查询当日已成交的交易记录。

**请求参数示例**：
```json
{
  "strategy_no": "get_today_trades"
}
```

**返回数据**：包含成交时间、股票代码、名称、买卖方向、价格、数量等信息。

### 3.3 F8委托查询

用于查询当日委托记录（包括已成交、未成交、已撤单等）。

**请求参数示例**：
```json
{
  "strategy_no": "get_today_entrusts"
}
```

**返回数据**：包含委托时间、股票代码、名称、买卖方向、价格、数量、状态等信息。

### 3.4 资金查询

用于查询账户资金情况。

**请求参数示例**：
```json
{
  "strategy_no": "get_balance"
}
```

**返回数据**：包含总资产、可用资金、可取资金、持仓市值等信息。

## 4. 交易队列说明

交易队列存储在`ActiveWork.csv`文件中，该文件包含以下字段：

| 字段名 | 描述 |
|-------|------|
| 股票代码 | 交易的股票代码 |
| 股票名称 | 交易的股票名称 |
| 数量 | 交易数量 |
| key | 唯一标识符 |
| status | 交易状态（0:未执行, 1:执行中, 2:已完成, 3:失败） |

## 5. 接口调用示例

### 5.1 Python调用示例

#### 买入股票

```python
import requests
import json

url = "http://127.0.0.1:6003/api/queue"

# 买入三花智控100股
data = [{
    "code": "002050.SZ",
    "name": "三花智控",
    "ct_amount": 100,
    "strategy_no": "strategy_001"
}]

headers = {"Content-Type": "application/json"}
response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.json())
```

#### 查询持仓

```python
import requests
import json

url = "http://127.0.0.1:6003/api/search"

data = {
    "strategy_no": "get_position"
}

headers = {"Content-Type": "application/json"}
response = requests.post(url, data=json.dumps(data), headers=headers)
print(response.json())
```

### 5.2 注意事项

1. 交易前确保已启动同花顺xiadan.exe并登录账户
2. 交易接口每次请求可以包含多个交易项
3. 查询接口会等待系统空闲后再执行查询
4. 系统会自动处理交易状态更新

## 6. 错误处理

当接口调用失败时，返回格式如下：

```json
{
  "success": false,
  "data": null,
  "error": "错误信息"
}
```

常见错误类型：

1. 同花顺客户端未启动或未登录
2. 股票代码错误或不存在
3. 资金不足（买入时）
4. 持仓不足（卖出时）
5. 系统繁忙，请稍后重试

## 7. 系统架构

- **Web服务**：基于tornado框架
- **交易控制**：通过pywinauto操作同花顺xiadan.exe
- **数据存储**：使用CSV文件存储交易队列和日志
- **核心模块**：
  - THSTradeAdapter：交易适配器
  - Exec_Auto_Trade：自动交易执行
  - Queue_Business：队列业务逻辑
  - Search_Work_Log：日志查询功能

## 8. 部署和运行

1. 确保已安装Python及相关依赖
2. 启动同花顺xiadan.exe并登录账户
3. 运行服务：`python app.py`
4. 服务默认在6003端口启动

## 9. 长期运行指南

- **个人电脑**：可以直接运行，保持同花顺客户端处于登录状态
- **云服务器**：推荐使用VNCServer等工具远程操作，确保图形界面可用
- **运行顺序**：必须先启动xiadan.exe并登录，再运行自动化控制程序

---

*本文档基于项目源码自动生成，如有变动请以实际代码为准。*