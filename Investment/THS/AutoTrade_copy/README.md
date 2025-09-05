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
└── README.md              # 操作手册
```

## 技术栈
- **前端**: React、TypeScript、Ant Design、axios
- **后端**: Flask、SQLAlchemy、SQLite
- **数据交互**: RESTful API

## 环境搭建
### 前端环境
1. 安装Node.js (建议版本16+)
2. 无需手动安装依赖，启动脚本会自动安装

### 后端环境
1. 安装Python (建议版本3.8+)
2. 无需手动安装依赖，启动脚本会自动安装

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

3. **trades**: 交易记录表
   - id: 交易ID
   - strategy_id: 所属策略ID
   - stock_code: 股票代码
   - stock_name: 股票名称
   - trade_type: 交易类型(buy/sell)
   - quantity: 交易数量
   - price: 交易价格
   - amount: 交易金额
   - trade_date: 交易日期
   - reason: 交易理由

4. **performances**: 策略性能表
   - id: 性能ID
   - strategy_id: 所属策略ID
   - date: 日期
   - return_rate: 收益率
   - sharpe_ratio: 夏普比率
   - max_drawdown: 最大回撤
   - volatility: 波动率
   - benchmark_return: 基准收益率

## 开发说明
### 前端开发
1. 组件开发: 在`src/components`目录下创建新组件
2. 页面开发: 在`src/pages`目录下创建新页面
3. API调用: 在`src/services`目录下定义API服务
4. 路由配置: 在`src/App.tsx`中配置路由

### 后端开发
1. API开发: 在`routes`目录下创建新的路由文件
2. 模型定义: 在`models.py`中定义新的数据模型
3. 业务逻辑: 在路由处理函数中实现业务逻辑
4. 数据库操作: 使用SQLAlchemy ORM进行数据库操作

## 注意事项
1. 首次启动服务时，后端脚本会自动初始化数据库并插入测试数据
2. 后端服务默认使用SQLite数据库，数据存储在`backend/investment.db`文件中
3. 前后端服务启动后，可通过浏览器访问`http://localhost:3000`使用应用
4. 若需要修改数据库结构，可修改`models.py`文件后重新运行`init_db.py`脚本

## 后续优化建议
1. 添加用户认证和权限管理
2. 实现数据可视化图表展示
3. 增加策略回测功能
4. 优化移动端适配
5. 添加更多技术指标分析
6. 实现数据导入导出功能

希望本操作手册能帮助您快速上手使用投资项目。如有任何问题，请查看代码注释或联系开发人员。

  - 使用`colorlog`库为日志添加颜色，便于区分不同级别的日志。

#### 3.6.2 通知 (`utils/notification.py`)
- **功能**：在关键操作时发送通知。
- **实现方式**：
  - 使用`plyer`库发送桌面通知。
  - 可扩展为支持邮件、短信等其他通知方式。

## 4. 关键流程
### 4.1 获取调仓信息
1. **组合调仓**：
   - `组合_今天调仓.py`：从同花顺平台获取指定组合的最新调仓信息。
   - 过滤掉创业板和科创板的股票。
   - 将结果保存到`COMBINATION_TODAY_ADJUSTMENT_FILE`文件中。

2. **策略调仓**：
   - `策略_今天调仓.py`：从同花顺平台获取指定策略的最新调仓信息。
   - 过滤掉创业板和科创板的股票。
   - 将结果保存到`STRATEGY_TODAY_ADJUSTMENT_FILE`文件中。

### 4.2 处理调仓信息
- `数据处理.py`：读取上述两个文件中的调仓信息，处理并保存到Excel文件中。
- 清空昨天的数据，确保只保存今天的调仓信息。

### 4.3 执行交易操作
- `自动化交易.py`：启动同花顺APP，连接设备，初始化页面对象。
- 根据调仓信息执行买入或卖出操作。
- 记录操作历史，并在每次操作后发送通知。

### 4.4 调度与监控
- `scheduler.py`：设置定时任务，在指定时间段内定期执行调仓信息获取和交易操作。
- 记录下一次任务的执行时间，并在任务结束时发送通知。

## 5. 技术选型
- **编程语言**：Python
- **第三方库**：
  - `requests`：用于发起HTTP请求。
  - `pandas`：用于处理和保存Excel文件。
  - `uiautomator2`：用于控制同花顺APP的UI操作。
  - `schedule`：用于设置定时任务。
  - `logging`和`colorlog`：用于日志记录。
  - `plyer`：用于发送桌面通知。

## 6. 未来扩展
- **多平台支持**：扩展支持更多交易平台，如雪球、东方财富等。
- **多种通知方式**：增加邮件、短信等通知方式。
- **更复杂的交易策略**：支持更多复杂的交易策略，如网格交易、趋势跟踪等。
- **性能优化**：优化代码性能，减少响应时间，提高稳定性。

---

以上是详细的项目需求文档，涵盖了项目的整体架构和各个模块的具体实现细节。希望这份文档能够帮助你更好地理解项目的功能和技术实现。
量化投资自动化交易/
├── config/                  # 配置文件
│   └── settings.py          # 全局配置
├── logs/                    # 日志文件
│   ├── ths_auto_trade.log
│   ├── 策略_今天调仓.log
│   └── 组合_今天调仓.log
├── data/                    # 数据文件
│   ├── operation_history.csv
│   ├── 策略今天调仓.xlsx
│   └── 组合今天调仓.xlsx
├── scripts/                 # 脚本文件
│   ├── ths_main.py          # 主程序
│   ├── 策略_今天调仓.py      # 策略调仓脚本
│   └── 组合_今天调仓.py      # 组合调仓脚本
├── utils/                   # 工具类和辅助函数
│   ├── file_monitor.py      # 文件监控工具
│   ├── notification.py      # 通知工具
│   ├── scheduler.py         # 定时任务工具
│   └── ths_logger.py        # 日志工具
├── pages/                   # 页面操作类
│   └── ths_page.py          # 同花顺页面操作类
└── README.md                # 项目说明文档
