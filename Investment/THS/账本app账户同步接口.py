import requests
from pprint import pprint

url = "https://tzzb.10jqka.com.cn/caishen_httpserver/tzzb/caishen_fund/pc/asset/v1/stock_position"

payload = {
  'terminal': "1",
  'version': "0.0.0",
  'userid': "641926488",
  'user_id': "641926488",
  'manual_id': "",
  'fund_key': "133508019",
  'rzrq_fund_key': ""
}

headers = {
  'User-Agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/135.0.0.0 Safari/537.36",
  'Accept': "application/json, text/plain, */*",
  'Accept-Encoding': "gzip, deflate, br, zstd",
  'sec-ch-ua-platform': "\"Windows\"",
  'sec-ch-ua': "\"Chromium\";v=\"135\", \"Not-A.Brand\";v=\"8\"",
  'sec-ch-ua-mobile': "?0",
  'origin': "https://tzzb.10jqka.com.cn",
  'sec-fetch-site': "same-origin",
  'sec-fetch-mode': "cors",
  'sec-fetch-dest': "empty",
  'referer': "https://tzzb.10jqka.com.cn/pc/index.html",
  'accept-language': "zh-CN,zh;q=0.9",
  'priority': "u=1, i",
  'Cookie': "shoudNotCookieRefresh=1; u_ukey=A10702B8689642C6BE607730E11E6E4A; u_uver=1.0.0; u_dpass=fou%2F0LouwneNgg4aLANzv2enaqgkV1cyTWuTdDYhEScfYqYIyaTF3YeykygdN%2FRBHi80LrSsTFH9a%2B6rtRvqGg%3D%3D; u_did=CC37D8EBB29D40329773B6DEFBD27A2F; u_ttype=WEB; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3LDExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzU4MTExNTk1Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTE1OTg3M2ZhNzYyZjc0NmVmNzZhMjgyNzNjMTY5YTAzOmRlZmF1bHRfNTox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=c70e5cfdec172dd60b4e33da5350c9df; user_status=0; utk=2c7de60a214d547dd20f9089d3ef8b0d; sess_tk=eyJ0eXAiOiJKV1QiLCJhbGciOiJFUzI1NiIsImtpZCI6InNlc3NfdGtfMSIsImJ0eSI6InNlc3NfdGsifQ.eyJqdGkiOiIwMzlhMTYzYzI3Mjg2YWY3NmU3NDJmNzZmYTczOTgxNTEiLCJpYXQiOjE3NTgxMTE1OTUsImV4cCI6MTc2MDc4OTk5NSwic3ViIjoiNjQxOTI2NDg4IiwiaXNzIjoidXBhc3MuMTBqcWthLmNvbS5jbiIsImF1ZCI6IjIwMjAxMTE4NTI4ODkwNzIiLCJhY3QiOiJvZmMiLCJjdWhzIjoiMzJiZGRiOWJlMTM1ZTY5NWUzNjlkYzBhZDcxOWIxZjIwNDlmYWNiYmEzMGVlYjcwMDkzNzQzNWFkMzkwM2Q5NSJ9.VBxfCBikgTJjC4ioQtoDOu1a0NooRz25PHy-muzrZS6LSKZCgmUoTHYogqWKAs7H2EcAT-ufy_CzN8u8N55rQQ; cuc=sufmt4wli5k8; v=AzhS_mYPpFE3sMjViWIsY1gVCe3PoZwr_gVwr3KphHMmjdbTGrFsu04VQDHB"
}

response = requests.post(url, data=payload, headers=headers)

pprint(response.json())