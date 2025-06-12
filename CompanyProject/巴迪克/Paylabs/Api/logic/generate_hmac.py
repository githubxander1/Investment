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
  "code": "943420",
  "rechargeApplyNo": "202506120600004",
  "pwd": "qwe123",
  "accessToken": "94a98f46169e05d2885f608af5ec0739f294f43b613384826fae56432def3bf2e24a48254923bef211f60ac4f55dd359a8d7a01b9906f73db84e62422b49258580b7a546676dc0ccc4a15785865db5e559705fc1ea68347ec78a090b326d34d56b44d7f18a0c96d23ba0b4c677c36f3a0de79606bd11042a08e3b20375cc36bc",
  "userId": "52",
  "randomStr": "31379-3888-18568-12145-3294-22418-26126-24297-257511938558123751910-17427-27890366806420779-4983476417452-74732656115609-21222-2680329273-20878-25239-1521927790",
  "hmac": "3a4f69a96491f43315c5bb6b23a8d1606d0c81e89982a8ad2eaab4bd4438f40c"
}
    secret_key  = "535485879a8a0f42b434bc6abcdf0047a051c5e02410f1d0cba1fb59798524444011279ebbdb44289dbf70b726ba6020d87d47defa3bd54e62db48291efefc1c2f0929679b3164bb38e32e144ed20467d118ffeb5f546952572db64f8343d55a31215a9c53ebd35cef1d5ee0aa8ed0485a4cafd57e2dd347b93523cf724b5bba"

    # 构建参数字符串
    param_str = build_param(params, sign_key="sign")
    print("参数字符串:", param_str)

    # 生成签名
    signature = generate_signature(param_str, secret_key)
    print("签名结果:", signature)
