# 投资项目操作手册

## 项目概述
本投资项目是一个前后端分离的应用，使用React作为前端框架，Flask作为后端框架，SQLite作为数据库。项目提供了策略管理、持仓分析、交易记录和性能评估等功能。

## 项目结构
```
AutoTrade/
├── frontend/              # 前端React项目
│   ├── public/            # 静态资源
│   ├── src/               # 源代码
│   │   ├── components/    # 组件
│   │   ├── pages/         # 页面
│   │   ├── routes/        # 路由
│   │   ├── services/      # API服务
│   │   ├── types.ts       # 类型定义
│   │   ├── App.tsx        # 主应用组件
│   │   └── index.tsx      # 入口文件
│   ├── package.json       # 前端依赖
│   └── start_frontend.bat # 前端启动脚本
├── backend/               # 后端Flask项目
│   ├── routes/            # API路由
│   ├── app.py             # Flask应用入口
│   ├── models.py          # 数据库模型
│   ├── init_db.py         # 数据库初始化脚本
│   ├── requirements.txt   # 后端依赖
│   └── start_backend.bat  # 后端启动脚本
├── websocket/             # WebSocket实时通信版本
│   ├── websocket_server.py # WebSocket服务器
│   └── websocket_client.py # WebSocket客户端示例
└── README.md              # 操作手册
```

## 技术栈
- **前端**: React、TypeScript、Ant Design、axios
- **后端**: Flask、SQLAlchemy、SQLite
- **实时通信**: WebSocket
- **数据交互**: RESTful API + WebSocket

## 环境搭建
### 前端环境
1. 安装Node.js (建议版本16+)
2. 无需手动安装依赖，启动脚本会自动安装

### 后端环境
1. 安装Python (建议版本3.8+)
2. 无需手动安装依赖，启动脚本会自动安装

### WebSocket环境
1. 安装Python (建议版本3.8+)
2. 安装依赖: `pip install websockets`

## 快速启动
### 启动后端服务
1. 打开命令行窗口
2. 进入`AutoTrade/backend`目录
3. 双击运行`start_backend.bat`脚本
4. 脚本会自动安装依赖、初始化数据库并启动后端服务
5. 后端服务默认运行在`http://localhost:5000`

### 启动前端服务
1. 打开新的命令行窗口
2. 进入`AutoTrade/frontend`目录
3. 双击运行`start_frontend.bat`脚本
4. 脚本会自动安装依赖并启动前端服务
5. 前端服务默认运行在`http://localhost:3000`

### 启动WebSocket服务
1. 打开命令行窗口
2. 进入`AutoTrade`目录
3. 运行命令: `python websocket_server.py`
4. WebSocket服务器将启动在 `ws://localhost:8765`

## WebSocket API
### 服务器端点
- **地址**: `ws://localhost:8765`
- **协议**: WebSocket

### 客户端命令
1. **获取系统状态**
   ```json
   {
     "command": "get_status"
   }
   ```

2. **执行交易任务**
   ```json
   {
     "command": "execute_tasks"
   }
   ```

### 服务器消息类型
1. **欢迎消息**
   ```json
   {
     "type": "welcome",
     "message": "已连接到AutoTrade WebSocket服务器",
     "timestamp": "YYYY-MM-DDTHH:mm:ss.ssssss"
   }
   ```

2. **任务状态**
   ```json
   {
     "type": "task_status",
     "status": "started|completed|error",
     "message": "任务相关信息",
     "timestamp": "YYYY-MM-DDTHH:mm:ss.ssssss"
   }
   ```

3. **系统状态**
   ```json
   {
     "type": "system_status",
     "time": "YYYY-MM-DDTHH:mm:ss.ssssss",
     "is_trading_day": true|false,
     "connected_clients": 1,
     "morning_signal_checked": true|false
   }
   ```

4. **错误消息**
   ```json
   {
     "type": "error",
     "message": "错误信息",
     "timestamp": "YYYY-MM-DDTHH:mm:ss.ssssss"
   }
   ```

## 功能说明
### 1. 交易筛选
- 查看不同策略的交易记录
- 根据股票代码、交易类型、日期范围筛选交易
- 查看交易详情和理由

### 2. 策略持仓
- 查看各策略当前持仓情况
- 按行业、板块分析持仓分布
- 查看单只股票的持仓详情

### 3. 历史调仓
- 查看策略的历史调仓记录
- 分析调仓效果和原因
- 对比不同时期的持仓变化

### 4. 策略对比
- 对比多个策略的性能指标
- 查看策略的收益率、夏普比率、最大回撤等指标
- 生成策略对比图表

## 数据库结构
### 主要表结构
1. **strategies**: 策略信息表
   - id: 策略ID
   - name: 策略名称
   - description: 策略描述
   - created_at: 创建时间
   - updated_at: 更新时间

2. **holdings**: 持仓信息表
   - id: 持仓ID
   - strategy_id: 所属策略ID
   - stock_code: 股票代码
   - stock_name: 股票名称
   - quantity: 持仓数量
   - price: 持仓价格
   - value: 持仓市值
   - weight: 持仓权重
   - industry: 所属行业
   - sector: 所属板块
   - updated_at: 更新时间

3. **transactions**: 交易记录表
   - id: 交易ID
   - strategy_id: 所属策略ID
   - stock_code: 股票代码
   - stock_name: 股票名称
   - trade_type: 交易类型 (买入/卖出)
   - quantity: 交易数量
   - price: 交易价格
   - amount: 交易金额
   - reason: 交易理由
   - trade_date: 交易日期
   - created_at: 创建时间

## WebSocket通信优势
1. **实时性**: 通过WebSocket实现服务器主动推送消息，无需客户端轮询
2. **高效性**: 减少了不必要的HTTP请求，降低了网络开销
3. **双向通信**: 支持服务器和客户端之间的双向实时通信
4. **状态同步**: 多个客户端可以实时同步系统状态和任务进度