import requests


def get_order_list():
    url = base_url + "/tax-center/merchant/exportToEmail"

    headers = {
        "accept": "application/json, text/plain, */*",
        "cookie": "JSESSIONID=B0E0EB0C0B0C0B0C0B0C0B0C0B0C0B0C0B0C0B0C0B0C0B0C0B0C0B0C0B0C0B0C0B0C0B0C0B",
        "langKey": "zh"
    }
    data = {
        "pageSize": 10,
        "pageNum": 1,
        "agent": null,
        "merchantNo": null,
        "merchantType": null,
        "merchantStatus": null,
        "npwp": "11.111.111.1-111.1111",
        "createTimeStart": null,
        "createTimeEnd": null,
        "updateTimeStart": null,
        "updateTimeEnd": null,
        "email": "wrj1272@163.com"
    }
    r = requests.post(url, json=data)
    print(r.json())