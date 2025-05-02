import requests
import json

def send_api_request():
    url = 'https://api-domian.com/api-pay/remit/V3.2/account/inquiry'
    headers = {
        'sign': 'isKl7JFKVEMeEh/pGwb/bpgRELcNn3veooRCMCQtjoGWR36Yq+8qaI2F8owpaNUNCcNyg7PX/PU/T5jH/GeejpXCrIhUwmEOIja8/Pw4RYyFjwzLzBCNnJYF1u1GZNtCCEh8zGKti2GZXf3NyUF5YfD0Q/bcO8kvKqrxtXb/biORH4/CeULFSzUvG/n3vHAAA9rlgBn51c8GuA+AGlEyWp9ntlCOy4N4A21faJZsBwudJBBRgBiZPVo6amZtZJHhWtg8UfHyYsXjokFwPN++vibd/XpeRDzhp5zvKh3y55cVveoX6YKTk00wYfLVyHg9yQymD+s52DTy3AE90DG3XA==',
        'Content-Type': 'application/json'
    }
    data = {
        "requestTime": "2024-06-27T08:42:20.451Z",
        "amount": "20000.00",
        "benificiaryAccountInfo": {
            "number": "0000000001",
            "holderName": "Test",
            "orgName": "Bank BCA",
            "orgCode": "CENAIDJA",
            "orgId": "014"
        },
        "merchantId": "010095",
        "countryCode": "IDN",
        "currency": "RP",
        "language": "EN",
        "merchantOrderId": "6010095DK_PAY1719477740451"
    }
    try:
        # 发送POST请求
        response = requests.post(url, headers=headers, data=json.dumps(data))
        # 检查响应状态码
        response.raise_for_status()
        return response.json()
    except requests.exceptions.HTTPError as http_err:
        print(f'HTTP error occurred: {http_err}')
    except json.JSONDecodeError:
        print('Failed to decode JSON response.')
    except Exception as err:
        print(f'Other error occurred: {err}')

# 调用函数发送请求
result = send_api_request()
if result:
    print(result)