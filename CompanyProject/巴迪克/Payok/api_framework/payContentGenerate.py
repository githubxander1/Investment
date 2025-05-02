import requests

def generate_pay_order():
    # 请求的URL
    url = "http://payok-test.com/api-merchant/getCode/payContentGenerated.json"

    # 请求头
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/x-www-form-urlencoded"
    }

    # 引用页
    referrer = "http://payok-test.com/merchant/payok-tool-paymentGenerator.html"
    headers["referrer"] = referrer

    # 请求体数据
    data = {
        "mchId": "020099",
        "channel": "",
        "goodsInfo": "001",
        "payer": "还款人1",
        "lang": "ch",
        "productName": "",
        "orderNo": "20250312154151171",
        "mobilePhone": "15318544154",
        "amount": "10000",
        "notifyUrl": "https://m.payok.id",
        "callbackUrl": "https://m.payok.id",
        "accessToken": "a4343673203a445b97d469c99cf6730c",
        "userId": "1209",
        "randomStr": "bed40478-3b4b-4ea3-9345-2ba812cd14fc",
        "hmac": "58FFD2CBEDFBBB7EC9999D5485C305CD"
    }

    # 发送POST请求
    try:
        response = requests.post(url, headers=headers, data=data)
        # 检查响应状态码
        response.raise_for_status()
        # 打印响应内容
        print(response.json())
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request error occurred: {req_err}")
    except ValueError as json_err:
        print(f"JSON decoding error occurred: {json_err}")

if __name__ == '__main__':
    generate_pay_order()