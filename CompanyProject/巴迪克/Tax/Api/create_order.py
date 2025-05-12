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

import logging

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s - %(levelname)s - %(message)s",
                    handlers=[
                        logging.StreamHandler(),
                        logging.FileHandler("./log/tax_api_log.log"),
                    ])


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
        """从数据库获取secret_key"""
        try:
            with SQLHandler(CONFIG['YAML_PATH'], self.environment, 'tax') as handler:
                sql = f"SELECT agent_no, sign_key FROM {handler.get_table('agent_base_info')} WHERE company_name = %s"
                result = handler.query_one(sql, (self.company_name,))
                logging.info(f'agent_no: {result[0]}, company_name: {self.company_name}, secret_key: {result[1]}')

            if not result:
                raise ValueError(f"未找到公司 {self.company_name} 的信息")
            return result[0], result[1]

        except Exception as e:
            print(f"secret_key获取失败: {str(e)}")
            raise

    @staticmethod
    def _generate_iso_timestamp() -> str:
        """生成ISO 8601格式时间戳（带毫秒和时区）"""
        now = datetime.datetime.now(datetime.timezone.utc).astimezone()
        # logging.info(f"当前时间: {now}")

        tz_offset = now.utcoffset()
        hours, minutes = divmod(int(tz_offset.total_seconds()) // 60, 60)
        # logging.info(f"时区偏移: {hours}:{minutes}")

        iso_timestamp = now.strftime(f"%Y-%m-%dT%H:%M:%S.{now.microsecond//1000:03d}") + \
            f"{'+' if hours >=0 else '-'}{abs(hours):02d}:{minutes:02d}"
        # logging.info(f"生成ISO 8601格式时间戳: {iso_timestamp}")

        return iso_timestamp

    def _generate_signature(self, payload: Dict) -> str:
        """生成HMAC-SHA256签名"""
        # 压缩JSON payload
        payload_str = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)
        logging.info(f"压缩后的JSON payload: {payload_str}")

        # 生成签名
        timestamp = self._generate_iso_timestamp()
        payload_hash = hashlib.sha256(payload_str.encode()).hexdigest()
        logging.info(f"加密后的JSON payload: {payload_hash}")

        canonical_str = f"POST:{CONFIG['ENDPOINT_PATH']}:{payload_hash}:{timestamp}"
        logging.info(f"原始请求字符串: {canonical_str}")

        SHA256_signature = hmac.new(
            self.secret_key.encode(),
            canonical_str.encode(),
            hashlib.sha256
        ).hexdigest()
        logging.info(f"生成的签名: {SHA256_signature}")
        return SHA256_signature

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
            logging.info(f"请求头: {headers}")

            # 发送请求
            response = requests.post(
                url=f"{CONFIG['BASE_URL']}{CONFIG['ENDPOINT_PATH']}",
                data=json.dumps(payload, separators=(',', ':')),
                headers=headers
            )
            response.raise_for_status()
            response_json = response.json()
            logging.info(f"响应: {response_json}")

            return response_json
        except requests.exceptions.RequestException as e:
            logging.error(f"请求失败: {str(e)}")
            return {"error": str(e)}
        except Exception as e:
            logging.error(f"系统错误: {str(e)}")
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

    MCC_dict= {7311: 'Advertising', 4511: 'Airlines', 5533: 'Automotive', 7298: 'Beauty Services',
           4899: 'Cable & Streaming Service', 8398: 'Charity / Donation', 5815: 'Digital Goods: Books, Movies, Music',
           5816: 'Digital Goods: Games', 5817: 'Digital Goods: Applications (Excludes Games)', 8299: 'Education',
           5732: 'Electronics', 5999: 'Fashion', 6012: 'FinancialService', 5499: 'Food & Beverage',
           9399: 'GovernmentServices', 5411: 'Groceries', 7011: 'Hospitality', 6399: 'Insurance', 6533: 'Payment',
           5262: 'Marketplace & Retail Online', 8099: 'Medical Platform', 1520: 'Property', 6211: 'SecuritiesBrokers',
           4214: 'Shipping & Delivery Service', 4789: 'Transportation', 4722: 'Travel Agencies / Online Ticketing',
           7299: 'Others', 6532: 'Payment Transaction—Customer Financial Institution',
           7392: 'Consulting, Management and Public Relations Services', 5945: 'Game, Toy and Hobby Shops',
           5600: 'Clothing Stores', 5072: 'Hardware Equipment and Supplies',
           6050: 'Quasi Cash–Member Financial Institution', 5045: 'Computers, Computer Peripheral Equipment, Software',
           8999: 'Professional Services', 8071: 'Dental and Medical Laboratories', 7531: 'Automotive Body Repair Shops',
           7542: 'Car Washes', 5311: 'Department Stores',
           4225: 'Public Warehousing–Farm Products, Refrigerated Goods, Household Goods Storage',
           8111: 'Attorneys, Legal Services', 4816: 'Computer Network/Information Services',
           7999: 'Recreation Services', 7210: 'Cleaning, Garment and Laundry Services',
           4900: 'Utilities–Electric, Gas, Heating Oil, Sanitary, Water', 8661: 'Organizations, Religious',
           8062: 'Hospitals', 3500: 'Car Rental Agencies',
           5983: 'Fuel Dealers–Coal, Fuel Oil, Liquefied Petroleum, Wood', 7523: 'Automobile Parking Lots and Garages',
           5995: 'Pet Shops, Pet Food and Supplies', 5944: 'Clock, Jewelry, Watch and Silverware Stores',
           5946: 'Camera and Photographic Supply Stores', 7230: 'Barber and Beauty Shops',
           7929: 'Events and entertainment', 5818: 'Digital Goods: Multi-Category (M)'}

    MCC_list = [7311, 4511, 5533, 7298, 4899, 8398, 5815, 5816, 5817, 8299, 5732, 5999, 6012, 5499, 9399, 5411, 7011,
               6399, 6533, 5262, 8099, 1520, 6211, 4214, 4789, 4722, 7299, 6532, 7392, 5945, 5600, 5072, 6050, 5045,
               8999, 8071, 7531, 7542, 5311, 4225, 8111, 4816, 7999, 7210, 4900, 8661, 8062, 3500, 5983, 7523, 5995,
               5944, 5946, 7230, 7929, 5818]
    paymentType =["CASH", "CreditCard", "DebitCard", "DANABALANCE", "SHOPEEBALANCE", "LINKAJABALANCE", "OVOBALANCE", "GOPAYBALANCE", "SinarmasVA", "MaybankVA", "DanamonVA", "BNCVA", "BCAVA", "INAVA", "BNIVA", "PermataVA", "MuamalatVA", "BSIVA", "BRIVA", "MandiriVA", "CIMBVA", "StaticMandiriVA", "StaticBCAVA", "QRIS", "Indodana", "Atome", "Kredivo", "Indomaret", "Alfarmart", "POS"]
    today = datetime.datetime.now().strftime("%Y%m%d")

    #批量生成
    n = 8
    amount = "0.01"
    # for paymentType in paymentType:
    order_suffix = f"{n:03d}"
    agentOrderNo = f"AgentOrderNo{today}{n}"
    payOrderNo = f"PayOrder{today}{n}"
    productName = faker.name()
    # productName = '的地方凤凰好好谷歌广告和狗狗狗狗狗个哈哈哈哈嗝哈哈哈哈嗝嗝哈哈哈更回复二哥给狗狗狗法国嗝哈哈哈哈哈哈哈哈哈哈哈狗狗狗狗狗狗个我是通过好好谷歌官方的地方凤凰好好谷歌广告和狗狗狗狗狗个哈哈哈哈嗝哈哈哈一百'

    creat_request_payload = {
        "merchantId": "600008M0001002",
        # "paymentType": paymentType,
        "paymentType": "StaticMandiriVA",
        # "paymentType": "CASH",
        "amount": amount,
        "agentOrderNo": agentOrderNo,
        "payOrderNo": payOrderNo,
        # "sourceAgentOrderNo": "souceAgentOrderNo20250508001",
        # "sourceAgentOrderNo": "20250508001",
        "sourceAgentOrderNo": "",
        # "productName": productName,
        "productName": 'product 1',
        "requestId": "1"
    }

    result = api_client.send_declaration(creat_request_payload)
    pprint(result)
    print(f"\n{n},已完成：amount: {amount}, agentOrderNo：{agentOrderNo}, payOrderNo：{payOrderNo}, productName：{productName}")
        # n += 1
