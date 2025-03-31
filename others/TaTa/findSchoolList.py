import http.client

conn = http.client.HTTPSConnection("admin.hv68.cn")
payload = ''
headers = {
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Accept': '*/*',
   'Host': 'admin.hv68.cn',
   'Connection': 'keep-alive'
}
conn.request("GET", "/prod-api/api/custom/findSchoolList?queryName=%25E6%25B2%2588", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))