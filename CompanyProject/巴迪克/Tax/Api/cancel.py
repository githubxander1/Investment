from pprint import pprint
from typing import Dict

from common import TaxAPIBase

class CancelOrderAPI(TaxAPIBase):
    """撤销订单API"""

    ENDPOINT_PATH = "/v1.0/declaration/cancel"

    def cancel_order(self, payload: Dict) -> Dict:
        """撤销订单"""
        return self.send_request(self.ENDPOINT_PATH, payload)

if __name__ == "__main__":
    api_client = CancelOrderAPI(company_name="tax_agent001@linshiyou.com")

    cancel_request_payload = {
        "agentOrderNo": "AgentOrderNo2025051411",
        "requestId": "19999999999999999999"
    }

    result = api_client.cancel_order(cancel_request_payload)
    pprint(result)
