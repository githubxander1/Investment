# T0交易系统优化方案

## 项目分析报告

### 当前架构概览
- **项目定位**：日内T+0短线交易系统（美的集团、中信证券、海康威视）
- **交易时段**：9:30-15:00
- **数据源**：AkShare / 东方财富
- **已实现指标**：
  1. `comprehensive_t0_strategy` - 综合T0策略
  2. `price_ma_deviation` - 价格均线偏离（基础版）
  3. `price_ma_deviation_optimized` - 价格均线偏离（优化版）

### 发现的主要问题

#### 1. 数据层问题
- ❌ 当前使用CSV存储，查询效率低
- ❌ 缺少实时数据更新机制
- ❌ 数据验证和完整性检查不足
- ❌ `data2dfcf.py`的东方财富接口实现不完整

#### 2. 可视化层问题
- ❌ `t0_data_visualizer.py`代码过长（1463行），维护困难
- ❌ 指标导入逻辑复杂，大量try-except嵌套
- ❌ 模拟指标与真实指标混合
- ❌ 图表更新性能待优化
- ❌ 缺少专业交互功能（十字光标、数据标注等）
- ❌ 播放功能存在线程安全隐患

#### 3. 架构设计问题
- ❌ 缺少分层架构（业务逻辑与UI混合）
- ❌ 没有插件化的指标加载机制
- ❌ 配置管理散落各处
- ❌ 缺少单元测试

---

## 优化方案

### 🎯 一、数据存储优化

#### 方案：SQLite（推荐）

**选择理由**：
- ✅ 轻量级，零配置
- ✅ 支持SQL查询，高效索引
- ✅ 事务支持，保证数据一致性
- ✅ 适合时间序列数据
- ✅ 可导出CSV备份

**对比其他方案**：
- ❌ Redis：需要独立服务，过于重量级
- ❌ CSV：查询慢，不支持并发，无索引

**数据库设计**：

```sql
-- 分时数据表
CREATE TABLE minute_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_code TEXT NOT NULL,
    datetime TEXT NOT NULL,
    open REAL NOT NULL,
    close REAL NOT NULL,
    high REAL NOT NULL,
    low REAL NOT NULL,
    volume INTEGER NOT NULL,
    amount REAL NOT NULL,
    avg_price REAL,
    change_pct REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(stock_code, datetime)
);

CREATE INDEX idx_stock_datetime ON minute_data(stock_code, datetime);
CREATE INDEX idx_datetime ON minute_data(datetime);

-- 交易信号表
CREATE TABLE trading_signals (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stock_code TEXT NOT NULL,
    datetime TEXT NOT NULL,
    indicator_name TEXT NOT NULL,
    signal_type TEXT NOT NULL CHECK(signal_type IN ('BUY', 'SELL')),
    price REAL NOT NULL,
    score REAL,
    metadata TEXT,  -- JSON格式
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE INDEX idx_signal_stock_datetime ON trading_signals(stock_code, datetime);
CREATE INDEX idx_signal_indicator ON trading_signals(indicator_name);

-- 系统配置表
CREATE TABLE system_config (
    key TEXT PRIMARY KEY,
    value TEXT NOT NULL,
    description TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**数据迁移计划**：
1. 创建SQLite数据库
2. 编写CSV导入脚本
3. 迁移现有缓存数据（`cache/fenshi_data/*.csv`）
4. 保留CSV作为备份格式

---

### 🏗️ 二、架构重构

#### 分层架构设计

```
Investment/T0/
├── core/                    # 核心层（新增）
│   ├── __init__.py
│   ├── data_manager.py      # 数据管理（SQLite CRUD）
│   ├── indicator_loader.py  # 指标动态加载器
│   ├── config_manager.py    # 配置管理
│   └── event_bus.py         # 事件总线（用于组件通信）
│
├── data/                    # 数据源层（新增）
│   ├── __init__.py
│   ├── base_source.py       # 数据源抽象基类
│   ├── akshare_source.py    # AkShare实现
│   ├── dfcf_source.py       # 东方财富实现（优化）
│   └── cache_source.py      # 缓存数据源（读取SQLite/CSV）
│
├── indicators/              # 指标层（已有，保持不变）
│   ├── comprehensive_t0_strategy.py
│   ├── price_ma_deviation.py
│   ├── price_ma_deviation_optimized.py
│   └── ...
│
├── ui/                      # UI层（重构）
│   ├── __init__.py
│   ├── main_window.py       # 主窗口（tkinter）
│   ├── components/
│   │   ├── chart_panel.py   # 图表面板（matplotlib）
│   │   ├── control_panel.py # 控制面板
│   │   ├── indicator_selector.py  # 指标选择器
│   │   └── status_bar.py    # 状态栏
│   └── utils/
│       ├── chart_helper.py  # 图表辅助函数
│       └── theme.py         # 主题配置
│
├── monitor/                 # 监控层（已有）
│   ├── signal_detector.py
│   └── ...
│
├── utils/                   # 工具层（已有）
│   ├── data_handler.py
│   └── ...
│
├── config/                  # 配置层（已有）
│   └── settings.py
│
├── tests/                   # 测试层（已有）
│   └── ...
│
├── db/                      # 数据库文件（新增）
│   └── t0_trading.db        # SQLite数据库
│
└── t0_app.py               # 应用入口（新增）
```

#### 核心模块说明

**1. core/data_manager.py**
- 封装SQLite操作
- 提供CRUD接口
- 支持批量插入/查询
- 数据验证

**2. core/indicator_loader.py**
- 自动发现indicators目录下的指标
- 动态加载指标模块
- 验证指标接口（analyze函数签名）
- 提供指标元数据

**3. data/base_source.py**
- 定义数据源接口
- 统一数据格式
- 错误处理

**4. ui/main_window.py**
- 主窗口框架
- 组件组装
- 事件分发

---

### 🎨 三、UI界面优化

#### 布局设计（参考同花顺/通达信）

```
┌─────────────────────────────────────────────────────────────────┐
│ 菜单栏: 文件 | 数据 | 指标 | 工具 | 帮助                         │
├─────────────────────────────────────────────────────────────────┤
│ 工具栏:                                                          │
│  [股票▼美的集团] [日期▼2025-10-24] [🔄刷新] [●实时监控]        │
│  状态: 就绪 | 数据: 242条 | 信号: 买3 卖2 | 时间: 14:30:00     │
├─────────────────────────────────────────────────────────────────┤
│                      主图区域 (60%)                              │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │   分时走势图 + 均价线                                      │  │
│  │   - 鼠标十字光标                                          │  │
│  │   - 买卖信号标注（▲买入 ▼卖出）                           │  │
│  │   - 支持缩放、拖拽                                        │  │
│  │   - 悬浮显示详细信息                                      │  │
│  │     时间: 14:30  价格: 74.85  涨跌: +0.52%               │  │
│  │     相对均线: -0.23%  成交量: 12,500                      │  │
│  └───────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│ 指标选择: ☑综合T0策略  ☑价格偏离(基础)  ☑价格偏离(优化)        │
├─────────────────────────────────────────────────────────────────┤
│                  指标子图1: 综合T0策略 (13%)                     │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │   复合评分曲线 + 买卖信号                                 │  │
│  └───────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                  指标子图2: 价格偏离(基础) (13%)                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │   偏离率曲线 + 阈值线                                     │  │
│  └───────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│                  指标子图3: 价格偏离(优化) (13%)                 │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │   优化偏离率 + 信号                                       │  │
│  └───────────────────────────────────────────────────────────┘  │
├─────────────────────────────────────────────────────────────────┤
│ 播放控制:                                                        │
│  [◀后退] [▶播放] [❚❚暂停] [前进▶] 速度: [====|----] 1.0x      │
│  进度: ████████████░░░░░░░░ 65% (158/242分钟)                   │
└─────────────────────────────────────────────────────────────────┘
```

#### 交互增强功能

1. **鼠标交互**：
   - ✅ 十字光标（显示精确时间和价格）
   - ✅ 悬浮提示框（多指标数据）
   - ✅ 点击信号点查看详情
   - ✅ 拖拽缩放时间轴
   - ✅ 双击重置视图

2. **信号标注**：
   - ✅ 买入信号：绿色向上箭头 ▲
   - ✅ 卖出信号：红色向下箭头 ▼
   - ✅ 信号强度：大小表示评分高低
   - ✅ 连线显示配对交易

3. **实时播放优化**：
   - ✅ 平滑动画过渡
   - ✅ 可调速度（0.1x - 5x）
   - ✅ 进度条显示
   - ✅ 支持暂停/继续/跳转

4. **数据面板**：
   - ✅ 显示当前时刻所有指标值
   - ✅ 信号统计（买入次数、卖出次数、胜率）
   - ✅ 盈亏分析

---

### 📡 四、实时监控实现

#### 实时数据流架构

```python
# 伪代码示例
class RealtimeMonitor:
    def __init__(self, stocks, interval=60):
        self.stocks = stocks  # ['000333', '600030', '002415']
        self.interval = interval  # 更新间隔（秒）
        self.running = False
        
    def start(self):
        """启动实时监控"""
        self.running = True
        threading.Thread(target=self._monitor_loop, daemon=True).start()
        
    def _monitor_loop(self):
        """监控主循环"""
        while self.running:
            # 检查是否在交易时段（9:30-15:00）
            if self._is_trading_hours():
                for stock in self.stocks:
                    # 获取最新数据
                    latest_data = self.fetch_latest(stock)
                    
                    # 更新数据库
                    self.data_manager.save_minute_data(latest_data)
                    
                    # 计算指标
                    signals = self.calculate_indicators(latest_data)
                    
                    # 检测信号
                    if signals:
                        self.emit_signal(stock, signals)
                        
            time.sleep(self.interval)
            
    def emit_signal(self, stock, signals):
        """发出信号通知"""
        # 1. 保存到数据库
        self.data_manager.save_signals(signals)
        
        # 2. 桌面通知
        self.show_notification(stock, signals)
        
        # 3. 更新UI
        self.event_bus.emit('signal_detected', stock, signals)
```

#### 通知方式

1. **桌面通知**：
   - Windows: 使用`win10toast`库
   - 通知内容：股票名称、信号类型、价格、评分

2. **UI内通知**：
   - 状态栏闪烁
   - 弹出提示框
   - 声音提示（可选）

3. **日志记录**：
   - 所有信号写入日志文件
   - 便于回测分析

---

### ⚙️ 五、配置管理优化

#### 配置文件设计（config/settings.py）

```python
# 股票配置
STOCKS = {
    '000333': '美的集团',
    '600030': '中信证券',
    '002415': '海康威视'
}

# 交易时段
TRADING_HOURS = {
    'morning': ('09:30', '11:30'),
    'afternoon': ('13:00', '15:00')
}

# 数据源配置
DATA_SOURCE = {
    'primary': 'akshare',      # 主数据源
    'fallback': 'dfcf',        # 备用数据源
    'cache_enabled': True,
    'cache_db': 'db/t0_trading.db'
}

# 指标配置
INDICATORS = {
    'comprehensive_t0_strategy': {
        'enabled': True,
        'display_name': '综合T0策略',
        'color': 'blue'
    },
    'price_ma_deviation': {
        'enabled': True,
        'display_name': '价格偏离(基础)',
        'color': 'purple'
    },
    'price_ma_deviation_optimized': {
        'enabled': True,
        'display_name': '价格偏离(优化)',
        'color': 'orange'
    }
}

# UI配置
UI_CONFIG = {
    'theme': 'light',  # light/dark
    'chart_height_ratio': [3, 1, 1, 1],  # 主图:子图比例
    'font_family': 'Microsoft YaHei',
    'line_width': 1.5
}

# 实时监控配置
MONITOR_CONFIG = {
    'enabled': False,
    'interval': 60,  # 秒
    'notification': True
}
```

---

## 实施计划

### 第一阶段：核心重构（3-5天）
1. ✅ 创建数据库模块（data_manager.py）
2. ✅ 迁移CSV数据到SQLite
3. ✅ 实现数据源抽象层
4. ✅ 完善AkShare数据源
5. ✅ 修复东方财富数据源

### 第二阶段：UI重构（3-4天）
1. ✅ 拆分可视化组件
2. ✅ 实现主窗口框架
3. ✅ 优化图表渲染性能
4. ✅ 添加交互功能（十字光标、悬浮提示）
5. ✅ 实现播放控制优化

### 第三阶段：监控功能（2-3天）
1. ✅ 实现实时数据获取
2. ✅ 集成指标计算
3. ✅ 信号检测和通知
4. ✅ 日志系统

### 第四阶段：测试和文档（2天）
1. ✅ 单元测试
2. ✅ 集成测试
3. ✅ 用户文档
4. ✅ 部署指南

---

## 技术栈

### 现有依赖
- pandas==2.0.3
- numpy==1.24.3
- matplotlib==3.7.2
- akshare==1.10.2
- requests==2.31.0

### 新增依赖
```
# 数据库
sqlite3  # Python内置

# 桌面通知（可选）
win10toast==0.9  # Windows通知

# 配置管理
pyyaml==6.0  # 支持YAML配置文件

# 日志
loguru==0.7.0  # 更强大的日志库
```

---

## 预期收益

### 性能提升
- 数据查询速度：CSV → SQLite，提升 **10-50倍**
- UI响应速度：组件化后，减少重绘，提升 **30%**
- 内存占用：优化数据加载，降低 **40%**

### 可维护性提升
- 代码行数：t0_data_visualizer.py从1463行 → 300行（主窗口）
- 模块解耦：便于单独测试和迭代
- 插件化指标：新增指标无需修改核心代码

### 功能增强
- ✅ 实时监控
- ✅ 信号通知
- ✅ 历史回放
- ✅ 专业交互体验

---

## 风险和注意事项

1. **数据迁移风险**：
   - 迁移前备份CSV文件
   - 验证数据完整性

2. **兼容性**：
   - 保留旧接口兼容性
   - 渐进式重构

3. **性能测试**：
   - 大数据量下的SQLite性能
   - UI渲染优化

4. **实时监控**：
   - 数据源稳定性
   - 频率限制

---

## 总结

这份优化方案涵盖了：
1. **数据存储**：CSV → SQLite，提升查询效率
2. **架构设计**：分层架构，提高可维护性
3. **UI优化**：组件化，增强交互体验
4. **实时监控**：自动化信号检测和通知

建议**优先实施第一和第二阶段**，打好基础后再添加实时监控功能。整个优化预计需要**10-14天**完成。
