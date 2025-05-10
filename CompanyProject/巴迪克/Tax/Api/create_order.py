# create_order.py
import os
import hmac
import json
import hashlib
import datetime

import requests
from urllib.parse import urlparse
from typing import Dict, Tuple, Optional
from pprint import pprint

from faker import Faker

from CompanyProject.巴迪克.utils.sql_handler import SQLHandler

# 配置常量
CONFIG = {
    "BASE_URL": "http://balitax-test.com/declaration-api",
    "ENDPOINT_PATH": "/v1.0/declaration/create",
    "YAML_PATH": os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../common/sql_config.yaml"
    ))
}

class TaxAPI:
    """税务申报API客户端"""

    def __init__(self, company_name: str, environment: str = 'test' ):
        """
        初始化税务API客户端
        :param environment: 环境标识（test/prod）
        :param company_name: 代理公司名称
        """
        self.environment = environment
        self.company_name = company_name
        self.agent_id, self.secret_key = self._load_agent_credentials()

    def _load_agent_credentials(self) -> Tuple[str, str]:
        """从数据库加载代理凭证"""
        try:
            with SQLHandler(CONFIG['YAML_PATH'], self.environment, 'tax') as handler:
                sql = f"SELECT agent_no, sign_key FROM {handler.get_table('agent_base_info')} WHERE company_name = %s"
                result = handler.query_one(sql, (self.company_name,))
                print(f'agent_no: {result[0]}, company_name:  {self.company_name}, secret_key: {result[1]}')

            if not result:
                raise ValueError(f"未找到公司 {self.company_name} 的信息")
            return result[0], result[1]
        except Exception as e:
            print(f"[ERROR] 凭证加载失败: {str(e)}")
            raise

    @staticmethod
    def _generate_iso_timestamp() -> str:
        """生成ISO 8601格式时间戳（带毫秒和时区）"""
        now = datetime.datetime.now(datetime.timezone.utc).astimezone()
        tz_offset = now.utcoffset()
        hours, minutes = divmod(int(tz_offset.total_seconds()) // 60, 60)
        return now.strftime(f"%Y-%m-%dT%H:%M:%S.{now.microsecond//1000:03d}") + \
            f"{'+' if hours >=0 else '-'}{abs(hours):02d}:{minutes:02d}"

    def _generate_signature(self, payload: Dict) -> str:
        """生成HMAC-SHA256签名"""
        # 压缩JSON payload
        payload_str = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)

        # 生成签名
        timestamp = self._generate_iso_timestamp()
        payload_hash = hashlib.sha256(payload_str.encode()).hexdigest()
        canonical_str = f"POST:{CONFIG['ENDPOINT_PATH']}:{payload_hash}:{timestamp}"

        return hmac.new(
            self.secret_key.encode(),
            canonical_str.encode(),
            hashlib.sha256
        ).hexdigest()

    def send_declaration(self, payload: Dict) -> Dict:
        """发送申报请求"""
        try:
            # 准备请求参数
            headers = {
                "Content-Type": "application/json; charset=utf-8",
                "X-AGENT-ID": self.agent_id,
                "X-TIMESTAMP": self._generate_iso_timestamp(),
                "X-SIGNATURE": self._generate_signature(payload),
                "Host": urlparse(CONFIG['BASE_URL']).netloc
            }

            # 发送请求
            response = requests.post(
                url=f"{CONFIG['BASE_URL']}{CONFIG['ENDPOINT_PATH']}",
                data=json.dumps(payload, separators=(',', ':')),
                headers=headers
            )
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] 请求失败: {str(e)}")
            return {"error": str(e)}
        except Exception as e:
            print(f"[ERROR] 系统错误: {str(e)}")
            return {"error": "Internal error"}

if __name__ == "__main__":
    # amount_test_data = {
    #     'max_xiaoshu':'123456789012.99',
    #     'max_fu':'-123456789012.99',
    #     'threexiaoshu':'123456789012.123',
    #     'float_zero':'123456789012.00',
    #     'init_14':'1234567890123.12',
    # }
    faker  = Faker()
    api_client = TaxAPI(company_name="tax_agent001@linshiyou.com")
    #每一种类型都请求
    paymentType =["CASH", "CreditCard", "DebitCard", "DANABALANCE", "SHOPEEBALANCE", "LINKAJABALANCE", "OVOBALANCE", "GOPAYBALANCE", "SinarmasVA", "MaybankVA", "DanamonVA", "BNCVA", "BCAVA", "INAVA", "BNIVA", "PermataVA", "MuamalatVA", "BSIVA", "BRIVA", "MandiriVA", "CIMBVA", "StaticMandiriVA", "StaticBCAVA", "QRIS", "Indodana", "Atome", "Kredivo", "Indomaret", "Alfarmart", "POS"]
    today = datetime.datetime.now().strftime("%Y%m%d")

    #批量生成
    n = 1
    amount = "0.01"
    # for paymentType in paymentType:
        # for n in range(1, requests_pre_type +1):
    order_suffix = f"{n:03d}"
    agentOrderNo = f"AgentOrderNo{today}-{paymentType}-{n}"
    payOrderNo = f"PayOrder{today}-{paymentType}-{n}"
    productName = faker.company()
    # productName = '的地方凤凰好好谷歌广告和狗狗狗狗狗个哈哈哈哈嗝哈哈哈哈嗝嗝哈哈哈更回复二哥给狗狗狗法国嗝哈哈哈哈哈哈哈哈哈哈哈狗狗狗狗狗狗个我是通过好好谷歌官方的地方凤凰好好谷歌广告和狗狗狗狗狗个哈哈哈哈嗝哈哈哈一百'

    creat_request_payload = {
        "merchantId": "600008M0000002",
        # "paymentType": paymentType,
        "paymentType": "StaticMandiriVA",
        # "paymentType": "INVALIDTYPE",
        "amount": amount,
        "agentOrderNo": agentOrderNo,
        "payOrderNo": payOrderNo,
        "sourceAgentOrderNo": "AGENT2025",
        "productName": productName,
        "requestId": "1"
    }

    result = api_client.send_declaration(creat_request_payload)
    pprint(result)
        # print(f"{n},正在处理{paymentType}，{agentOrderNo}, {payOrderNo}, {productName}")
    print(f"\n{n},已完成：amount: {amount}, agentOrderNo：{agentOrderNo}, payOrderNo：{payOrderNo}, productName：{productName}")
        # n += 1
