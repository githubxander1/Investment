# 代理爬虫系统

这个目录包含三个主要的Python脚本，用于从不同来源获取和管理代理服务器：

## 文件说明

### 1. free_proxy.py
从 [free-proxy-list.net](https://free-proxy-list.net) 获取免费代理服务器。

功能：
- 使用 Playwright 爬取网页数据
- 多线程验证代理有效性
- 过滤无效/内网IP
- 保存有效代理到CSV文件

### 2. proxynova.py
从 [ProxyNova](https://www.proxynova.com/proxy-server-list/) 获取免费代理服务器。

功能：
- 使用 Playwright 爬取网页数据
- 解析JavaScript混淆的IP地址
- 多线程验证代理有效性
- 过滤无效/内网IP
- 保存有效代理到CSV文件

### 3. proxy_manager.py
统一管理两个代理源，提供自动切换功能。

功能：
- 自动从两个源获取代理
- 主源失败时自动切换到备用源
- 合并和保存所有有效代理
- 提供简单的API供其他模块调用

### 4. proxy_utils.py
代理工具函数库。

功能：
- 解析JavaScript混淆的IP地址
- 验证IP地址格式
- 使用curl风格验证代理

## 使用方法

### 直接运行脚本
```bash
# 运行 free_proxy.py
python free_proxy.py

# 运行 proxynova.py
python proxynova.py

# 运行代理管理器
python proxy_manager.py
```

### 在其他Python脚本中使用
```python
from proxy_manager import ProxyManager

# 创建代理管理器实例
manager = ProxyManager("./proxy_data")

# 获取代理（自动切换源）
proxies = manager.get_proxies(max_workers=10, verify_timeout=5.0, fallback=True)

# 获取最新代理数据
latest_proxies = manager.get_latest_proxies()
```

## 技术特点

### JavaScript混淆IP解析
ProxyNova网站使用JavaScript动态生成IP地址以防止爬虫，我们使用`py_mini_racer`库在Python中执行JavaScript代码来解析真实的IP地址。

### CURL风格代理验证
使用与以下curl命令相同的方式验证代理：
```bash
curl --proxy "ip:port" -i http://azenv.net/
```

这确保了我们验证的代理与实际使用场景一致。

## 配置说明

所有脚本都支持自定义配置，可以通过修改脚本末尾的参数来调整：

- `TARGET_URL`: 目标网站URL
- `SAVE_DIR`: 保存目录
- `LOG_DIR`: 日志目录
- `VERIFY_PROXIES`: 是否验证代理有效性
- `MAX_WORKERS`: 验证代理的最大并发线程数
- `VERIFY_TIMEOUT`: 验证超时时间（秒）
- `DAILY_CRAWL_TIME`: 定时任务执行时间

## 输出文件

脚本会生成以下类型的文件：

1. `free_proxies_valid_YYYYMMDD.csv` - 来自free-proxy-list.net的有效代理
2. `proxynova_proxies_valid_YYYYMMDD.csv` - 来自ProxyNova的有效代理
3. `merged_proxies_valid_YYYYMMDD.csv` - 合并后的有效代理
4. 日志文件 - 记录执行过程和错误信息

## 依赖库

- playwright
- pandas
- requests
- schedule
- py-mini-racer

安装依赖：
```bash
pip install playwright pandas requests schedule py-mini-racer
playwright install chromium
```