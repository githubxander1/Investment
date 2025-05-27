# import hmac
# import hashlib
# from collections.abc import Mapping, Collection
#
# EXCLUDE_KEYS = {'hmac', 'page', 'rows', 'limit', 'total', 'totalPage', 'offset'}
#
#
# def is_valid_param(key, value):
#     """判断是否需要参与签名"""
#     if key in EXCLUDE_KEYS:
#         return False
#     if value is None:
#         return False
#     if isinstance(value, (list, set, dict)) and not value:
#         return False
#     if isinstance(value, Collection) and not isinstance(value, (str, bytes)):
#         return False
#     return True
#
#
# def generate_sign(params: dict, secret_key: str) -> str:
#     # 过滤无效参数
#     filtered = {k: v for k, v in params.items() if is_valid_param(k, v)}
#
#     # 按 key 排序
#     sorted_params = sorted(filtered.items(), key=lambda x: x[0])
#
#     # 构造 key=value&key=value 格式字符串
#     param_str = "&".join(f"{k}={v}" for k, v in sorted_params)
#
#     # 拼接 secretKey
#     sign_str = param_str + secret_key
#
#     # 生成 HMAC-SHA256 签名
#     signature = hmac.new(
#         secret_key.encode(),
#         sign_str.encode(),
#         hashlib.sha256
#     ).hexdigest()
#
#     return signature
#
#
# def generate_hmac_sha256_sign(params, secret_key):
#     sorted_params = "&".join(f"{k}={v}" for k, v in sorted(params.items()))
#     sign_str = sorted_params + secret_key
#     signature = hmac.new(secret_key.encode(), sign_str.encode(), hashlib.sha256).hexdigest()
#     return signature


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

# # 示例数据
# json_obj = {
#     "username": "zhangsan",
#     "age": 20,
#     "gender": "",
#     "sign": "abcd1234",
#     "page": 1,
#     "tags": ["a", "b"],
#     "address": {"city": "Beijing", "district": "Haidian"},
#     "empty_list": [],
# }
#
# secret_key = "your_very_secret_key_here"
#
# # 构建参数字符串
# param_str = build_param(json_obj, sign_key="sign")
# print("参数字符串:", param_str)
#
# # 生成签名
# signature = generate_signature(param_str, secret_key)
# print("签名结果:", signature)


if __name__ == '__main__':
#     params={
#   "bankAccountNo": "15354879",
#   "amount": 11111,
#   "withPwd": "qwe123456.ID",
#   "cashAdvanceLetter": "",
#   "bankName": "中国人民银行",
#   "remitType": "3",
#   "accessToken": "05900b7bb9f5bcfdf51f907eb3c7df35baed686dfd67beef61c515c2f7aee650c40f123bf1c921be1c9291e0e41e0e1b6e507560a0960ad7fdaa84a837175737166c6acc6a6aad47055e41dc4efe0dc003adde2f35e44254df8ceedb4ec2eab836b3e56c2160c66c5895083a8d34f69fbe7f1d6aee9070918a571b651efa770d",
#   "userId": "92",
#   "randomStr": "-19937-16470-25263-9297-1006512569-5668-772932159-1739239120811-29334946-100491902830702-89-232077653-309211574121498-19166-2451-2028829543-14878-2835629393-25690",
#   "hmac": "1E02C5E5EAAB07886D2836238D5BF04D42B4FBD033F3E0696668A133B7E7A6E0"
# }
#     secret_key  = "3e92b6595ce0440d386a5fe63a1e2c41c1140da09efb86cac6a5346ead36c4df0e4001bf97c7bee83e68150f1a8d22285e0418fc3eafccd1242fac80c7dd47821ea3f43b8c88bdd4c00079be62e6546d104b1e5efc628c009a4b3bc5da227505d46a8c04af0185ae4cc5edf0d7f516aaade123b90764140dddf8cc75e359778d"
    params = {
  "referenceProductId": "467",
  "cloneProductId": 468,
  "accessToken": "6b4d3881b81205d36cf943cc249b488cd859da997907236560c594cef5962b515ecc6879820667ae99d963b91c99015235509e6789a480e410b4c1cdbafb10ba3dd524168c9b84fca222375c2afccd0bac029b22cd3abe9ca210c33a94576d728c8253dbbd998a73b266390a6a50919eb9b861d5bacaa4c7c5744e82334c134a",
  "userId": "52",
  "randomStr": "-373021771-3897-20884-13537797827372-4478-100792837126480-10200-21258199974899565-29584-17258-2070524321235602829211786-167789074-2299223987-176425343-10546-19467",
  "hmac": "FF6FDB99331787A7846DF58748E675D61F8A4B8629F9CA5EED78B47D4BD97CFE"
}
    secret_key  = "4723159ffdcd94d9097aea453ab39bc7e30d5471947119bc09c07d710c1984073abb5b0cb493be7cf33ee83108211d4aa950655ae67792be937a8e5eef0dd39ddf2a72f1e51a391f2689cb88fa0e3f129b23895087d39d0b42f70d33d02da3b1346930844620a466371f7364ca13f044a6b7c27689e85d5e76f8d542cec314a8"
    # print(generate_hmac_sha256_sign(params, secret_key))
    # print(generate_sign(params, secret_key))
    # 构建参数字符串
    param_str = build_param(params, sign_key="sign")
    print("参数字符串:", param_str)

    # 生成签名
    signature = generate_signature(param_str, secret_key)
    print("签名结果:", signature)
