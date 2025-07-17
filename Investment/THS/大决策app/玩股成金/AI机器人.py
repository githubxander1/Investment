from pprint import pprint

import requests
import json

url = "http://ai.api.traderwin.com/api/ai/robot/get.json?token=5a66427c4cc7054622909acafc31d2a6"

payload = json.dumps({
   "cmd": "9015",
   "robotId": "2"
})
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Content-Type': 'application/json',
   'Accept': '*/*',
   'Host': 'ai.api.traderwin.com',
   'Connection': 'keep-alive'
}

response = requests.request("GET", url, headers=headers, data=payload)

pprint(response.json())