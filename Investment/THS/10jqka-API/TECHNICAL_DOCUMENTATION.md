# 10jqka-API 技术文档

## 1. 项目概述

本技术文档详细描述10jqka-API项目的内部实现机制、协议分析结果和开发扩展方法，为开发者提供深入理解和扩展该项目的技术指导。

## 2. 核心模块详解

### 2.1 连接管理模块

连接管理模块负责与同花顺服务器建立和维护TCP连接，主要功能在`ThsCore`类中实现。

**主要方法**: 

```java
public boolean connectThsServer() {
    try {
        socket = new Socket(Constant.CONNECT_HOST, Constant.CONNECT_PORT);
        outputStream = socket.getOutputStream();
        inputStream = socket.getInputStream();
        dataHandler = new ewa();
        System.out.println("连接同花顺服务器成功");
    } catch (Exception e) {
        System.out.println("连接同花顺服务器失败");
        return false;
    }
    return true;
}
```

连接成功后，创建`ewa`实例作为数据处理器，负责后续的数据收发和解析工作。

### 2.2 登录认证模块

登录认证模块实现了完整的同花顺客户端登录流程，包括设备信息初始化、短信验证码登录和持久化登录。

#### 2.2.1 设备信息初始化

```java
// 发送相关的设备初始化信息
public boolean sendDeviceInfo() {
    // 实现设备信息收集和发送逻辑
    // ...
}
```

此方法负责收集设备指纹信息（如设备型号、系统版本、网络环境等），并将其发送到服务器进行设备认证。

#### 2.2.2 短信验证码登录

```java
// 发送登录验证包
public void sendSmsLogin(String phoneNumber) {
    // 实现向指定手机号发送验证码的逻辑
    // ...
}

// 验证收到的验证码
public boolean verifyCheckCode(String phoneNumber, String checkCode, int i) {
    // 实现验证码验证逻辑
    // ...
}
```

这两个方法协同工作，完成手机号+短信验证码的登录流程。

#### 2.2.3 持久化登录

```java
// 使用passport登录
public void passportLogin(byte[] passportData) {
    // 实现使用保存的登录凭证自动登录的逻辑
    // ...
}
```

登录成功后，系统会将登录凭证保存到`passport.dat`文件中，下次启动时自动读取并使用该凭证登录。

### 2.3 数据处理模块

数据处理模块负责对收发的数据进行编码、解码和解析，主要由`ewa`类实现。

```java
// 数据处理器
public class ewa {
    // 解析服务器返回的数据
    public Object a(byte[] data, int offset, int length, int type, int subType, byte[] extraData) {
        // 实现数据解析逻辑
        // ...
    }
    
    // 其他数据处理方法
    // ...
}
```

### 2.4 加密解密模块

加密解密模块负责对敏感数据进行加密和解密处理，主要由`fjc`类实现。

```java
// 加密工具类中的方法示例
public String b(String input) {
    // 实现数据加密逻辑
    // ...
}
```

## 3. 协议分析结果

### 3.1 通信协议结构

同花顺客户端与服务器之间采用自定义的二进制协议进行通信，协议结构主要包括：

- **包头**: 包含消息长度、消息类型等基本信息
- **包体**: 包含具体的业务数据
- **包尾**: 包含校验信息等

### 3.2 登录协议流程

1. **建立TCP连接**: 客户端连接到同花顺服务器
2. **发送设备信息**: 客户端发送设备指纹等信息
3. **请求验证码**: 客户端发送获取短信验证码的请求
4. **验证身份**: 客户端发送手机号和验证码进行身份验证
5. **获取会话**: 验证成功后，服务器返回会话信息
6. **保存凭证**: 客户端保存登录凭证到本地文件

### 3.3 数据加密机制

同花顺协议采用多层加密机制保护数据安全：

1. **基础加密**: 使用DES等对称加密算法
2. **数据混淆**: 采用特定算法对数据进行混淆处理
3. **校验机制**: 使用校验和等方式确保数据完整性

## 4. 扩展开发指南

### 4.1 获取股票行情数据

要扩展项目获取股票行情数据，可以按照以下步骤进行：

1. **分析数据包结构**: 使用Wireshark等工具捕获同花顺客户端请求行情数据的数据包

2. **模拟数据请求**: 参考捕获的数据包，构造并发送类似的请求

```java
public void requestStockData(String stockCode) {
    try {
        // 构造请求数据包
        byte[] requestData = constructStockDataRequest(stockCode);
        
        // 发送请求
        outputStream.write(requestData);
        outputStream.flush();
        
        // 接收并解析响应
        byte[] responseData = receiveResponse();
        processStockDataResponse(responseData);
    } catch (Exception e) {
        e.printStackTrace();
    }
}

private byte[] constructStockDataRequest(String stockCode) {
    // 构造股票数据请求包的具体实现
    // ...
    return requestData;
}

private void processStockDataResponse(byte[] responseData) {
    // 使用dataHandler解析响应数据
    Object result = dataHandler.a(responseData, 0, responseData.length, 0, 2, null);
    
    // 处理解析结果
    if (result instanceof StuffTableStruct) {
        StuffTableStruct tableData = (StuffTableStruct) result;
        // 提取和使用表格数据
        // ...
    }
}
```

### 4.2 使用Frida Hook辅助开发

使用Frida工具Hook同花顺客户端的关键函数，可以帮助理解数据处理逻辑：

```javascript
// Frida脚本示例，用于Hook StuffTableStruct类的方法
Java.perform(function () {
    var StuffTableStruct = Java.use('thsCrack.StuffTableStruct');
    
    // Hook a方法，观察数据解析过程
    StuffTableStruct.a.overload('int').implementation = function (param) {
        console.log('StuffTableStruct.a called with param: ' + param);
        var result = this.a(param);
        console.log('StuffTableStruct.a result: ' + result);
        return result;
    };
});
```

### 4.3 添加新功能的步骤

1. **分析需求**: 明确需要实现的功能和数据流程
2. **协议分析**: 使用抓包工具分析相关协议
3. **代码实现**: 根据分析结果实现相应的功能模块
4. **测试验证**: 测试实现的功能是否正常工作
5. **文档更新**: 更新相关文档说明新功能

## 5. 代码优化建议

### 5.1 错误处理优化

当前代码中的错误处理较为简单，可以添加更详细的错误日志和异常处理机制：

```java
// 优化前
public boolean connectThsServer() {
    try {
        socket = new Socket(Constant.CONNECT_HOST, Constant.CONNECT_PORT);
        // ...
    } catch (Exception e) {
        System.out.println("连接同花顺服务器失败");
        return false;
    }
    return true;
}

// 优化后
public boolean connectThsServer() {
    try {
        socket = new Socket(Constant.CONNECT_HOST, Constant.CONNECT_PORT);
        // ...
    } catch (UnknownHostException e) {
        System.err.println("无法解析服务器地址: " + Constant.CONNECT_HOST);
        e.printStackTrace();
        return false;
    } catch (IOException e) {
        System.err.println("连接服务器失败，可能是网络问题或服务器不可用");
        e.printStackTrace();
        return false;
    } catch (Exception e) {
        System.err.println("连接服务器时发生未知错误");
        e.printStackTrace();
        return false;
    }
    return true;
}
```

### 5.2 配置管理优化

将硬编码的配置参数提取到配置文件中，便于维护和修改：

```java
// 从配置文件读取参数
public class ConfigManager {
    private static Properties properties = new Properties();
    
    static {
        try (InputStream input = ConfigManager.class.getClassLoader().getResourceAsStream("config.properties")) {
            if (input != null) {
                properties.load(input);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
    
    public static String getProperty(String key, String defaultValue) {
        return properties.getProperty(key, defaultValue);
    }
    
    public static int getIntProperty(String key, int defaultValue) {
        String value = properties.getProperty(key);
        if (value != null) {
            try {
                return Integer.parseInt(value);
            } catch (NumberFormatException e) {
                // ignore
            }
        }
        return defaultValue;
    }
}
```

### 5.3 线程安全优化

当前代码在多线程环境下可能存在安全问题，可以添加线程安全机制：

```java
// 使用线程安全的集合和同步机制
public class ThreadSafeThsCore extends ThsCore {
    private final ConcurrentHashMap<String, Object> sharedData = new ConcurrentHashMap<>();
    
    @Override
    public synchronized boolean verifyCheckCode(String phoneNumber, String checkCode, int i) {
        // 线程安全的验证码验证实现
        // ...
        return super.verifyCheckCode(phoneNumber, checkCode, i);
    }
    
    // 其他线程安全的方法
    // ...
}
```

## 6. 常见问题解决

### 6.1 连接服务器失败

- 检查网络连接是否正常
- 确认同花顺服务器地址和端口是否正确
- 检查防火墙设置是否阻止了连接

### 6.2 登录失败

- 确认手机号格式是否正确
- 检查验证码是否输入正确
- 验证`passport.dat`文件是否损坏或过期

### 6.3 数据解析错误

- 检查数据包格式是否正确
- 确认使用了正确的解析方法和参数
- 验证同花顺客户端版本与当前代码是否兼容

## 7. 版本兼容性说明

当前项目基于特定版本的同花顺客户端进行逆向分析，可能与其他版本存在兼容性问题。当同花顺客户端更新后，可能需要重新分析协议并更新代码。

## 8. 附录

### 8.1 重要类索引

| 类名 | 主要功能 | 文件位置 |
|------|---------|---------|
| ThsCore | 核心功能实现 | src/main/java/core/ThsCore.java |
| Main | 程序入口 | src/main/java/Main.java |
| ewa | 数据处理器 | src/main/java/thsCrack/ewa.java |
| fjc | 加密工具 | src/main/java/thsCrack/fjc.java |
| StuffTableStruct | 数据表结构 | src/main/java/thsCrack/StuffTableStruct.java |