import http.client

conn = http.client.HTTPSConnection("admin.hv68.cn")
payload = ''
headers = {
   'token': 'b994aaea1a2342c49329dc036469ba1e',
   'User-Agent': 'Apifox/1.0.0 (https://apifox.com)',
   'Accept': '*/*',
   'Host': 'admin.hv68.cn',
   'Connection': 'keep-alive'
}
conn.request("GET", "/prod-api/api/custom/getPersonMsg?platformType=1&openid=otm7z6Cz6G70yB6t2EPQAbCc3i8w", payload, headers)
res = conn.getresponse()
data = res.read()
print(data.decode("utf-8"))