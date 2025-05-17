# cancel.py
from urllib.parse import urlparse

from locust import HttpUser, task, between
from common import TaxAPIBase
import json
import logging
from faker import Faker
import datetime


logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")


class CancelAPILocust(HttpUser):
    host = "http://balitax-test.com/declaration-api"
    wait_time = between(0.1, 0.5)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tax_api_base = TaxAPIBase(company_name="tax_agent001@linshiyou.com")
        self.faker = Faker()
        self.generated_order_nos = set()

    @task
    def cancel_order(self):
        order_no = self._generate_unique_orderno(datetime.datetime.now().strftime("%Y%m%d"))


        payload = {
            "agentOrderNo": f"AgentOrderNo{order_no}",
            "requestId": str(self.faker.random_int(min=1, max=9999))
        }

        endpoint_path = "/v1.0/declaration/cancel"

        headers = {
            "Content-Type": "application/json; charset=utf-8",
            "X-AGENT-ID": self.tax_api_base.agent_id,
            "X-TIMESTAMP": self.tax_api_base._generate_iso_timestamp(),
            "X-SIGNATURE": self.tax_api_base._generate_signature(endpoint_path, payload),
            "Host": urlparse(self.host).netloc
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
            order_no = self.faker.random_int(min=1, max=100)
            full_orderno = f"AgentOrderNo{today}{order_no}"
            if full_orderno not in self.generated_order_nos:
                self.generated_order_nos.add(full_orderno)
                return order_no
