from pprint import pprint

import requests
import json

url = "http://ai.api.traderwin.com/api/ai/signal/rank.json"

payload = json.dumps({
   "flag": 3,
   "pageSize": 3,
   "index": "1",
   "cmd": "9023",
   "marketType": ""
})
headers = {
   'token': '5a66427c4cc7054622909acafc31d2a6',
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json',
   'Accept': '*/*',
   'Host': 'ai.api.traderwin.com',
   'Connection': 'keep-alive'
}

response = requests.request("GET", url, headers=headers, data=payload)

pprint(response.json())