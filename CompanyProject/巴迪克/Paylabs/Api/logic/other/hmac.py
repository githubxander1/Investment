# public String buildParam(Map<String, Object> jsonObj, String signKey) {
#     StringBuilder param = new StringBuilder();
#     String[] keys = jsonObj.keySet().toArray(new String[0]);
#     Arrays.sort(keys); // 参数名按 ASCII 字典顺序排序
#
#     for (String key : keys) {
#         // 排除签名字段、分页字段（signKey、page、rows、limit、total、totalPage、offset）
#         if (StringUtils.isNotEmpty(signKey) && signKey.equals(key)) {
#             continue;
#         }
#         if ("page".equalsIgnoreCase(key)) {
#             continue;
#         }
#         if ("rows".equalsIgnoreCase(key)) {
#             continue;
#         }
#         if ("limit".equalsIgnoreCase(key)) {
#             continue;
#         }
#         if ("total".equalsIgnoreCase(key)) {
#             continue;
#         }
#         if ("totalPage".equalsIgnoreCase(key)) {
#             continue;
#         }
#         if ("offset".equalsIgnoreCase(key)) {
#             continue;
#         }
#
#         Object value = jsonObj.get(key);
#
#         if (value != null) {
#             if (value instanceof List || value instanceof String[]) {
#                 continue; // 排除 List 和 数组类型
#             } else if (value instanceof Map) {
#                 param.append(key).append("=").append(JsonHelper.toJson(value)).append("&");
#             } else {
#                 param.append(key).append("=").append(value).append("&");
#             }
#         }
#     }
#
#     return param.substring(0, param.length() - 1); // 去掉最后一个 &
# }
# String signature = DigestUtils.sha256Hex(src + secretKey).toUpperCase();
