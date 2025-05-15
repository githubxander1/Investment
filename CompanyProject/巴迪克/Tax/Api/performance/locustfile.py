# locustfile.py
from locust import HttpUser, task, between
from utils.helper import send_create_order
import asyncio
import json
from contextlib import contextmanager

@contextmanager
def async_client(locust_instance):
    client = locust_instance.client
    yield client


class TaxAPILocust(HttpUser):
    wait_time = between(0.1, 0.5)

    @task
    def create_order(self):
        from utils.helper import send_create_order
        payload = {
            "merchantId": "600009M0000001",
            "paymentType": "StaticMandiriVA",
            "amount": "0.01",
            "agentOrderNo": "AgentOrderNo20250515",
            "payOrderNo": "PayOrder20250515",
            "sourceAgentOrderNo": "",
            "productName": "Test Product",
            "requestId": "1"
        }

        loop = asyncio.get_event_loop()
        result = loop.run_until_complete(send_create_order(self.client, payload))
        if result["status"] == "success":
            self.environment.events.request_success.fire(
                request_type="POST",
                name="/v1.0/declaration/create",
                response_time=result["elapsed"],
                response_length=0
            )
        else:
            self.environment.events.request_failure.fire(
                request_type="POST",
                name="/v1.0/declaration/create",
                response_time=result["elapsed"],
                exception=Exception(result["response"])
            )
