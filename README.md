# 股票数据爬虫项目

本项目包含两个不同的方式来获取股票数据：
1. 使用Playwright模拟浏览器操作的方式
2. 直接调用API接口的方式

## 文件说明

- `stock_crawler_playwright.py` - 使用Playwright的爬虫程序
- `stock_api_client.py` - 直接调用API接口的客户端程序
- `requirements.txt` - 项目依赖列表

## 安装依赖

```bash
pip install -r requirements.txt
```

如果使用Playwright，还需要安装浏览器：

```bash
playwright install chromium
```

## 使用方法

### 方法1：使用API客户端（推荐但需要认证）

```bash
python stock_api_client.py
```

该程序将获取美的集团的日线数据和分时图数据，并保存为JSON文件。

**注意：** 百度股票API需要有效的认证令牌(Acs-Token)才能访问数据。在实际使用中，您需要通过合法途径获取有效的认证信息。

### 方法2：使用Playwright爬虫

```bash
python stock_crawler_playwright.py
```

该程序将启动浏览器，访问目标网站，并尝试获取数据。

## 自定义股票代码

要获取其他股票的数据，可以修改相应代码中的股票代码和名称参数。

## 注意事项

1. 直接调用API的方式更稳定、更快速，但需要处理认证问题。
2. Playwright方式可能因为网站结构变化而需要调整选择器。
3. 请遵守网站的robots.txt和使用条款，不要过于频繁地请求数据。
4. 本示例仅用于学习目的，请勿用于商业用途。