import requests

url = "http://paylabs-test.com/api-platform/dkTrans/listPageDkTrade.json"

headers = {
    "accept": "application/json, text/javascript, */*; q=0.01",
    "accept-language": "zh-CN,zh;q=0.9",
    "cache-control": "no-cache",
    "content-type": "application/json;charset=UTF-8",
    "pragma": "no-cache",
    "proxy-connection": "keep-alive",
    "x-requested-with": "XMLHttpRequest"
}

referrer = "http://paylabs-test.com/platform/paylabs-riskControl-remitrisk.html"
referrer_policy = "strict-origin-when-cross-origin"

body = {
    "accessToken": "c0446338e23ef064491947acc188e58497d1ea9cfbc4d4183e9320718f7ff5a9c1b5804c05e3e41ce07ab3457bfc2146b0d7d8e7265a3c2d4a765c305baa248365911868a24277ac92477a84f3ce41acb9a79c7391a78fca808dae266af1de12d1dd9745ce28588a9afbd5ce168e36ecb44952fdf639bd6e1f8126747beb8171",
    "userId": "113",
    "randomStr": "394323011-18263-23164-13215289327029-3114619194378422043-27101-2970222330-1012327231-2114-21306-2347714942-11570-49246352-16765-12938429-2202313716-624116967-23579",
    "merchantNo": "",
    "merchantType": "",
    "stTotalAmount": "",
    "edTotalAmount": "",
    "stTotalNum": "",
    "edTotalNum": "",
    "stAvgAmount": "",
    "edAvgAmount": "",
    "stMaxAmount": "",
    "edMaxAmount": "",
    "stMinAmount": "",
    "edMinAmount": "",
    "riskLevel": "",
    "merchantStatus": "",
    "salesmanNos": "",
    "agentName": "",
    "merchantGroupTitle": "",
    "startTime": "2025-04-01 00:00:00",
    "endTime": "2025-04-30 23:59:59",
    "order": [{"column": 0, "dir": "asc"}],
    "columns": [
        {"data": "merchantNo", "name": "", "searchable": True, "orderable": False, "search": {"value": "", "regex": False}},
        {"data": "merchantName", "name": "", "searchable": True, "orderable": False, "search": {"value": "", "regex": False}},
        {"data": "merchantType", "name": "", "searchable": True, "orderable": False, "search": {"value": "", "regex": False}},
        {"data": "merRiskAssessment", "name": "", "searchable": True, "orderable": False, "search": {"value": "", "regex": False}},
        {"data": "sumSuccessAmount", "name": "sumSuccessOrderAmount", "searchable": True, "orderable": True, "search": {"value": "", "regex": False}},
        {"data": "sumSuccessOrderNumber", "name": "sumSuccessOrderNumber", "searchable": True, "orderable": True, "search": {"value": "", "regex": False}},
        {"data": "avgSuccessAmount", "name": "avgSuccessOrderAmount", "searchable": True, "orderable": True, "search": {"value": "", "regex": False}},
        {"data": "maxSuccessAmount", "name": "maxSuccessOrderAmount", "searchable": True, "orderable": True, "search": {"value": "", "regex": False}},
        {"data": "minSuccessAmount", "name": "minSuccessOrderAmount", "searchable": True, "orderable": True, "search": {"value": "", "regex": False}},
        {"data": "merchantStatus", "name": "", "searchable": True, "orderable": False, "search": {"value": "", "regex": False}},
        {"data": "salesmanName", "name": "", "searchable": True, "orderable": False, "search": {"value": "", "regex": False}},
        {"data": "agentName", "name": "", "searchable": True, "orderable": False, "search": {"value": "", "regex": False}},
        {"data": "merchantGroupTitle", "name": "", "searchable": True, "orderable": False, "search": {"value": "", "regex": False}},
        {"data": "opt", "name": "", "searchable": True, "orderable": False, "search": {"value": "", "regex": False}}
    ],
    "search": {"value": "", "regex": False},
    "hmac": "9ebeda99f962830ed22e56f7e484f3426798a72c6fa7abbcf2ec7861680e86fe",
    "rows": "10",
    "page": 1
}

try:
    response = requests.post(url, headers=headers, json=body, cookies=requests.cookies.RequestsCookieJar())
    response.raise_for_status()
    print(response.json())
except requests.exceptions.RequestException as e:
    print(f"请求出错: {e}")
except ValueError as e:
    print(f"解析响应出错: {e}")