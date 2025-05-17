# locustfile.py
import datetime
import logging
import time
from urllib.parse import urlparse

from faker import Faker
from locust import HttpUser, task, between

from CompanyProject.巴迪克.Tax.Api.common import TaxAPIBase, CONFIG
# from utils.helper import send_create_order
# import asyncio
import json
from contextlib import contextmanager


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")
@contextmanager
def async_client(locust_instance):
    client = locust_instance.client
    yield client


class TaxAPILocust(HttpUser):
    host = "http://balitax-test.com/declaration-api"
    wait_time = between(0.1, 0.5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tax_api_base = TaxAPIBase(company_name="tax_agent002@linshiyou.com")
        self.faker = Faker()
        self.generated_order_nos = set()  # 记录已使用的订单号，防止重复

    @task(5)
    def create_order(self):
        today = datetime.datetime.now().strftime("%Y%m%d")
        order_no = self._generate_unique_orderno(today)

        payload = {
            "merchantId": "600009M0000001",
            "paymentType": "StaticMandiriVA",
            "amount": round(self.faker.random.uniform(0.01, 999999999999.99), 2),
            "agentOrderNo": f"AgentOrderNo{today}{order_no}",
            "payOrderNo": f"PayOrder{today}{order_no}",
            "sourceAgentOrderNo": "",
            "productName": self.faker.catch_phrase(),
            "requestId": str(self.faker.random_int(min=1, max=20))
        }

        endpoint_path = "/v1.0/declaration/create"

        # 构建请求头（与 common.py 保持一致）
        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "X-AGENT-ID": self.tax_api_base.agent_id,
            "X-TIMESTAMP": self.tax_api_base._generate_iso_timestamp(),
            "X-SIGNATURE": self.tax_api_base._generate_signature(endpoint_path, payload),
            "Host": urlparse(CONFIG["BASE_URL"]).netloc
        }

        # 发送请求并验证结果
        with self.client.post(
                endpoint_path,
                data=json.dumps(payload, separators=(',', ':')),
                headers=headers,
                catch_response=True
        ) as response:
            try:
                data = response.json()
                logging.debug(f"Response Data: {json.dumps(data, indent=2)}")

                if 'error' in data:
                    response.failure(f"API 返回错误: {data['error']}")
                else:
                    response.success()

            except Exception as e:
                response.failure(f"解析失败: {str(e)}")
                logging.error(f"请求失败: {payload}, 响应: {response.text}")

    @task(1)
    def cancel_order(self):
        agentOrderNo = "AgentOrderNo20250515"
        payload = {
            "agentOrderNo": agentOrderNo,
            "requestId": str(int(time.time() * 1000))
        }

        endpoint_path = "/v1.0/declaration/cancel"
        signature = self.tax_api_base._generate_signature(endpoint_path, payload)

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "X-AGENT-ID": self.tax_api_base.agent_id,
            "X-TIMESTAMP": self.tax_api_base._generate_iso_timestamp(),
            "X-SIGNATURE": signature,
            "Host": urlparse(CONFIG["BASE_URL"]).netloc
        }

        with self.client.post(
                endpoint_path,
                data=json.dumps(payload, separators=(',', ':')),
                headers=headers,
                catch_response=True
        ) as response:
            try:
                data = response.json()
                if 'error' in data:
                    response.failure(f"API 返回错误: {data['error']}")
                else:
                    response.success()

            except Exception as e:
                response.failure(f"解析失败: {str(e)}")
                logging.error(f"请求失败: {payload}, 响应: {response.text}")
    def _generate_unique_orderno(self, today: str):
        """生成唯一订单号"""
        while True:
            order_no = self.faker.random_int(min=10, max=100)
            full_orderno = f"AgentOrderNo{today}{order_no}"
            if full_orderno not in self.generated_order_nos:
                self.generated_order_nos.add(full_orderno)
                return order_no


# if __name__ == "__main__":
#     from locust.main import main
#
#     main()


    # @task
    # def create_order(self):
    #     from utils.helper import send_create_order
    #     payload = {
    #         "merchantId": "600009M0000001",
    #         "paymentType": "StaticMandiriVA",
    #         "amount": "0.01",
    #         "agentOrderNo": "AgentOrderNo20250515",
    #         "payOrderNo": "PayOrder20250515",
    #         "sourceAgentOrderNo": "",
    #         "productName": "Test Product",
    #         "requestId": "1"
    #     }
    #
    #     loop = asyncio.get_event_loop()
    #     result = loop.run_until_complete(send_create_order(self.client, payload))
    #     if result["status"] == "success":
    #         self.environment.events.request_success.fire(
    #             request_type="POST",
    #             name="/v1.0/declaration/create",
    #             response_time=result["elapsed"],
    #             response_length=0
    #         )
    #     else:
    #         self.environment.events.request_failure.fire(
    #             request_type="POST",
    #             name="/v1.0/declaration/create",
    #             response_time=result["elapsed"],
    #             exception=Exception(result["response"])
    #         )
