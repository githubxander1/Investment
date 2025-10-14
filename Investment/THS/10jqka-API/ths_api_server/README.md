# 同花顺API服务器与客户端

本项目提供了一个基于Flask的API服务器，用于封装同花顺Java程序的功能，并提供Python客户端进行测试和调用。

## 功能特点

- 提供RESTful API接口访问同花顺功能
- 自动登录同花顺服务器
- 检查passport.dat文件状态
- 支持健康检查

## 目录结构

```
ths_api_server/
├── app.py           # Flask API服务器主文件
├── ths_api_client.py # Python API客户端
├── requirements.txt # 项目依赖
└── README.md        # 使用说明
```

## 环境准备

1. 确保已安装Python 3.7+和pip
2. 确保Java环境已正确配置（用于运行同花顺Java程序）
3. 确保同花顺项目已按之前的配置正确设置，包括passport.dat文件位置

## 安装依赖

```bash
cd ths_api_server
pip install -r requirements.txt
```

## 启动API服务器

```bash
python app.py
```

服务器默认在`http://localhost:5000`启动。

## API接口说明

### 健康检查

```
GET /api/ths/health
```

**响应示例：**
```json
{
  "success": true,
  "status": "running",
  "timestamp": "2023-11-10 14:45:30"
}
```

### 检查passport.dat文件

```
GET /api/ths/check_passport
```

**响应示例：**
```json
{
  "success": true,
  "exists": true,
  "path": "d:\\Xander\\git_projects\\Investment\\passport.dat"
}
```

### 同花顺登录

```
GET /api/ths/login
```

**响应示例：**
```json
{
  "success": true,
  "message": "登录成功",
  "passport_exists": true
}
```

## 使用Python客户端

```bash
python ths_api_client.py
```

客户端会自动测试所有API接口，包括健康检查、passport.dat文件检查和同花顺登录。

## 注意事项

1. 如果是首次登录（没有passport.dat文件），可能需要手动输入短信验证码
2. 服务器运行时请确保Java环境正常
3. 默认使用Waitress作为生产服务器，也可以使用Flask开发服务器

## 扩展建议

1. 添加更多的API接口来支持同花顺的其他功能
2. 实现更完善的错误处理机制
3. 添加用户认证和权限控制
4. 优化日志记录和监控功能