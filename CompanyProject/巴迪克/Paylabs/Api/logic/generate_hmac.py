import hashlib
import json
from collections.abc import Mapping, Sequence

# 需要排除的字段
EXCLUDE_KEYS = {'sign', 'page', 'rows', 'limit', 'total', 'totalPage', 'offset', 'hmac'}

def build_param(json_obj, sign_key='sign'):
    """
    构建请求参数字符串
    """
    filtered = {}

    # 过滤无效参数
    for key in sorted(json_obj.keys()):
        if key.lower() in EXCLUDE_KEYS or key == sign_key:
            continue

        value = json_obj[key]

        if value is None:
            continue

        # 排除 List 或 Array 类型
        if isinstance(value, Sequence) and not isinstance(value, str):
            continue

        # 如果是字典，转换为 JSON 字符串
        if isinstance(value, Mapping):
            filtered[key] = json.dumps(value, separators=(',', ':'), ensure_ascii=False)
        else:
            filtered[key] = str(value)

    # 拼接 key=value&...
    param_str = '&'.join(f"{k}={v}" for k, v in filtered.items())
    return param_str

def generate_signature(param_str, secret_key):
    """
    生成 SHA-256 签名
    """
    sign_str = param_str + secret_key
    signature = hashlib.sha256(sign_str.encode('utf-8')).hexdigest()
    return signature.upper()

if __name__ == '__main__':
    params = {
  "agent": {
    "id": "4",
    "agentNo": "12025052809520",
    "agentName": "agent001",
    "contactPhone": "15318544155",
    "contact": "15318544155"
  },
  "accessToken": "3c57d2ccf6fb8ee2aee68a10ca9b807fa5b112d3595eebaca336ae63ce305f59f9f9ffc40dc9e3c89df1e52b4d1092985722de2e50b456b260f2bea9b1ced7ff663c8a7bc9e5949f5655b91f7bb73eaad30c73490c74cc6d2a5e5dc7f545c74f879ccd0e01165ba61695d6a5b0dcbe593559ed4e9e741ede9d695d65b3ce532b",
  "userId": "52",
  "randomStr": "-5361-330211331310839721-3139-111322417150-31517310382451431930-2330031277-2803-294002394824746-1557925261266472392684422841-7704-19465-24687-12788-16904-16820",
  "hmac": "8D4D480A168FE9EBD316B8A962A8F5E761C0AD22B71849D4AAE3320B96FE0278"
}
    secret_key  = "d0e23bc489e17ed45c2ec45173d73de5952ff6cf00fbc8bc0c62e4c6471dc7bc6713080c89809f56a81e1f6f0d4d488b1153e46759704312a3c3e546cd5f09c3677fa005b6611bf0042a291eac68d3addd0360e8074560be9edf49a584c747c3f417300b8b9d3ad9d09451eeca7822cded37f29d4f3ef702f7a477bd88c42d58"

    # 构建参数字符串
    param_str = build_param(params, sign_key="sign")
    print("参数字符串:", param_str)

    # 生成签名
    signature = generate_signature(param_str, secret_key)
    print("签名结果:", signature)
