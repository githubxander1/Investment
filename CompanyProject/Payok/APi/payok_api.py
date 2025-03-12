import requests
from payok_utils import generate_signature


class PayokAPI:
    def __init__(self, base_url, merchant_id, private_key_path, public_key_path):
        self.base_url = base_url
        self.merchant_id = merchant_id
        self.private_key_path = private_key_path
        self.public_key_path = public_key_path

    def account_availability_query(self, request_time, amount, benificiary_account_info, merchant_order_id, country_code,
                                   currency, language):
        api_url = self.base_url + '/api-pay/remit/V3.2/account/inquiry'
        data = {
            "requestTime": request_time,
            "merchantId": self.merchant_id,
            "merchantOrderId": merchant_order_id,
            "amount": amount,
            "countryCode": country_code,
            "currency": currency,
            "language": language,
            "benificiaryAccountInfo": benificiary_account_info
        }
        sign = generate_signature(self.private_key_path, data, api_url)
        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "sign": sign
        }
        response = requests.post(api_url, headers=headers, json=data)
        return response.json()

    def initiate_payment(self, request_time, amount, benificiary_account_info, merchant_order_id, country_code, currency,
                         language, inquiry_token, notification_url=None, description=None, card_holder_info=None):
        api_url = self.base_url + '/api-pay/remit/V3.2/order/create'
        data = {
            "requestTime": request_time,
            "merchantId": self.merchant_id,
            "merchantOrderId": merchant_order_id,
            "amount": amount,
            "countryCode": country_code,
            "currency": currency,
            "language": language,
            "inquiryToken": inquiry_token,
            "benificiaryAccountInfo": benificiary_account_info
        }
        if notification_url:
            data["notificationUrl"] = notification_url
        if description:
            data["description"] = description
        if card_holder_info:
            data["cardHolderInfo"] = card_holder_info

        sign = generate_signature(self.private_key_path, data, api_url)
        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "sign": sign
        }
        response = requests.post(api_url, headers=headers, json=data)
        return response.json()

    def payment_order_query(self, request_time, merchant_order_id):
        api_url = self.base_url + '/api-pay/remit/V3.2/order/query'
        data = {
            "requestTime": request_time,
            "merchantId": self.merchant_id,
            "merchantOrderId": merchant_order_id
        }
        sign = generate_signature(self.private_key_path, data, api_url)
        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "sign": sign
        }
        response = requests.post(api_url, headers=headers, json=data)
        return response.json()

    def account_balance_query(self, request_time):
        api_url = self.base_url + '/api-pay/remit/V3.2/balance/query'
        data = {
            "requestTime": request_time,
            "merchantId": self.merchant_id
        }
        sign = generate_signature(self.private_key_path, data, api_url)
        headers = {
            "Content-Type": "application/json;charset=utf-8",
            "sign": sign
        }
        response = requests.post(api_url, headers=headers, json=data)
        return response.json()
