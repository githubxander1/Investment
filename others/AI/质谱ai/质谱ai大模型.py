import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain.llms import ChatOpenAI
import os

# 生成股票价格数据
np.random.seed(0)  # 设置随机种子以保证结果可重复
dates = pd.date_range(start='2023-01-01', periods=100, freq='D')
close_prices = np.cumsum(np.random.normal(0, 1, 100)) + 100
high_prices = close_prices + np.random.uniform(0, 5, 100)
low_prices = close_prices - np.random.uniform(0, 5, 100)
volumes = np.random.randint(1000000, 5000000, 100)

df = pd.DataFrame({
    '日期': dates,
    '收盘': close_prices,
    '最高': high_prices,
    '最低': low_prices,
    '成交量': volumes
})

# 生成股票信息
stock_info = pd.DataFrame({
    'item': ['公司名称', '行业', '市值'],
    'value': ['Example Corp', 'Technology', '100B']
})

# 生成新闻数据
news_titles = [
    "Example Corp reports Q4 earnings",
    "New partnership announced for Example Corp",
    "Market analysts predict growth for Example Corp",
    "Example Corp launches new product",
    "Economic outlook favorable for technology sector"
]

news_df = pd.DataFrame({
    '新闻标题': news_titles
})

def analyze_stock_trend(stock_code, df, stock_info, news_df):
    """使用LangChain和OpenAI模型分析股票走势并给出投资建议"""
    # 计算一些基本指标
    latest_price = df['收盘'].iloc[-1]
    price_change = df['收盘'].iloc[-1] - df['收盘'].iloc[0]
    price_change_percent = (price_change / df['收盘'].iloc[0]) * 100

    # 准备股票信息
    info_str = "\n".join([f"{row['item']}: {row['value']}" for _, row in stock_info.iterrows()])

    # 准备新闻信息
    news_str = "\n".join([f"- {row['新闻标题']}" for _, row in news_df.iterrows()])

    # 创建提示模板
    template = """
    分析以下股票数据并给出走势分析和投资建议：

    股票代码：{stock_code}
    最新收盘价：{latest_price}
    年度价格变化：{price_change} ({price_change_percent}%)
    最高价：{high_price}
    最低价：{low_price}
    平均成交量：{avg_volume}

    股票信息：
    {stock_info}

    相关新闻：
    {news}

    请提供以下信息：
    1. 总体趋势分析
    2. 可能的支撑位和阻力位
    3. 成交量分析
    4. 短期和长期预测
    5. 潜在风险和机会
    6. 基于技术分析和新闻的投资建议
    """

    prompt = PromptTemplate(
        input_variables=["stock_code", "latest_price", "price_change", "price_change_percent",
                         "high_price", "low_price", "avg_volume", "stock_info", "news"],
        template=template
    )

    # 创建LLM链
    llm = ChatOpenAI(
        temperature=0.95,
        model="glm-4-flash",
        openai_api_key=os.getenv("OPENAI_API_KEY"),
        openai_api_base="https://open.bigmodel.cn/api/paas/v4/"
    )
    chain = LLMChain(llm=llm, prompt=prompt)

    # 运行链
    result = chain.run({
        "stock_code": stock_code,
        "latest_price": f"{latest_price:.2f}",
        "price_change": f"{price_change:.2f}",
        "price_change_percent": f"{price_change_percent:.2f}",
        "high_price": f"{df['最高'].max():.2f}",
        "low_price": f"{df['最低'].min():.2f}",
        "avg_volume": f"{df['成交量'].mean():.2f}",
        "stock_info": info_str,
        "news": news_str
    })

    return result

# 设置环境变量 OPENAI_API_KEY
os.environ["OPENAI_API_KEY"] = "c496018f53e9fb12a7d75e47ba765439.hJcqoB2MjCLPLx8t"

# 调用 analyze_stock_trend 函数
stock_code = "EXMP"
result = analyze_stock_trend(stock_code, df, stock_info, news_df)

print(result)
