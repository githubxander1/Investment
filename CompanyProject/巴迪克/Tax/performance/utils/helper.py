# utils/helper.py

import datetime
import aiohttp
import asyncio
import time
from ..config.settings import Config
from ..utils.logger import logger
from faker import Faker

fake = Faker()

async def send_create_order(session, payload):
    url = Config.API_BASE_URL + Config.CREATE_ENDPOINT
    start = time.time()

    try:
        async with session.post(url, json=payload) as response:
            elapsed = (time.time() - start) * 1000  # 毫秒
            text = await response.text()

            try:
                data = await response.json()
            except Exception as e:
                data = {"error": f"JSON 解析失败: {str(e)}"}

            if response.status == 200 and data.get("errCode") == "0":
                logger.info(f"✅ 成功：{payload['agentOrderNo']} - 耗时 {elapsed:.2f} ms")
                return {
                    "status": "success",
                    "elapsed": elapsed,
                    "payload": payload,
                    "response_data": data
                }
            else:
                logger.error(f"❌ 失败：{payload['agentOrderNo']} - 状态码: {response.status}, 返回: {text[:499]}")
                return {
                    "status": "failure",
                    "elapsed": elapsed,
                    "payload": payload,
                    "response": text,
                    "response_data": data
                }

    except Exception as e:
        elapsed = (time.time() - start) * 1000
        logger.error(f"🚨 异常捕获：{payload['agentOrderNo']} - 错误: {str(e)}")
        return {
            "status": "exception",
            "elapsed": elapsed,
            "payload": payload,
            "response": str(e),
            "response_data": {}
        }


async def run_async_requests(total=50):
    tasks = []
    today = datetime.datetime.now().strftime("%Y%m%d")

    async with aiohttp.ClientSession() as session:
        for i in range(total):
            payload = {
                "merchantId": "600009M0000001",
                "paymentType": "StaticMandiriVA",
                "amount": "0.01",
                "agentOrderNo": f"AgentOrderNo{today}{i}",
                "payOrderNo": f"PayOrder{today}{i}",
                "sourceAgentOrderNo": "",
                "productName": fake.name(),
                "requestId": "1"
            }
            tasks.append(send_create_order(session, payload))

        results = await asyncio.gather(*tasks)
        return results
