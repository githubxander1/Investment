# 同花顺10jqka-API实盘交易功能实现方案

## 1. 项目概述

本文档提供在现有10jqka-API项目基础上实现实盘交易功能的详细方案，通过扩展API接口实现证券账户查询和实盘交易能力，不依赖UI界面，完全通过API方式操作。

## 2. 技术架构设计

### 2.1 系统架构图

```
+----------------+      +-------------------+      +-------------------+
|                |      |                   |      |                   |
|  客户端应用     +----->+  10jqka-API服务    +----->+  同花顺服务器      |
|                |      |  (扩展实盘交易)     |      |  (mobi2.hexin.cn) |
+----------------+      +-------------------+      +-------------------+
```

### 2.2 核心组件

1. **API服务器层**：基于现有Flask框架，扩展交易相关接口
2. **交易服务层**：封装交易指令构建和发送逻辑
3. **通信层**：处理与同花顺服务器的TCP通信和协议解析
4. **数据持久层**：保存交易记录、账户信息等

## 3. 功能模块设计

### 3.1 证券账户查询模块

实现获取同花顺账户下关联的所有证券账户信息，包括账户类型、资金账号等。

### 3.2 交易指令模块

支持以下交易操作：
- 买入股票
- 卖出股票
- 查询委托
- 查询成交
- 查询资金
- 查询持仓

### 3.3 订单管理模块

- 委托单状态跟踪
- 撤单功能
- 交易日志记录

## 4. 代码实现方案

### 4.1 扩展API接口 (app.py)

```python
from flask import Flask, request, jsonify
import os
import subprocess
import json

app = Flask(__name__)

# 项目路径配置
base_dir = os.path.dirname(os.path.abspath(__file__))
ths_project_dir = os.path.dirname(base_dir)

# 检查passport.dat文件是否存在
def check_passport_file():
    passport_path = os.path.join(ths_project_dir, "passport.dat")
    exists = os.path.exists(passport_path)
    return {
        "exists": exists,
        "path": passport_path if exists else None
    }

# 运行Java程序
def run_java_program(command, timeout=30):
    try:
        # 构建完整的命令行
        java_cmd = [
            "java",
            "-cp",
            f"{ths_project_dir}/lib/snappy-java-1.1.10.1.jar;{ths_project_dir}/bin;.",
            command
        ]
        
        # 执行命令
        result = subprocess.run(
            java_cmd,
            cwd=ths_project_dir,
            capture_output=True,
            text=True,
            timeout=timeout
        )
        
        return {
            "success": result.returncode == 0,
            "stdout": result.stdout,
            "stderr": result.stderr
        }
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

# 健康检查接口
@app.route('/api/health', methods=['GET'])
def health_check():
    return jsonify({
        "status": "ok",
        "message": "API服务运行正常"
    })

# 检查passport.dat接口
@app.route('/api/ths/check_passport', methods=['GET'])
def check_passport():
    result = check_passport_file()
    return jsonify(result)

# 登录接口
@app.route('/api/ths/login', methods=['POST'])
def login():
    data = request.json
    phone = data.get('phone')
    password = data.get('password')
    
    if not phone or not password:
        return jsonify({
            "success": False,
            "message": "手机号和密码不能为空"
        }), 400
    
    # 调用Java程序执行登录
    result = run_java_program(f"Login {phone} {password}")
    
    # 检查是否生成了passport.dat
    passport_result = check_passport_file()
    
    return jsonify({
        "success": result['success'] and passport_result['exists'],
        "message": "登录成功" if (result['success'] and passport_result['exists']) else "登录失败",
        "login_output": result
    })

# 新增接口：获取证券账户列表
@app.route('/api/ths/accounts', methods=['GET'])
def get_accounts():
    # 检查是否已登录
    passport_result = check_passport_file()
    if not passport_result['exists']:
        return jsonify({
            "success": False,
            "message": "请先登录"
        }), 401
    
    # 调用Java程序获取账户列表
    result = run_java_program("GetAccounts")
    
    if result['success']:
        try:
            accounts_data = json.loads(result['stdout'])
            return jsonify({
                "success": True,
                "accounts": accounts_data
            })
        except json.JSONDecodeError:
            return jsonify({
                "success": False,
                "message": "解析账户数据失败",
                "raw_output": result['stdout']
            })
    else:
        return jsonify({
            "success": False,
            "message": "获取账户列表失败",
            "error": result['stderr']
        })

# 新增接口：股票买入
@app.route('/api/ths/buy', methods=['POST'])
def buy_stock():
    data = request.json
    account_id = data.get('account_id')
    stock_code = data.get('stock_code')
    price = data.get('price')
    quantity = data.get('quantity')
    
    if not all([account_id, stock_code, price, quantity]):
        return jsonify({
            "success": False,
            "message": "请提供完整的交易信息"
        }), 400
    
    # 检查是否已登录
    passport_result = check_passport_file()
    if not passport_result['exists']:
        return jsonify({
            "success": False,
            "message": "请先登录"
        }), 401
    
    # 构建交易命令
    trade_command = f"Trade buy {account_id} {stock_code} {price} {quantity}"
    result = run_java_program(trade_command)
    
    return jsonify({
        "success": result['success'],
        "message": "买入委托已提交" if result['success'] else "买入委托失败",
        "trade_output": result
    })

# 新增接口：股票卖出
@app.route('/api/ths/sell', methods=['POST'])
def sell_stock():
    data = request.json
    account_id = data.get('account_id')
    stock_code = data.get('stock_code')
    price = data.get('price')
    quantity = data.get('quantity')
    
    if not all([account_id, stock_code, price, quantity]):
        return jsonify({
            "success": False,
            "message": "请提供完整的交易信息"
        }), 400
    
    # 检查是否已登录
    passport_result = check_passport_file()
    if not passport_result['exists']:
        return jsonify({
            "success": False,
            "message": "请先登录"
        }), 401
    
    # 构建交易命令
    trade_command = f"Trade sell {account_id} {stock_code} {price} {quantity}"
    result = run_java_program(trade_command)
    
    return jsonify({
        "success": result['success'],
        "message": "卖出委托已提交" if result['success'] else "卖出委托失败",
        "trade_output": result
    })

# 新增接口：查询资金
@app.route('/api/ths/funds', methods=['GET'])
def get_funds():
    account_id = request.args.get('account_id')
    
    if not account_id:
        return jsonify({
            "success": False,
            "message": "请提供账户ID"
        }), 400
    
    # 检查是否已登录
    passport_result = check_passport_file()
    if not passport_result['exists']:
        return jsonify({
            "success": False,
            "message": "请先登录"
        }), 401
    
    # 调用Java程序查询资金
    result = run_java_program(f"GetFunds {account_id}")
    
    if result['success']:
        try:
            funds_data = json.loads(result['stdout'])
            return jsonify({
                "success": True,
                "funds": funds_data
            })
        except json.JSONDecodeError:
            return jsonify({
                "success": False,
                "message": "解析资金数据失败",
                "raw_output": result['stdout']
            })
    else:
        return jsonify({
            "success": False,
            "message": "查询资金失败",
            "error": result['stderr']
        })

# 新增接口：查询持仓
@app.route('/api/ths/positions', methods=['GET'])
def get_positions():
    account_id = request.args.get('account_id')
    
    if not account_id:
        return jsonify({
            "success": False,
            "message": "请提供账户ID"
        }), 400
    
    # 检查是否已登录
    passport_result = check_passport_file()
    if not passport_result['exists']:
        return jsonify({
            "success": False,
            "message": "请先登录"
        }), 401
    
    # 调用Java程序查询持仓
    result = run_java_program(f"GetPositions {account_id}")
    
    if result['success']:
        try:
            positions_data = json.loads(result['stdout'])
            return jsonify({
                "success": True,
                "positions": positions_data
            })
        except json.JSONDecodeError:
            return jsonify({
                "success": False,
                "message": "解析持仓数据失败",
                "raw_output": result['stdout']
            })
    else:
        return jsonify({
            "success": False,
            "message": "查询持仓失败",
            "error": result['stderr']
        })

# 新增接口：查询委托
@app.route('/api/ths/orders', methods=['GET'])
def get_orders():
    account_id = request.args.get('account_id')
    status = request.args.get('status', 'all')  # all, pending, executed, canceled
    
    if not account_id:
        return jsonify({
            "success": False,
            "message": "请提供账户ID"
        }), 400
    
    # 检查是否已登录
    passport_result = check_passport_file()
    if not passport_result['exists']:
        return jsonify({
            "success": False,
            "message": "请先登录"
        }), 401
    
    # 调用Java程序查询委托
    result = run_java_program(f"GetOrders {account_id} {status}")
    
    if result['success']:
        try:
            orders_data = json.loads(result['stdout'])
            return jsonify({
                "success": True,
                "orders": orders_data
            })
        except json.JSONDecodeError:
            return jsonify({
                "success": False,
                "message": "解析委托数据失败",
                "raw_output": result['stdout']
            })
    else:
        return jsonify({
            "success": False,
            "message": "查询委托失败",
            "error": result['stderr']
        })

# 新增接口：撤单
@app.route('/api/ths/cancel_order', methods=['POST'])
def cancel_order():
    data = request.json
    account_id = data.get('account_id')
    order_id = data.get('order_id')
    
    if not all([account_id, order_id]):
        return jsonify({
            "success": False,
            "message": "请提供账户ID和订单ID"
        }), 400
    
    # 检查是否已登录
    passport_result = check_passport_file()
    if not passport_result['exists']:
        return jsonify({
            "success": False,
            "message": "请先登录"
        }), 401
    
    # 调用Java程序撤单
    result = run_java_program(f"CancelOrder {account_id} {order_id}")
    
    return jsonify({
        "success": result['success'],
        "message": "撤单请求已提交" if result['success'] else "撤单失败",
        "cancel_output": result
    })

if __name__ == '__main__':
    # 生产环境使用Waitress作为WSGI服务器
    from waitress import serve
    print("使用Waitress作为生产服务器")
    serve(app, host='0.0.0.0', port=5000)
```

### 4.2 扩展Java核心功能 (TradeHandler.java)

创建一个新的Java类来处理交易相关功能：

```java
package core;

import java.io.*;
import java.net.Socket;
import java.util.*;
import org.json.JSONObject;
import org.json.JSONArray;

public class TradeHandler {
    private ThsCore thsCore;
    private Socket socket;
    private static final String HOST = "mobi2.hexin.cn";
    private static final int PORT = 9528;
    
    public TradeHandler() {
        thsCore = new ThsCore();
    }
    
    public void connect() throws IOException {
        socket = new Socket(HOST, PORT);
        thsCore.setSocket(socket);
    }
    
    public void disconnect() throws IOException {
        if (socket != null && !socket.isClosed()) {
            socket.close();
        }
    }
    
    // 加载passport.dat文件进行自动登录
    public boolean loadPassport(String passportPath) throws IOException {
        File passportFile = new File(passportPath);
        if (!passportFile.exists()) {
            return false;
        }
        
        // 读取passport.dat文件内容
        byte[] passportData = new byte[(int) passportFile.length()];
        try (FileInputStream fis = new FileInputStream(passportFile)) {
            fis.read(passportData);
        }
        
        // 使用passport数据进行自动登录
        return thsCore.passportLogin(passportData);
    }
    
    // 获取证券账户列表
    public String getAccounts() throws Exception {
        // 发送获取账户列表的请求
        byte[] request = thsCore.buildAccountListRequest();
        byte[] response = thsCore.sendRequest(request);
        
        // 解析账户列表响应
        List<Map<String, Object>> accounts = thsCore.parseAccountListResponse(response);
        
        // 转换为JSON字符串返回
        JSONArray jsonAccounts = new JSONArray(accounts);
        return jsonAccounts.toString();
    }
    
    // 股票买入
    public String buyStock(String accountId, String stockCode, double price, int quantity) throws Exception {
        // 构建买入请求
        byte[] request = thsCore.buildTradeRequest("buy", accountId, stockCode, price, quantity);
        byte[] response = thsCore.sendRequest(request);
        
        // 解析交易响应
        Map<String, Object> result = thsCore.parseTradeResponse(response);
        
        // 转换为JSON字符串返回
        JSONObject jsonResult = new JSONObject(result);
        return jsonResult.toString();
    }
    
    // 股票卖出
    public String sellStock(String accountId, String stockCode, double price, int quantity) throws Exception {
        // 构建卖出请求
        byte[] request = thsCore.buildTradeRequest("sell", accountId, stockCode, price, quantity);
        byte[] response = thsCore.sendRequest(request);
        
        // 解析交易响应
        Map<String, Object> result = thsCore.parseTradeResponse(response);
        
        // 转换为JSON字符串返回
        JSONObject jsonResult = new JSONObject(result);
        return jsonResult.toString();
    }
    
    // 查询资金
    public String getFunds(String accountId) throws Exception {
        // 构建查询资金请求
        byte[] request = thsCore.buildFundsRequest(accountId);
        byte[] response = thsCore.sendRequest(request);
        
        // 解析资金响应
        Map<String, Object> funds = thsCore.parseFundsResponse(response);
        
        // 转换为JSON字符串返回
        JSONObject jsonFunds = new JSONObject(funds);
        return jsonFunds.toString();
    }
    
    // 查询持仓
    public String getPositions(String accountId) throws Exception {
        // 构建查询持仓请求
        byte[] request = thsCore.buildPositionsRequest(accountId);
        byte[] response = thsCore.sendRequest(request);
        
        // 解析持仓响应
        List<Map<String, Object>> positions = thsCore.parsePositionsResponse(response);
        
        // 转换为JSON字符串返回
        JSONArray jsonPositions = new JSONArray(positions);
        return jsonPositions.toString();
    }
    
    // 查询委托
    public String getOrders(String accountId, String status) throws Exception {
        // 构建查询委托请求
        byte[] request = thsCore.buildOrdersRequest(accountId, status);
        byte[] response = thsCore.sendRequest(request);
        
        // 解析委托响应
        List<Map<String, Object>> orders = thsCore.parseOrdersResponse(response);
        
        // 转换为JSON字符串返回
        JSONArray jsonOrders = new JSONArray(orders);
        return jsonOrders.toString();
    }
    
    // 撤单
    public String cancelOrder(String accountId, String orderId) throws Exception {
        // 构建撤单请求
        byte[] request = thsCore.buildCancelOrderRequest(accountId, orderId);
        byte[] response = thsCore.sendRequest(request);
        
        // 解析撤单响应
        Map<String, Object> result = thsCore.parseCancelOrderResponse(response);
        
        // 转换为JSON字符串返回
        JSONObject jsonResult = new JSONObject(result);
        return jsonResult.toString();
    }
}
```

### 4.3 扩展Main.java添加交易功能入口

```java
import core.TradeHandler;
import java.io.*;

public class Main {
    public static void main(String[] args) {
        try {
            if (args.length < 1) {
                System.out.println("请提供命令参数");
                System.out.println("可用命令: Login, GetAccounts, Buy, Sell, GetFunds, GetPositions, GetOrders, CancelOrder");
                return;
            }
            
            String command = args[0];
            String projectDir = System.getProperty("user.dir");
            String passportPath = projectDir + File.separator + "passport.dat";
            
            TradeHandler tradeHandler = new TradeHandler();
            
            try {
                // 连接服务器
                tradeHandler.connect();
                
                // 根据命令执行不同操作
                switch (command) {
                    case "Login":
                        if (args.length < 3) {
                            System.out.println("登录命令格式: Login <手机号> <密码>");
                            return;
                        }
                        String phone = args[1];
                        String password = args[2];
                        // 这里应该调用现有的登录逻辑
                        break;
                        
                    case "GetAccounts":
                        // 加载passport进行自动登录
                        if (!tradeHandler.loadPassport(passportPath)) {
                            System.out.println("{\"error\":\"未找到有效的passport.dat文件，请先登录\"}");
                            return;
                        }
                        String accounts = tradeHandler.getAccounts();
                        System.out.println(accounts);
                        break;
                        
                    case "Trade":
                        if (args.length < 6) {
                            System.out.println("交易命令格式: Trade <buy/sell> <account_id> <stock_code> <price> <quantity>");
                            return;
                        }
                        String tradeType = args[1];
                        String accountId = args[2];
                        String stockCode = args[3];
                        double price = Double.parseDouble(args[4]);
                        int quantity = Integer.parseInt(args[5]);
                        
                        // 加载passport进行自动登录
                        if (!tradeHandler.loadPassport(passportPath)) {
                            System.out.println("{\"error\":\"未找到有效的passport.dat文件，请先登录\"}");
                            return;
                        }
                        
                        String tradeResult;
                        if ("buy".equals(tradeType)) {
                            tradeResult = tradeHandler.buyStock(accountId, stockCode, price, quantity);
                        } else if ("sell".equals(tradeType)) {
                            tradeResult = tradeHandler.sellStock(accountId, stockCode, price, quantity);
                        } else {
                            System.out.println("{\"error\":\"交易类型必须是buy或sell\"}");
                            return;
                        }
                        System.out.println(tradeResult);
                        break;
                        
                    case "GetFunds":
                        if (args.length < 2) {
                            System.out.println("查询资金命令格式: GetFunds <account_id>");
                            return;
                        }
                        accountId = args[1];
                        
                        // 加载passport进行自动登录
                        if (!tradeHandler.loadPassport(passportPath)) {
                            System.out.println("{\"error\":\"未找到有效的passport.dat文件，请先登录\"}");
                            return;
                        }
                        
                        String funds = tradeHandler.getFunds(accountId);
                        System.out.println(funds);
                        break;
                        
                    case "GetPositions":
                        if (args.length < 2) {
                            System.out.println("查询持仓命令格式: GetPositions <account_id>");
                            return;
                        }
                        accountId = args[1];
                        
                        // 加载passport进行自动登录
                        if (!tradeHandler.loadPassport(passportPath)) {
                            System.out.println("{\"error\":\"未找到有效的passport.dat文件，请先登录\"}");
                            return;
                        }
                        
                        String positions = tradeHandler.getPositions(accountId);
                        System.out.println(positions);
                        break;
                        
                    case "GetOrders":
                        if (args.length < 2) {
                            System.out.println("查询委托命令格式: GetOrders <account_id> [status]");
                            return;
                        }
                        accountId = args[1];
                        String status = args.length > 2 ? args[2] : "all";
                        
                        // 加载passport进行自动登录
                        if (!tradeHandler.loadPassport(passportPath)) {
                            System.out.println("{\"error\":\"未找到有效的passport.dat文件，请先登录\"}");
                            return;
                        }
                        
                        String orders = tradeHandler.getOrders(accountId, status);
                        System.out.println(orders);
                        break;
                        
                    case "CancelOrder":
                        if (args.length < 3) {
                            System.out.println("撤单命令格式: CancelOrder <account_id> <order_id>");
                            return;
                        }
                        accountId = args[1];
                        String orderId = args[2];
                        
                        // 加载passport进行自动登录
                        if (!tradeHandler.loadPassport(passportPath)) {
                            System.out.println("{\"error\":\"未找到有效的passport.dat文件，请先登录\"}");
                            return;
                        }
                        
                        String cancelResult = tradeHandler.cancelOrder(accountId, orderId);
                        System.out.println(cancelResult);
                        break;
                        
                    default:
                        System.out.println("不支持的命令: " + command);
                        break;
                }
            } finally {
                // 断开连接
                tradeHandler.disconnect();
            }
        } catch (Exception e) {
            e.printStackTrace();
            System.out.println("{\"error\":\"" + e.getMessage() + "\"}");
        }
    }
}
```

### 4.4 扩展ThsCore类添加交易相关方法

需要在现有的ThsCore类中添加以下方法：

```java
// 构建获取账户列表请求
public byte[] buildAccountListRequest() {
    // 实现构建获取账户列表的请求数据包
    // ...
    return requestData;
}

// 解析账户列表响应
public List<Map<String, Object>> parseAccountListResponse(byte[] response) {
    // 实现解析账户列表响应数据
    List<Map<String, Object>> accounts = new ArrayList<>();
    // ...
    return accounts;
}

// 构建交易请求
public byte[] buildTradeRequest(String tradeType, String accountId, String stockCode, double price, int quantity) {
    // 实现构建买入/卖出请求数据包
    // ...
    return requestData;
}

// 解析交易响应
public Map<String, Object> parseTradeResponse(byte[] response) {
    // 实现解析交易响应数据
    Map<String, Object> result = new HashMap<>();
    // ...
    return result;
}

// 构建查询资金请求
public byte[] buildFundsRequest(String accountId) {
    // 实现构建查询资金请求数据包
    // ...
    return requestData;
}

// 解析资金响应
public Map<String, Object> parseFundsResponse(byte[] response) {
    // 实现解析资金响应数据
    Map<String, Object> funds = new HashMap<>();
    // ...
    return funds;
}

// 构建查询持仓请求
public byte[] buildPositionsRequest(String accountId) {
    // 实现构建查询持仓请求数据包
    // ...
    return requestData;
}

// 解析持仓响应
public List<Map<String, Object>> parsePositionsResponse(byte[] response) {
    // 实现解析持仓响应数据
    List<Map<String, Object>> positions = new ArrayList<>();
    // ...
    return positions;
}

// 构建查询委托请求
public byte[] buildOrdersRequest(String accountId, String status) {
    // 实现构建查询委托请求数据包
    // ...
    return requestData;
}

// 解析委托响应
public List<Map<String, Object>> parseOrdersResponse(byte[] response) {
    // 实现解析委托响应数据
    List<Map<String, Object>> orders = new ArrayList<>();
    // ...
    return orders;
}

// 构建撤单请求
public byte[] buildCancelOrderRequest(String accountId, String orderId) {
    // 实现构建撤单请求数据包
    // ...
    return requestData;
}

// 解析撤单响应
public Map<String, Object> parseCancelOrderResponse(byte[] response) {
    // 实现解析撤单响应数据
    Map<String, Object> result = new HashMap<>();
    // ...
    return result;
}
```

### 4.5 客户端示例 (ths_api_client.py)

```python
import requests
import json

class ThsApiClient:
    def __init__(self, base_url="http://localhost:5000"):
        self.base_url = base_url
        
    def health_check(self):
        """检查API服务是否正常运行"""
        try:
            response = requests.get(f"{self.base_url}/api/health")
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def check_passport(self):
        """检查passport.dat文件是否存在"""
        try:
            response = requests.get(f"{self.base_url}/api/ths/check_passport")
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def login(self, phone, password):
        """登录同花顺账户"""
        try:
            response = requests.post(
                f"{self.base_url}/api/ths/login",
                json={"phone": phone, "password": password}
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_accounts(self):
        """获取证券账户列表"""
        try:
            response = requests.get(f"{self.base_url}/api/ths/accounts")
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def buy_stock(self, account_id, stock_code, price, quantity):
        """买入股票"""
        try:
            response = requests.post(
                f"{self.base_url}/api/ths/buy",
                json={
                    "account_id": account_id,
                    "stock_code": stock_code,
                    "price": price,
                    "quantity": quantity
                }
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def sell_stock(self, account_id, stock_code, price, quantity):
        """卖出股票"""
        try:
            response = requests.post(
                f"{self.base_url}/api/ths/sell",
                json={
                    "account_id": account_id,
                    "stock_code": stock_code,
                    "price": price,
                    "quantity": quantity
                }
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_funds(self, account_id):
        """查询资金信息"""
        try:
            response = requests.get(f"{self.base_url}/api/ths/funds", params={"account_id": account_id})
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_positions(self, account_id):
        """查询持仓信息"""
        try:
            response = requests.get(f"{self.base_url}/api/ths/positions", params={"account_id": account_id})
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_orders(self, account_id, status="all"):
        """查询委托信息"""
        try:
            response = requests.get(
                f"{self.base_url}/api/ths/orders",
                params={"account_id": account_id, "status": status}
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def cancel_order(self, account_id, order_id):
        """撤单"""
        try:
            response = requests.post(
                f"{self.base_url}/api/ths/cancel_order",
                json={"account_id": account_id, "order_id": order_id}
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}

# 示例使用
if __name__ == "__main__":
    client = ThsApiClient()
    
    # 1. 健康检查
    health_result = client.health_check()
    print("健康检查结果:", health_result)
    
    # 2. 检查passport
    passport_result = client.check_passport()
    print("Passport检查结果:", passport_result)
    
    # 如果passport不存在，先登录
    if not passport_result.get("exists", False):
        phone = input("请输入手机号: ")
        password = input("请输入密码: ")
        login_result = client.login(phone, password)
        print("登录结果:", login_result)
    
    # 3. 获取账户列表
    accounts_result = client.get_accounts()
    print("账户列表:", accounts_result)
    
    # 假设我们有一个账户ID
    if accounts_result.get("success", False) and len(accounts_result.get("accounts", [])) > 0:
        account_id = accounts_result["accounts"][0]["account_id"]
        
        # 4. 查询资金
        funds_result = client.get_funds(account_id)
        print("资金信息:", funds_result)
        
        # 5. 查询持仓
        positions_result = client.get_positions(account_id)
        print("持仓信息:", positions_result)
        
        # 6. 查询委托
        orders_result = client.get_orders(account_id)
        print("委托信息:", orders_result)
        
        # 7. 示例：买入股票
        # buy_result = client.buy_stock(account_id, "600000", 10.0, 100)
        # print("买入结果:", buy_result)
        
        # 8. 示例：卖出股票
        # sell_result = client.sell_stock(account_id, "600000", 10.5, 100)
        # print("卖出结果:", sell_result)
        
        # 9. 示例：撤单
        # if orders_result.get("success", False) and len(orders_result.get("orders", [])) > 0:
        #     order_id = orders_result["orders"][0]["order_id"]
        #     cancel_result = client.cancel_order(account_id, order_id)
        #     print("撤单结果:", cancel_result)
```

## 5. 依赖项和环境配置

### 5.1 Python依赖项 (requirements.txt)

```
Flask==2.2.5
Waitress==2.1.2
requests==2.31.0
```

### 5.2 Java依赖项

- snappy-java-1.1.10.1.jar（已存在于项目中）
- json库（用于JSON解析，可以使用org.json库）

## 6. 实现难点和解决方案

### 6.1 协议解析

同花顺客户端与服务器之间采用自定义二进制协议通信，需要仔细分析协议结构。可以使用Wireshark等工具捕获数据包进行分析。

### 6.2 数据加密

同花顺使用多层加密机制保护数据安全，包括DES对称加密和数据混淆。需要逆向分析加密算法并在Java代码中实现。

### 6.3 会话管理

需要正确处理登录会话，包括passport.dat文件的生成、加载和使用，确保API请求能够通过身份验证。

### 6.4 错误处理

添加完善的错误处理机制，包括网络异常、服务器错误、参数错误等情况的处理和提示。

## 7. 测试和验证

1. **单元测试**：为每个API接口编写单元测试
2. **集成测试**：测试完整的交易流程
3. **模拟环境测试**：在模拟交易环境中验证功能
4. **实盘测试**：小金额实盘测试（谨慎操作）

## 8. 安全注意事项

1. **敏感信息保护**：不要在代码中硬编码用户名、密码等敏感信息
2. **API访问控制**：考虑添加API访问控制机制，如API密钥验证
3. **交易安全**：添加交易确认机制，防止误操作
4. **合规性**：确保遵循相关法律法规，仅用于个人学习和研究

## 9. 参考资源

1. GitHub项目：skyformat99/ths_trade - 同花顺自动化交易接口
2. 同花顺客户端网络协议分析
3. Java网络编程相关知识

## 10. 后续优化方向

1. 添加交易策略管理功能
2. 实现定时任务和条件单功能
3. 增加交易日志和审计功能
4. 添加风控机制
5. 优化性能和并发处理能力