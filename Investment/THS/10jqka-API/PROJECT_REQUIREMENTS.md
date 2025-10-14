# 10jqka-API 项目需求文档

## 1. 项目概述

### 1.1 项目背景
10jqka-API是一个针对同花顺金融客户端协议的逆向工程项目，旨在为开发者提供与同花顺服务器进行通信的标准化接口，简化金融数据获取和交易操作的复杂度。

### 1.2 项目目标
- 实现同花顺客户端登录协议的完整分析与复现
- 提供简单易用的API接口，屏蔽底层协议细节
- 支持持久化登录状态，提高用户体验
- 建立稳定可靠的数据通信框架，为后续扩展数据获取功能奠定基础

### 1.3 应用场景
- 金融数据分析平台的数据获取
- 自动化交易系统的底层通信组件
- 个人投资辅助工具的后端服务
- 金融市场监控与预警系统

## 2. 系统架构

### 2.1 整体架构
10jqka-API项目采用多层架构设计，主要包含以下层次：

1. **核心通信层**：基于Java实现的底层通信模块，负责与同花顺服务器直接交互
2. **API服务层**：基于Python Flask实现的Web服务，封装Java核心功能为RESTful API
3. **客户端层**：Python客户端库，提供简洁的方法调用API服务

### 2.2 技术栈
- **核心通信层**：Java 21、Maven、snappy-java 1.1.10.1
- **API服务层**：Python 3.x、Flask 2.2.5、Waitress
- **客户端层**：Python 3.x、requests
- **通信协议**：TCP/IP、自定义二进制协议
- **数据存储**：本地文件（passport.dat）

### 2.3 系统拓扑图
```
客户端应用
    ↓
Python客户端库 (ths_api_client.py)
    ↓
Flask API服务 (app.py)
    ↓
Java核心通信模块 (ThsCore.java)
    ↓
同花顺服务器 (mobi2.hexin.cn:9528)
```

## 3. 功能需求

### 3.1 核心通信功能

#### 3.1.1 服务器连接管理
- 建立与同花顺服务器的TCP连接
- 维护连接状态，处理断连重连
- 提供连接状态查询接口

#### 3.1.2 数据收发机制
- 实现同花顺自定义协议的数据打包与发送
- 实现数据接收与解析
- 支持数据包类型识别与分类处理

### 3.2 认证与安全功能

#### 3.2.1 设备信息初始化
- 收集并生成设备指纹信息
- 向服务器发送设备认证信息
- 处理设备认证响应

#### 3.2.2 登录认证
- 支持手机号+短信验证码登录
- 支持密码登录（预留）
- 处理登录成功/失败响应

#### 3.2.3 持久化登录
- 登录成功后生成passport.dat文件保存登录凭证
- 支持从passport.dat文件读取凭证自动登录
- 提供passport.dat文件存在性检查

### 3.3 API服务功能

#### 3.3.1 健康检查接口
- 提供API服务运行状态查询
- 返回服务运行时间戳

#### 3.3.2 Passport检查接口
- 检查passport.dat文件是否存在
- 返回文件路径和存在状态

#### 3.3.3 登录接口
- 提供触发同花顺登录流程的API
- 支持短信验证码输入（通过控制台交互）
- 返回登录结果和状态信息

## 4. 技术需求

### 4.1 性能需求
- API响应时间：≤500ms（非登录操作）
- 登录操作最大响应时间：≤30秒
- 支持并发请求数：≥10个并发连接

### 4.2 可靠性需求
- 服务可用性：≥99%
- 连接稳定性：支持长时间保持连接
- 错误处理：完善的异常捕获和错误返回机制

### 4.3 安全需求
- 数据传输：支持加密通信
- 凭证存储：安全存储登录凭证
- 访问控制：简单的API访问控制机制

### 4.4 可扩展性需求
- 模块化设计：便于后续功能扩展
- 接口抽象：定义清晰的接口规范
- 配置管理：集中式配置管理机制

## 5. 接口说明

### 5.1 RESTful API接口

#### 5.1.1 健康检查接口
- **URL**: `/api/ths/health`
- **方法**: GET
- **参数**: 无
- **返回**: 
  ```json
  {
    "success": true,
    "status": "running",
    "timestamp": "2023-10-01 12:00:00"
  }
  ```

#### 5.1.2 Passport检查接口
- **URL**: `/api/ths/check_passport`
- **方法**: GET
- **参数**: 无
- **返回**: 
  ```json
  {
    "success": true,
    "exists": true,
    "path": "d:\\Xander\\git_projects\\Investment\\Investment\\THS\\10jqka-API\\passport.dat"
  }
  ```

#### 5.1.3 登录接口
- **URL**: `/api/ths/login`
- **方法**: GET
- **参数**: 无
- **返回**: 
  ```json
  {
    "success": true,
    "message": "登录成功",
    "passport_exists": false
  }
  ```
  或需要验证码时：
  ```json
  {
    "success": false,
    "need_verification": true,
    "message": "需要输入短信验证码",
    "process_id": 12345
  }
  ```

### 5.2 Java核心接口

#### 5.2.1 ThsCore类主要方法
- `connectThsServer()`: 连接同花顺服务器
- `sendDeviceInfo()`: 发送设备初始化信息
- `sendSmsLogin(String phoneNumber)`: 发送登录验证码请求
- `verifyCheckCode(String phoneNumber, String checkCode, Integer loginType)`: 验证登录验证码
- `passportLogin(byte[] passport)`: 使用passport数据自动登录

### 5.3 Python客户端接口

#### 5.3.1 ThsApiClient类主要方法
- `health_check()`: 检查API服务器健康状态
- `check_passport()`: 检查passport.dat文件是否存在
- `login()`: 调用登录API

## 6. 配置需求

### 6.1 服务器配置
- 同花顺服务器地址: `mobi2.hexin.cn`
- 服务器端口: `9528`
- API服务端口: `5000`

### 6.2 环境配置
- Java运行环境: JDK 21或更高版本
- Python环境: Python 3.6或更高版本
- Maven: 3.x或更高版本

### 6.3 依赖配置
- Java依赖: snappy-java 1.1.10.1
- Python依赖: Flask 2.2.5, requests

## 7. 部署与运行

### 7.1 部署要求
- 操作系统: Windows/Linux/MacOS
- 内存要求: ≥512MB
- 磁盘空间: ≥100MB

### 7.2 启动流程
1. **启动API服务器**:
   ```bash
   cd d:\Xander\git_projects\Investment\Investment\THS\10jqka-API\ths_api_server
   python app.py
   ```

2. **使用客户端调用API**:
   ```bash
   cd d:\Xander\git_projects\Investment\Investment\THS\10jqka-API\ths_api_server
   python ths_api_client.py
   ```

### 7.3 直接运行Java核心程序
```bash
cd d:\Xander\git_projects\Investment\Investment\THS\10jqka-API
java -cp "lib/snappy-java-1.1.10.1.jar;bin;." Main
```

## 8. 监控与维护

### 8.1 日志管理
- API服务器日志输出到控制台
- Java核心程序日志输出到控制台
- 支持日志级别调整（预留）

### 8.2 常见问题处理
- 连接失败: 检查网络连接和服务器地址配置
- 登录失败: 确认手机号正确性和验证码输入
- passport.dat生成失败: 检查文件权限和磁盘空间

## 9. 扩展规划

### 9.1 功能扩展路线图
1. 第一阶段: 完成登录功能和基础API（已实现）
2. 第二阶段: 扩展股票行情数据获取功能
3. 第三阶段: 实现交易相关功能
4. 第四阶段: 添加用户认证和权限控制

### 9.2 技术扩展方向
- 支持更多金融数据源
- 实现WebSocket实时数据推送
- 优化并发处理能力
- 添加数据缓存机制

## 10. 注意事项

1. 本项目仅供学习和研究使用，请勿用于商业用途
2. 遵守相关法律法规，合法使用金融数据
3. 保护用户隐私和数据安全
4. 定期更新依赖库和安全补丁
5. 注意监控API调用频率，避免触发服务器限制