import requests
from fake_useragent import UserAgent

ua = UserAgent()
url = "https://dq.10jqka.com.cn/fuyao/stock_diagnosis/finance/v1/ability_history?code=300010&market=333&type=stock&ability_id=final_score&industry_type="
headers = {
        "User-Agent": ua.random
    }

response = requests.get(url, headers=headers)
print(response.text)