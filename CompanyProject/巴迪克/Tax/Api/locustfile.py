# locustfile.py

from locust import HttpUser, task, between
from common import TaxAPIBase, CONFIG
import json
import logging
from urllib.parse import urlparse
from faker import Faker
import datetime

# 启用详细日志
logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

class TaxAPILocust(HttpUser):
    host = "http://balitax-test.com/declaration-api"  # Locust UI 显示地址
    wait_time = between(0.1, 0.5)     # 用户等待时间

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.tax_api_base = TaxAPIBase(company_name="tax_agent002@linshiyou.com")
        self.faker = Faker()
        self.generated_order_nos = set()  # 记录已使用的订单号，防止重复

    @task
    def create_order(self):
        today = datetime.datetime.now().strftime("%Y%m%d")
        order_no = self._generate_unique_orderno(today)

        payload = {
            "merchantId": "600009M0000001",
            "paymentType": "StaticMandiriVA",
            "amount": "0.01",
            "agentOrderNo": f"AgentOrderNo{today}{order_no}",
            "payOrderNo": f"PayOrder{today}{order_no}",
            "sourceAgentOrderNo": "",
            "productName": self.faker.name(),
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

    def _generate_unique_orderno(self, today: str):
        """生成唯一订单号"""
        while True:
            order_no = self.faker.random_int(min=1000, max=9999)
            full_orderno = f"AgentOrderNo{today}{order_no}"
            if full_orderno not in self.generated_order_nos:
                self.generated_order_nos.add(full_orderno)
                return order_no
if __name__ == "__main__":
    from locust.main import main

    # 使用 main() 函数启动 Locust
    main()
