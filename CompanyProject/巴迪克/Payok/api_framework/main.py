import os

from payok_api import PayokAPI


# 配置参数
# base_url = "https://your_api_domain.com"
# base_url = "https://192.168.0.224:8994"
base_url = "https://payok-test.com"
merchant_id = "010095"
private_key_path = "private_key.pem"
print('文件存在' if os.path.exists(private_key_path) else '文件不存在')
public_key_path = "public_key.pem"

# 初始化API对象
payok_api = PayokAPI(base_url, merchant_id, private_key_path, public_key_path)

# 账户可用性查询
request_time = "2025-03-27T08:42:20.451Z"
amount = "10000.00"
benificiary_account_info = {
    "number": "0000000001",
    "holderName": "Test",
    "orgName": "Bank BCA",
    "orgCode": "CENAIDJA",
    "orgId": "014"
}
merchant_order_id = "6010095DK_PAY1719477740451"
country_code = "IDN"
currency = "RP"
language = "EN"

account_availability_result = payok_api.account_availability_query(request_time, amount, benificiary_account_info,
                                                                 merchant_order_id, country_code, currency, language)
print("账户可用性查询结果:", account_availability_result)

# 发起代付
if account_availability_result.get('code') == 'SUCCESS':
    inquiry_token = account_availability_result.get('inquiryToken')
    notification_url = "http://merchant-api.com/test/notify/20240627164210123/DK_PAY/6"
    card_holder_info = {
        "zip": "123456",
        "firstName": "John",
        "lastName": "Don",
        "country": "Indonesia",
        "address": "Merchant Address",
        "city": "Jakarta",
        "phone": "223345678",
        "email": "test@logic.com"
    }
    initiate_payment_result = payok_api.initiate_payment(request_time, amount, benificiary_account_info,
                                                        merchant_order_id, country_code, currency, language, inquiry_token,
                                                        notification_url, "Transfering Test", card_holder_info)
    print("发起代付结果:", initiate_payment_result)

# 代付订单查询
payment_order_query_result = payok_api.payment_order_query(request_time, merchant_order_id)
print("代付订单查询结果:", payment_order_query_result)

# 账户余额查询
account_balance_query_result = payok_api.account_balance_query(request_time)
print("账户余额查询结果:", account_balance_query_result)
