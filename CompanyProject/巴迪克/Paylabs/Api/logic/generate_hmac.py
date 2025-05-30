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
    params ={
  "code": "412918",
  "rechargeApplyNo": "202505300600007",
  "pwd": "qwe123",
  "accessToken": "2793403748d9aee9a85967bc14aafc664a84a6b1ae154001dfc4b7c8444c1ce26ba9c3a3d32a180c854b5975a9664c4ecfeeae521cacff2e9fc42295d646268e52b844608928db27920d66dc8aebd83c332fec3c11e2480a473d03501a8eb31bd8c8c6a1bc689b0a29b26de98eaeafb6f2e1f86aee89e54112ef178f5180fdfe",
  "userId": "52",
  "randomStr": "24642-144283131243211270815022-16541-2108516099874717341-22377-9624325538224-4781-10807-12146225951191-16898206061559520403473018203-25471-220304861-128536010",
  "hmac": "54f3698dc34f33a73a5a6191d178c1aa4fcc1e36e9c344b91a50f9a4cd33b0a4"
}
    secret_key  = "8022c85f57203dc025d007a2a2e5a7cff26868a3888774ca2e238f3757c3a3311ef0b6006a7f16431e5b722d9a7f2e7243172ad787d536331f29a7b6ccdb8173387118b5c9e20e3b6a3e32130351cdb62043cbc70aaa6c6a6bbb4ef86be7b45e0eba15573e29dfd25c10c32db4b168836e82edf689cf193fc62fc92e5d8ce16f"

    # 构建参数字符串
    param_str = build_param(params, sign_key="sign")
    print("参数字符串:", param_str)

    # 生成签名
    signature = generate_signature(param_str, secret_key)
    print("签名结果:", signature)
