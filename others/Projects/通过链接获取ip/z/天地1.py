import requests

# 替换为你的天地图API Key
api_key = '29edc6c3e99bffcca73d686971b3b827'

# 地址信息
address = '北京市延庆区延庆镇莲花池村前街50夕阳红养老院'

# 地理编码API接口URL
geocoder_url = f'http://api.tianditu.gov.cn/geocoder?ds={{"keyWord":"{address}"}}&tk={api_key}'

# 发送HTTP GET请求
response = requests.get(geocoder_url)

# 解析返回的JSON数据
geocoder_data = response.json()

# 输出结果
print(geocoder_data)
