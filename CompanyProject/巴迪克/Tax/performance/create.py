import datetime
import logging
from pprint import pprint
from typing import Dict

from faker import Faker

from common import TaxAPIBase

class CreateOrderAPI(TaxAPIBase):
    """创建订单API"""

    ENDPOINT_PATH = "/v1.0/declaration/create"

    def create_order(self, payload: Dict) -> Dict:
        """创建订单"""
        return self.send_request(self.ENDPOINT_PATH, payload)

if __name__ == "__main__":
    fake = Faker()
    api_client = CreateOrderAPI(company_name="tax_agent002@linshiyou.com")

    MCC_dict = {7311: 'Advertising', 4511: 'Airlines', 5533: 'Automotive', 7298: 'Beauty Services',
                4899: 'Cable & Streaming Service', 8398: 'Charity / Donation',
                5815: 'Digital Goods: Books, Movies, Music',
                5816: 'Digital Goods: Games', 5817: 'Digital Goods: Applications (Excludes Games)', 8299: 'Education',
                5732: 'Electronics', 5999: 'Fashion', 6012: 'FinancialService', 5499: 'Food & Beverage',
                9399: 'GovernmentServices', 5411: 'Groceries', 7011: 'Hospitality', 6399: 'Insurance', 6533: 'Payment',
                5262: 'Marketplace & Retail Online', 8099: 'Medical Platform', 1520: 'Property',
                6211: 'SecuritiesBrokers',
                4214: 'Shipping & Delivery Service', 4789: 'Transportation', 4722: 'Travel Agencies / Online Ticketing',
                7299: 'Others', 6532: 'Payment Transaction—Customer Financial Institution',
                7392: 'Consulting, Management and Public Relations Services', 5945: 'Game, Toy and Hobby Shops',
                5600: 'Clothing Stores', 5072: 'Hardware Equipment and Supplies',
                6050: 'Quasi Cash–Member Financial Institution',
                5045: 'Computers, Computer Peripheral Equipment, Software',
                8999: 'Professional Services', 8071: 'Dental and Medical Laboratories',
                7531: 'Automotive Body Repair Shops',
                7542: 'Car Washes', 5311: 'Department Stores',
                4225: 'Public Warehousing–Farm Products, Refrigerated Goods, Household Goods Storage',
                8111: 'Attorneys, Legal Services', 4816: 'Computer Network/Information Services',
                7999: 'Recreation Services', 7210: 'Cleaning, Garment and Laundry Services',
                4900: 'Utilities–Electric, Gas, Heating Oil, Sanitary, Water', 8661: 'Organizations, Religious',
                8062: 'Hospitals', 3500: 'Car Rental Agencies',
                5983: 'Fuel Dealers–Coal, Fuel Oil, Liquefied Petroleum, Wood',
                7523: 'Automobile Parking Lots and Garages',
                5995: 'Pet Shops, Pet Food and Supplies', 5944: 'Clock, Jewelry, Watch and Silverware Stores',
                5946: 'Camera and Photographic Supply Stores', 7230: 'Barber and Beauty Shops',
                7929: 'Events and entertainment', 5818: 'Digital Goods: Multi-Category (M)'}

    MCC_list = [7311, 4511, 5533, 7298, 4899, 8398, 5815, 5816, 5817, 8299, 5732, 5999, 6012, 5499, 9399, 5411, 7011,
                6399, 6533, 5262, 8099, 1520, 6211, 4214, 4789, 4722, 7299, 6532, 7392, 5945, 5600, 5072, 6050, 5045,
                8999, 8071, 7531, 7542, 5311, 4225, 8111, 4816, 7999, 7210, 4900, 8661, 8062, 3500, 5983, 7523, 5995,
                5944, 5946, 7230, 7929, 5818]
    paymentType = ["CASH", "CreditCard", "DebitCard", "DANABALANCE", "SHOPEEBALANCE", "LINKAJABALANCE", "OVOBALANCE",
                   "GOPAYBALANCE", "SinarmasVA", "MaybankVA", "DanamonVA", "BNCVA", "BCAVA", "INAVA", "BNIVA",
                   "PermataVA", "MuamalatVA", "BSIVA", "BRIVA", "MandiriVA", "CIMBVA", "StaticMandiriVA", "StaticBCAVA",
                   "QRIS", "Indodana", "Atome", "Kredivo", "Indomaret", "Alfarmart", "POS"]
    today = datetime.datetime.now().strftime("%Y%m%d")

    # 批量生成
    n = 14
    order_suffix = f"{n:03d}"
    # agentOrderNo = f"AgentOrderNo{today}{n}"
    order_no = fake.random_int(min=1, max=1)
    payOrderNo = f"PayOrder{today}{order_no}"
    # productName = faker.name()
    # productName = '的地方凤凰好好谷歌广告和狗狗狗狗狗个哈哈哈哈嗝哈哈哈哈嗝嗝哈哈哈更回复二哥给狗狗狗法国嗝哈哈哈哈哈哈哈哈哈哈哈狗狗狗狗狗狗个我是通过好好谷歌官方的地方凤凰好好谷歌广告和狗狗狗狗狗个哈哈哈哈嗝哈哈哈一百'

    creat_request_payload = {
            "merchantId": "600009M0000001",
            "paymentType": "StaticMandiriVA",
            "amount": "0.01",
            "agentOrderNo": f"AgentOrderNo{today}{order_no}",
            "payOrderNo": payOrderNo,
            "sourceAgentOrderNo": "",
            "productName": fake.name(),
            "requestId": "1"
        }

    # result = api_client.send_declaration(creat_request_payload)
    result = api_client.create_order(creat_request_payload)
    pprint(result)
    if result.get("errCode") == "0":
        logging.info(f"✅ 订单已生成，订单号：{result.get('incomeOrderNo')}")
    else:
        logging.warning(f"⚠️ 订单未生成，错误信息：{result}")

    # print(
    #     f"\n{n},已完成：agentOrderNo：{agentOrderNo}, payOrderNo：{payOrderNo}, productName：{productName}")


    # creat_request_payload = {
    #     "merchantId": "600009M0000001",
    #     "paymentType": "StaticMandiriVA",
    #     "amount": "0.01",
    #     "agentOrderNo": "AgentOrderNo20230515004",
    #     "payOrderNo": "PayOrder20230515004",
    #     "productName": "Test Product",
    #     "requestId": "1"
    # }
    #
    # pprint(result)
