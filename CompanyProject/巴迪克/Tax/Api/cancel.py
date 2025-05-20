from pprint import pprint
from typing import Dict

# from common import TaxAPIBase
from CompanyProject.巴迪克.Tax.Api.com.common import TaxAPIBase

class CancelOrderAPI(TaxAPIBase):
    """撤销订单API"""

    ENDPOINT_PATH = "/v1.0/declaration/cancel"

    def cancel_order(self, payload: Dict) -> Dict:
        """撤销订单"""
        result = self.send_request(self.ENDPOINT_PATH, payload)
        try:
            print(f"✅ 撤销订单成功：{result}")
            assert result["errCodeDes"] == "success"
        except AssertionError:
            print("❌ 撤销订单失败：请求{}，返回{}".format(payload, result))
        # pprint(f"✅ 订单撤销成功", {result})
        return result

if __name__ == "__main__":
    api_client = CancelOrderAPI(company_name="tax_agent009")

    cancel_request_payload = {
        "agentOrderNo": "AgentOrderNo20250520613",
        "requestId": "19999999999999999999"
    }

    result = api_client.cancel_order(cancel_request_payload)
    pprint(result)
