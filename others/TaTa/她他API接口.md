---
title: 她他API接口
language_tabs:
  - shell: Shell
  - http: HTTP
  - javascript: JavaScript
  - ruby: Ruby
  - python: Python
  - php: PHP
  - java: Java
  - go: Go
toc_footers: []
includes: []
search: true
code_clipboard: true
highlight_theme: darkula
headingLevel: 2
generator: "@tarslib/widdershins v4.0.28"

---

# 她他API接口

Base URLs:

* <a href="https://admin.hv68.cn/prod-api">admin.hv68.cn: https://admin.hv68.cn/prod-api</a>

# Authentication

# 2024-前端对客接口文档/用户联系地址相关接口

<a id="opIdedit_34"></a>

## PUT 修改用户联系地址

PUT /api/customAddress/update

修改用户联系地址

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[CustomAddressDto](#schemacustomaddressdto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RVoid](#schemarvoid)|

<a id="opIdadd_35"></a>

## POST 新增用户联系地址

POST /api/customAddress/create

新增用户联系地址

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[CustomAddressDto](#schemacustomaddressdto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RVoid](#schemarvoid)|

<a id="opIdgetCustomAddressList"></a>

## GET 获取用户联系地址详细信息

GET /api/customAddress/getCustomAddressInfo

获取用户联系地址详细信息

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RListCustomAddressVo](#schemarlistcustomaddressvo)|

<a id="opIdremove_41"></a>

## DELETE 删除用户联系地址

DELETE /api/customAddress/remove/{ids}

删除用户联系地址

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ids|path|array[integer]| 是 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RVoid](#schemarvoid)|

# 2024-前端对客接口文档/用户相关接口

<a id="opIdupdateUserBaseInfo"></a>

## PUT 用户修改基本信息

PUT /api/custom/center/base-info

用户修改基本信息

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[CustomCenterBaseInfoDto](#schemacustomcenterbaseinfodto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RVoid](#schemarvoid)|

<a id="opIdverifyPhone"></a>

## POST 校验用户手机号

POST /api/custom/verifyPhone

校验用户手机号

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[VerifyPhoneReqDto](#schemaverifyphonereqdto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[R](#schemar)|

<a id="opIdsaveTest"></a>

## POST 性格测试保存到个人信息

POST /api/custom/saveMbti/{testCode}

性格测试保存到个人信息

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|testCode|path|string| 是 |测试参数|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|测试编码|[R](#schemar)|

<a id="opIdsaveUserBaseInfo"></a>

## POST 新用户保存基本资料

POST /api/custom/base-info

新用户保存基本资料

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[CustomBaseInfoDto](#schemacustombaseinfodto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RBoolean](#schemarboolean)|

<a id="opIdverificationCode"></a>

## GET 发送短信验证码

GET /api/custom/verificationCode/{phoneNum}

发送短信验证码

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|phoneNum|path|string| 是 |手机号|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[R](#schemar)|

<a id="opIdgetPersonMsg"></a>

## GET 获取个人基本信息

GET /api/custom/getPersonMsg

获取个人基本信息

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|platformType|query|integer(int32)| 是 |0 h5用户 1 小程序用户|
|openid|query|string| 是 |openid|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RLoginCustomVo](#schemarlogincustomvo)|

<a id="opIdfindSchoolList"></a>

## GET 根据输入内容获取大学名称列表

GET /api/custom/findSchoolList

根据输入内容获取大学名称列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|queryName|query|string| 是 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RListString](#schemarliststring)|

<a id="opIdexistSchoolName"></a>

## GET existSchoolName

GET /api/custom/existSchoolName

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|schoolName|query|string| 是 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RBoolean](#schemarboolean)|

# 2024-前端对客接口文档/登录相关接口

<a id="opIdloginByPhone"></a>

## POST 小程序获取手机号[静默登录]

POST /api/wx/phoneToLogin

小程序获取手机号[静默登录]

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[WxCodeLoginDto](#schemawxcodelogindto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RWxLoginVo](#schemarwxloginvo)|

<a id="opIdlogout_1"></a>

## POST 退出登录

POST /api/wx/logout

退出登录

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RVoid](#schemarvoid)|

<a id="opIdlogin_1"></a>

## POST 统一登录

POST /api/wx/login

统一登录

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[LoginDto](#schemalogindto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RWxLoginVo](#schemarwxloginvo)|

<a id="opIdloginByWx"></a>

## POST 小程序登录

POST /api/wx/jsCodeToLogin

小程序登录

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[WxLoginDto](#schemawxlogindto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RWxLoginVo](#schemarwxloginvo)|

<a id="opIdcode2Token"></a>

## POST h5登录获取token

POST /api/wx/code2Token

h5登录获取token

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[WxRequestDto](#schemawxrequestdto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RWxLoginVo](#schemarwxloginvo)|

<a id="opIdwxTokenCheck"></a>

## GET 公众号签名验证[无需对接]

GET /api/wx/wxTokenCheck

公众号签名验证[无需对接]

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|signature|query|string| 是 |openid|
|timestamp|query|string| 否 |none|
|nonce|query|string| 否 |none|
|echostr|query|string| 否 |none|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|Inline|

### 返回数据结构

# 2024-前端对客接口文档/认证相关接口

<a id="opIdsubmitVerify"></a>

## POST 用户提交认证

POST /api/verify/submitVerify

用户提交认证

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[CustomVerifyDto](#schemacustomverifydto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RBoolean](#schemarboolean)|

<a id="opIdgetVerifyStatus"></a>

## GET 用户认证状态

GET /api/verify/getVerifyStatus

用户认证状态

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|customerId|query|integer(int64)| 否 |用户编号|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RCustomVerifyStatusVo](#schemarcustomverifystatusvo)|

<a id="opIdgetVerifyDetail"></a>

## GET 用户认证详情 1-实名认证 2-学历认证 3-工作认证

GET /api/verify/detail

用户认证详情 1-实名认证 2-学历认证 3-工作认证

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|verifyType|query|integer(int32)| 是 |1实名认证，2 学历认证 3工作认证|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RCustomVerifyRespVo](#schemarcustomverifyrespvo)|

# 2024-前端对客接口文档/互选池相关接口

<a id="opIdshareId"></a>

## POST 生成互选池分享编号

POST /api/publicChoose/shareId

生成互选池分享编号

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RString](#schemarstring)|

<a id="opIdlike"></a>

## POST 互选点击喜欢或取消喜欢
 status: 0=取消,1=喜欢,2=不喜欢

POST /api/publicChoose/like

互选点击喜欢或取消喜欢
 status: 0=取消,1=喜欢,2=不喜欢

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[LikeDto](#schemalikedto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[R](#schemar)|

<a id="opIdcollect"></a>

## POST 点击收藏或取消收藏 1=收藏 0=取消收藏

POST /api/publicChoose/collect

点击收藏或取消收藏 1=收藏 0=取消收藏

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[CollectDto](#schemacollectdto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[R](#schemar)|

<a id="opIdgetCustomDetail"></a>

## GET 根据shareCode获取客户详细信息

GET /api/publicChoose/shareCustomDetail

根据shareCode获取客户详细信息

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|platformType|query|integer(int32)| 是 |0 h5用户 1 小程序用户|
|shareCode|query|string| 是 |shareCode|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RCustomDetailVo](#schemarcustomdetailvo)|

<a id="opIdrecommend"></a>

## GET 每日推荐查询

GET /api/publicChoose/recommend

每日推荐查询

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|amount|query|integer(int32)| 是 |每日每种类型推荐数量|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RListCustomBaseVo](#schemarlistcustombasevo)|

<a id="opIdlist_41"></a>

## GET 互选池用户列表

GET /api/publicChoose/list

互选池用户列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|blindBox|query|integer(int32)| 是 |是否拆盲盒：1-拆盲盒展示[打码照片] 2-非拆盲盒展示[正常照片] 3-无照片展示|
|shareId|query|string| 否 |分享编号|
|pageSize|query|integer(int32)| 否 |分页大小|
|pageNum|query|integer(int32)| 否 |当前页数|
|orderByColumn|query|string| 否 |排序列|
|isAsc|query|string| 否 |排序的方向desc或者asc|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[TableDataInfoCustomBaseVo](#schematabledatainfocustombasevo)|

<a id="opIdlistForLike"></a>

## GET 互选点击取消喜欢、喜欢、不喜欢

GET /api/publicChoose/listForLike

互选点击取消喜欢、喜欢、不喜欢

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|loverStatus|query|integer(int32)| 是 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RListCustomBaseVo](#schemarlistcustombasevo)|

<a id="opIdgetCustomDetail_1"></a>

## GET 根据loverId获取客户详细信息

GET /api/publicChoose/getCustomDetail

根据loverId获取客户详细信息

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|loverId|query|integer(int64)| 是 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RCustomDetailVo](#schemarcustomdetailvo)|

# 2024-前端对客接口文档/支付相关接口

<a id="opIdrefund"></a>

## POST 退款

POST /api/pay/unifiedRefund

退款

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[RefundDto](#schemarefunddto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[R](#schemar)|

<a id="opIdunifiedOrder"></a>

## POST 统一下单

POST /api/pay/unifiedOrder

统一下单

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[PayDto](#schemapaydto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RUnifiedPayResponseVO](#schemarunifiedpayresponsevo)|

<a id="opIdcloseOrderByOrderNo"></a>

## POST 关闭订单

POST /api/pay/closeOrderByOrderNo

关闭订单

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[CloseOrderDto](#schemacloseorderdto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[R](#schemar)|

# 2024-前端对客接口文档/文件上传相关接口[临时方案]

<a id="opIdupload_2"></a>

## POST 文件上传

POST /api/oss/upload

文件上传

> Body 请求参数

```yaml
file: ""

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» file|body|string(binary)| 是 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[ROssFileVo](#schemarossfilevo)|

# 2024-前端对客接口文档/MBTI性格测试接口

<a id="opIduserInfo"></a>

## POST MBTI 个人测试性格信息

POST /api/mbti/userInfo/{testCode}

MBTI 个人测试性格信息

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|testCode|path|string| 是 |测试ID|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|测试信息|[RTraitMbtiUserTestVo](#schemartraitmbtiusertestvo)|

<a id="opIduserInfoList"></a>

## POST MBTI个人测试列表

POST /api/mbti/userInfo/list

MBTI个人测试列表

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[MbtiResultListQueryDto](#schemambtiresultlistquerydto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|测试列表|[RListTraitMbtiTestResultVo](#schemarlisttraitmbtitestresultvo)|

<a id="opIdtest"></a>

## POST MBTI个人性格测试

POST /api/mbti/test

MBTI个人性格测试

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[MbtiQuestionTestParam](#schemambtiquestiontestparam)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|测试编码|[RString](#schemarstring)|

<a id="opIdquestions"></a>

## POST 性格题目

POST /api/mbti/questions

性格题目

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[MbtiInfoQuestionQueryDto](#schemambtiinfoquestionquerydto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|性格问题|[RListTraitMbtiQuestionInfoVo](#schemarlisttraitmbtiquestioninfovo)|

# 2024-前端对客接口文档/客户匹配设置相关接口

<a id="opIdupdate"></a>

## POST 新增/修改客户匹配设置

POST /api/customQuery/update

新增/修改客户匹配设置

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[CustomQueryDto](#schemacustomquerydto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RVoid](#schemarvoid)|

<a id="opIdgetCustomQueryInfo"></a>

## GET 获取客户匹配设置详细信息

GET /api/customQuery/getCustomQueryInfo

获取客户匹配设置详细信息

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RCustomSettingQueryVo](#schemarcustomsettingqueryvo)|

# 2024-前端对客接口文档/反馈咨询相关接口

<a id="opIdwxSendMsg"></a>

## POST 客户咨询

POST /api/consult/wxSendMsg

客户咨询

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[ConsultDto](#schemaconsultdto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[R](#schemar)|

<a id="opIdupdate_1"></a>

## POST 客户更新咨询状态

POST /api/consult/update

客户更新咨询状态

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[ConsultDto](#schemaconsultdto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[R](#schemar)|

<a id="opIdconsultList"></a>

## GET 咨询列表

GET /api/consult/list

咨询列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|page|query|integer(int32)| 是 |none|
|pageSize|query|integer(int32)| 是 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[R](#schemar)|

# 2024-前端对客接口文档/回复咨询结果相关接口

<a id="opIdwxSendMsg_1"></a>

## POST 客服解答客户咨询

POST /api/answer/wxSendMsg

客服解答客户咨询

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[AnswerDto](#schemaanswerdto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[R](#schemar)|

# 2024-前端对客接口文档/活动相关接口

<a id="opIdlike_1"></a>

## POST 0-取消喜欢 1-喜欢 2-拒绝喜欢

POST /api/activity/like

0-取消喜欢 1-喜欢 2-拒绝喜欢

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[ActivityChooseBaseDto](#schemaactivitychoosebasedto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RInteger](#schemarinteger)|

<a id="opIdqueryDetailById"></a>

## GET 活动详情

GET /api/activity/detail

活动详情

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|activityId|query|integer| 是 |none|

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "title": "string",
    "typeId": 0,
    "grade": 0,
    "titleImg": "string",
    "link": "string",
    "subTitle": "string",
    "maxNum": 0,
    "maxMaleNum": 0,
    "maxFemaleNum": 0,
    "address": "string",
    "detail": "string",
    "detailImg": "string",
    "beginTime": "2019-08-24T14:15:22Z",
    "endTime": "2019-08-24T14:15:22Z",
    "isSelect": 0,
    "nowNum": 0,
    "nowMaleNum": 0,
    "nowFemaleNum": 0,
    "maxChooseNum": 0,
    "briefIntroduction": "string",
    "activityCost": "string",
    "activityPrice": 0,
    "isOnline": "string",
    "activityType": 0,
    "preEnrollNum": 0,
    "activityPlatform": "string",
    "typeTitle": "string",
    "enrollStatus": 0,
    "enrollStatusName": "string",
    "payStatus": 0,
    "payStatusName": "string",
    "activityStatus": "string",
    "activityCustomInfoVoList": [
      {
        "customId": 0,
        "nickName": "string",
        "imageUrl": "string"
      }
    ]
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RActivityDetailVo](#schemaractivitydetailvo)|

<a id="opIdactivityEnroll"></a>

## POST 活动报名/取消报名

POST /api/activity/enroll

活动报名/取消报名

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[ActivityCustomDto](#schemaactivitycustomdto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RActivityEnrollVo](#schemaractivityenrollvo)|

<a id="opIdselectOppositeSexCustomList"></a>

## GET 活动嘉宾列表[异性报名成功嘉宾]

GET /api/activity/selectOppositeSexCustomList/{activityId}

活动嘉宾列表[异性报名成功嘉宾]

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|activityId|path|integer(int64)| 是 |活动id|
|pageSize|query|integer(int32)| 否 |分页大小|
|pageNum|query|integer(int32)| 否 |当前页数|
|orderByColumn|query|string| 否 |排序列|
|isAsc|query|string| 否 |排序的方向desc或者asc|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[TableDataInfoCustomBaseVo](#schematabledatainfocustombasevo)|

<a id="opIdlist_42"></a>

## GET 活动列表

GET /api/activity/list

活动列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|status|query|string| 否 |活动状态(0-未开始|1-报名中|2-报名结束，活动进行中|3-活动结束，以;分割)|
|grade|query|integer(int32)| 否 |活动等级:越大优先级越高|
|typeId|query|integer(int32)| 否 |活动类型(0代表所有活动类型,4:双保险活动)|
|pageSize|query|integer(int32)| 否 |分页大小|
|pageNum|query|integer(int32)| 否 |当前页数|
|orderByColumn|query|string| 否 |排序列|
|isAsc|query|string| 否 |排序的方向desc或者asc|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[TableDataInfoActivityBaseVo](#schematabledatainfoactivitybasevo)|

<a id="opIdlistForLike_2"></a>

## GET 活动嘉宾列表[不喜欢/喜欢/互相喜欢]

GET /api/activity/listForLike

活动嘉宾列表[不喜欢/喜欢/互相喜欢]

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|activityId|query|integer(int64)| 是 |活动id|
|loveType|query|integer(int32)| 是 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RListCustomBaseVo](#schemarlistcustombasevo)|

<a id="opIdgetCustomDetail_2"></a>

## GET 用户详情

GET /api/activity/getCustomDetail

用户详情

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|activityId|query|integer(int64)| 是 |活动id|
|customId|query|integer(int64)| 是 |参加活动用户id|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RCustomDetailVo](#schemarcustomdetailvo)|

# 2024-前端对客接口文档/社群相关接口

<a id="opIdquerySocialGroupList"></a>

## GET 获取社群相关等信息

GET /api/socialGroup/queryList

获取社群相关等信息

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RListSocialGroupTypeBaseVo](#schemarlistsocialgrouptypebasevo)|

# 2024-前端对客接口文档/我的页面相关接口

<a id="opIdgetPersonalData"></a>

## GET 获取数据统计信息

GET /api/personal/getPersonalData

获取数据统计信息

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RPersonalInfo](#schemarpersonalinfo)|

<a id="opIdclaimMembership"></a>

## POST 领取会员

POST /api/personal/claimMembership

领取会员

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[ClaimMemberShipDto](#schemaclaimmembershipdto)| 否 |none|

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "msg": "string",
  "data": true
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RBoolean](#schemarboolean)|

<a id="opIdgetCustomList"></a>

## GET 获取客户列表 typeId 1 我的收藏 2 互选成功 3 我喜欢的 4 喜欢我的

GET /api/personal/getCustomList/{typeId}

获取客户列表 typeId 1 我的收藏 2 互选成功 3 我喜欢的 4 喜欢我的

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|typeId|path|integer(int32)| 是 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RListCustomBaseVo](#schemarlistcustombasevo)|

# 2024-前端对客接口文档/系统设置信息相关接口

<a id="opIdsetting"></a>

## GET 获取应用设置等信息

GET /api/cms/setting

获取应用设置等信息

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RAppSettingVo](#schemarappsettingvo)|

# 2024-前端对客接口文档/照片管理相关接口

<a id="opIdsaveImageInfo"></a>

## POST 保存照片

POST /api/customImage/saveImageInfo

保存照片

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[ImageUploadDto](#schemaimageuploaddto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RVoid](#schemarvoid)|

<a id="opIdgetImageInfo"></a>

## POST 获取照片管理详细信息

POST /api/customImage/getImageInfo

获取照片管理详细信息

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|pageId|query|string| 是 |页面编号, 5001-个人形象照, 5002-打码照片|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[RCustomImageListVo](#schemarcustomimagelistvo)|

# 2024-前端对客接口文档/站内信相关接口

## GET 站内模板消息列表

GET /api/msg/listMsgConfigs

> 返回示例

```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "id": 0,
      "type": 0,
      "typeName": "",
      "enable": 0,
      "title": "",
      "content": "",
      "remark": ""
    }
  ]
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RListAppMsgConfigVo](#schemarlistappmsgconfigvo)|

## GET 获取玩家站内信息列表

GET /api/msg/listAppMsg

> 返回示例

```json
{
  "code": 0,
  "msg": "",
  "data": [
    {
      "senderId": 0,
      "senderName": "",
      "senderAvatarUrl": "",
      "msgList": [
        {
          "id": 0,
          "receiverId": 0,
          "senderId": 0,
          "msgType": 0,
          "readFlag": 0,
          "title": "",
          "content": "",
          "remark": "",
          "msgTypeName": ""
        }
      ]
    }
  ]
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RListAppMsgListVo](#schemarlistappmsglistvo)|

## POST 阅读指定玩家发送的信息

POST /api/msg/read

> Body 请求参数

```json
{
  "senderId": 0
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|senderId|query|integer| 否 |消息发送人ID（Long类型）|
|body|body|[AppMsgReadDto](#schemaappmsgreaddto)| 否 |none|

> 返回示例

```json
{
  "code": 0,
  "msg": "",
  "data": 0
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RInteger](#schemarinteger)|

## POST 给指定玩家发送站内信息

POST /api/msg/send

> Body 请求参数

```yaml
receiverId: 0
msgType: 0
title: ""
content: ""

```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» receiverId|body|integer| 是 |消息接收人ID（Long类型）|
|» msgType|body|integer| 否 |消息类型|
|» title|body|string| 否 |消息标题|
|» content|body|string| 否 |消息内容|

> 返回示例

```json
{
  "code": 0,
  "msg": "",
  "data": false
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RBoolean](#schemarboolean)|

## POST 删除指定玩家发送的信息

POST /api/msg/del

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|senderId|query|integer| 否 |消息发送人ID（Long类型）|

> 返回示例

```json
{
  "code": 0,
  "msg": "",
  "data": false
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RBoolean](#schemarboolean)|

# 2024-前端对客接口文档/会员相关接口

<a id="opIdgetVipList"></a>

## GET 获取所有会员类型

GET /api/vip/getVipList

获取所有会员类型

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "id": 0,
      "typeId": 0,
      "price": 0,
      "discountPrice": 0,
      "remark": "string",
      "bgColor": "string",
      "vipTypeName": "string",
      "validTimeUnit": 0,
      "validTimeUnitName": "string",
      "validTime": 0,
      "sortNum": 0,
      "vipName": "string"
    }
  ]
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RListVipVo](#schemarlistvipvo)|

# 2024-前端对客接口文档/会员管理

<a id="opIdedit_13"></a>

## PUT 修改会员管理

PUT /tata/customVip

修改会员管理

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[CustomVipBo](#schemacustomvipbo)| 否 |none|

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "msg": "string",
  "data": {}
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RVoid](#schemarvoid)|

<a id="opIdadd_13"></a>

## POST 新增会员管理

POST /tata/customVip

新增会员管理

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[CustomVipBo](#schemacustomvipbo)| 否 |none|

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "msg": "string",
  "data": {}
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RVoid](#schemarvoid)|

<a id="opIdexport_12"></a>

## POST 导出会员管理列表

POST /tata/customVip/export

导出会员管理列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|createBy|query|string| 否 |创建者|
|createTime|query|string| 否 |创建时间|
|updateBy|query|string| 否 |更新者|
|updateTime|query|string| 否 |更新时间|
|params|query|string| 否 |请求参数|
|id|query|integer| 是 |自增id|
|vipId|query|integer| 是 |会员id|
|customId|query|integer| 是 |用户id|
|price|query|number| 是 |会员价格|
|discountPrice|query|number| 是 |会员折扣价格|
|startTime|query|string| 是 |会员卡开始时间|
|endTime|query|string| 是 |会员卡结束时间|
|remark|query|string| 是 |备注|
|vipName|query|string| 否 |会员名称|

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

<a id="opIdgetInfo_13"></a>

## GET 获取会员管理详细信息

GET /tata/customVip/{id}

获取会员管理详细信息

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|id|path|integer| 是 |主键|

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "vipId": 0,
    "customId": 0,
    "price": 0,
    "discountPrice": 0,
    "startTime": "2019-08-24T14:15:22Z",
    "endTime": "2019-08-24T14:15:22Z",
    "remark": "string",
    "vipName": "string"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RCustomVipVo](#schemarcustomvipvo)|

<a id="opIdlist_16"></a>

## GET 查询会员管理列表

GET /tata/customVip/list

查询会员管理列表

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|createBy|query|string| 否 |创建者|
|createTime|query|string| 否 |创建时间|
|updateBy|query|string| 否 |更新者|
|updateTime|query|string| 否 |更新时间|
|params|query|string| 否 |请求参数|
|id|query|integer| 是 |自增id|
|vipId|query|integer| 是 |会员id|
|customId|query|integer| 是 |用户id|
|price|query|number| 是 |会员价格|
|discountPrice|query|number| 是 |会员折扣价格|
|startTime|query|string| 是 |会员卡开始时间|
|endTime|query|string| 是 |会员卡结束时间|
|remark|query|string| 是 |备注|
|vipName|query|string| 否 |会员名称|
|pageSize|query|integer| 否 |分页大小|
|pageNum|query|integer| 否 |当前页数|
|orderByColumn|query|string| 否 |排序列|
|isAsc|query|string| 否 |排序的方向desc或者asc|

> 返回示例

> 200 Response

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "vipId": 0,
      "customId": 0,
      "price": 0,
      "discountPrice": 0,
      "startTime": "2019-08-24T14:15:22Z",
      "endTime": "2019-08-24T14:15:22Z",
      "remark": "string",
      "vipName": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[TableDataInfoCustomVipVo](#schematabledatainfocustomvipvo)|

<a id="opIdremove_16"></a>

## DELETE 删除会员管理

DELETE /tata/customVip/{ids}

删除会员管理

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|ids|path|array[string]| 是 |主键串|

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "msg": "string",
  "data": {}
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RVoid](#schemarvoid)|

# 2024-前端对客接口文档/合伙人相关接口

<a id="opIdAddCustomQuery"></a>

## POST 新增/修改客户匹配设置

POST /api/admin/addCustomQuery

新增/修改客户匹配设置

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[CustomQueryDto](#schemacustomquerydto)| 否 |none|

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "msg": "string",
  "data": true
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RBoolean](#schemarboolean)|

<a id="opIdauditVerify"></a>

## POST 认证审核

POST /api/admin/auditVerify

认证审核

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[CustomVerifyAuditDto](#schemacustomverifyauditdto)| 否 |none|

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "msg": "string",
  "data": true
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RBoolean](#schemarboolean)|

<a id="opIdgetCustomQueryInfo_1"></a>

## GET 获取客户匹配设置详细信息

GET /api/admin/getCustomQueryInfo

获取客户匹配设置详细信息

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "birthDates": [
      "string"
    ],
    "pureHeights": [
      "string"
    ],
    "eduBackgrounds": [
      "string"
    ],
    "emotionalStates": [
      "string"
    ],
    "homeTown": "string",
    "verifyStatus": "string",
    "weights": [
      "string"
    ],
    "constellations": [
      "string"
    ],
    "yearIncome": "string",
    "residencePlace": "string",
    "workCity": "string",
    "workJobs": [
      "string"
    ],
    "houseStates": [
      "string"
    ],
    "carStates": [
      "string"
    ],
    "sexType": "string"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RCustomSettingQueryVo](#schemarcustomsettingqueryvo)|

<a id="opIdlist_54"></a>

## GET 全部嘉宾列表数据

GET /api/admin/list

全部嘉宾列表数据

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|keyWords|query|string| 否 |客户ID/昵称/微信号|
|pageSize|query|integer| 否 |分页大小|
|pageNum|query|integer| 否 |当前页数|
|orderByColumn|query|string| 否 |排序列|
|isAsc|query|string| 否 |排序的方向desc或者asc|

> 返回示例

> 200 Response

```json
{
  "total": 0,
  "rows": [
    {
      "customId": 0,
      "nickName": "string",
      "wxNumber": "string",
      "birthDate": "2019-08-24T14:15:22Z",
      "pureHeight": "string",
      "homeTown": "string",
      "eduBackground": "string",
      "workCity": "string",
      "workJob": "string",
      "houseState": "string",
      "futureCity": "string",
      "futurePlan": "string",
      "masterImageUrl": "string",
      "verifyStatus": 0,
      "verifyStatusName": "string",
      "residencePlace": "string",
      "permanentPlace": "string",
      "weight": "string",
      "nation": "string",
      "loveStatus": 0,
      "loveStatusName": "string",
      "chooseSource": 0,
      "chooseTime": "2019-08-24T14:15:22Z",
      "blindBox": 0,
      "sexType": "string",
      "sexTypeName": "string",
      "matchmakerRemark": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» total|integer(int64)|false|none||总记录数|
|» rows|[object]|false|none||列表数据|
|»» customId|integer(int64)|false|none||用户id|
|»» nickName|string|false|none||昵称|
|»» wxNumber|string|false|none||微信号|
|»» birthDate|string(date-time)|false|none||出生年月|
|»» pureHeight|string|false|none||身高cm|
|»» homeTown|string|false|none||家乡|
|»» eduBackground|string|false|none||学历|
|»» workCity|string|false|none||工作地|
|»» workJob|string|false|none||职业|
|»» houseState|string|false|none||房产情况|
|»» futureCity|string|false|none||未来发展城市|
|»» futurePlan|string|false|none||未来发展规划|
|»» masterImageUrl|string|false|none||主图|
|»» verifyStatus|integer(int32)|false|none||认证状态  0：未认证，1：认证|
|»» verifyStatusName|string|false|none||认证状态  0：未认证，1：认证|
|»» residencePlace|string|false|none||居住地|
|»» permanentPlace|string|false|none||户口所在地|
|»» weight|string|false|none||身高|
|»» nation|string|false|none||民族|
|»» loveStatus|integer(int32)|false|none||选择状态值 0-默认 1-喜欢 2-不喜欢 3-互相喜欢|
|»» loveStatusName|string|false|none||选择状态值 0-默认 1-喜欢 2-不喜欢 3-互相喜欢|
|»» chooseSource|integer(int32)|false|none||互选来源 0-活动互选 1-互选池互选|
|»» chooseTime|string(date-time)|false|none||互选时间|
|»» blindBox|integer(int32)|false|none||1-打码照片展示 2-正常照片展示 3-无照片展示|
|»» sexType|string|false|none||性别 1男，0女,2 未知|
|»» sexTypeName|string|false|none||性别 1男，0女,2 未知|
|»» matchmakerRemark|string|true|none||红娘=>备注|
|» code|integer(int32)|false|none||消息状态码|
|» msg|string|false|none||消息内容|

<a id="opIdgetVerifyDetail_1"></a>

## GET 认证详情: 1-实名认证 2-学历认证 3-工作认证

GET /api/admin/getVerifyDetailByCustomId

认证详情: 1-实名认证 2-学历认证 3-工作认证

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|verifyType|query|integer| 是 |1实名认证，2 学历认证 3工作认证|
|customId|query|integer| 是 |客户Id|

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "customId": 0,
    "verifyStatus": 0,
    "verifyStatusName": "string",
    "verifyImageUrl": [
      "string"
    ],
    "verifyFailReason": "string",
    "nameAuthType": 0,
    "nameAuthName": "string",
    "nameAuthCertNo": "string",
    "academicAuthType": 0,
    "academicAuthName": "string",
    "academicAuthSit": "string",
    "jobAuthType": 0,
    "jobAuthCompanyAllName": "string",
    "jobAuthCompanyName": "string"
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RCustomVerifyRespVo](#schemarcustomverifyrespvo)|

<a id="opIdgetCustomDetail_2"></a>

## GET 根据customId获取客户详细信息

GET /api/admin/getCustomDetail

根据customId获取客户详细信息

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|customId|query|integer| 是 |none|

> 返回示例

> 200 Response

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "customId": 0,
    "realName": "string",
    "phoneNumber": "string",
    "wxNumber": "string",
    "sexType": "string",
    "birthDate": "2019-08-24T14:15:22Z",
    "pureHeight": "string",
    "homeTown": "string",
    "eduBackground": "string",
    "finalSchool": "string",
    "familySituation": "string",
    "emotionalState": "string",
    "loveExperience": "string",
    "workCity": "string",
    "workJob": "string",
    "workCompany": "string",
    "yearIncome": "string",
    "houseState": "string",
    "futureCity": "string",
    "futurePlan": "string",
    "personalIntro": "string",
    "familyIntro": "string",
    "loveIntro": "string",
    "imageUrl": [
      "string"
    ],
    "verifyStatus": "string",
    "referrer": "string",
    "nickName": "string",
    "constellation": "string",
    "marryTime": "string",
    "idealRemark": "string",
    "carState": "string",
    "residencePlace": "string",
    "permanentPlace": "string",
    "weight": "string",
    "nation": "string",
    "hobby": "string",
    "memberType": "string",
    "verifyPhoneStatus": "string",
    "friendName": "string",
    "nameCertifiedStatus": 0,
    "nameCertifiedStatusName": "string",
    "eduCertifiedStatus": 0,
    "eduCertifiedStatusName": "string",
    "jobCertifiedStatus": 0,
    "jobCertifiedStatusName": "string",
    "loveStatus": 0,
    "loveStatusName": "string",
    "collectStatus": 0,
    "avatarUrl": "string",
    "brandId": 0,
    "customImageInfo": {
      "personalImageUrls": [
        "string"
      ],
      "blindImageUrls": [
        "string"
      ],
      "imageUrls": [
        "string"
      ]
    },
    "customSettingVo": {
      "id": 0,
      "customId": 0,
      "choose": 0,
      "blindBox": 0,
      "one2one": 0,
      "chooseIdentity": 0,
      "hideYearIncomeStatus": 0,
      "hideSchoolStatus": 0,
      "hidePersonalIntroStatus": 0,
      "hideLoveIntroStatus": 0,
      "hideHobbyStatus": 0,
      "hideIdealRemarkStatus": 0,
      "status": 0,
      "remark": "string",
      "testCode": "string"
    }
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|[RCustomDetailVo](#schemarcustomdetailvo)|

# 2024-前端对客接口文档/朋友引荐接口

<a id="opIdlistInviteeCustom"></a>

## POST 查询邀请我或者为我代言的朋友

POST /api/customInvite/listInviteeCustom

查询邀请我或者为我代言的朋友

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[CustomInviteDto](#schemacustominvitedto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[R](#schemar)|

<a id="opIdlistInviteCustom"></a>

## POST 查询我邀请或者代言的朋友

POST /api/customInvite/listInviteCustom

查询我邀请或者代言的朋友

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[CustomInviteDto](#schemacustominvitedto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[R](#schemar)|

<a id="opIdaddRepresentRelation"></a>

## POST 添加代言朋友

POST /api/customInvite/addRepresentRelation

添加代言朋友

> Body 请求参数

```json
""
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|[CustomInviteRelationDto](#schemacustominviterelationdto)| 否 |none|

> 返回示例

> 200 Response

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|OK|[R](#schemar)|

# app.hv68.cn/auth

## GET 欢迎

GET /miniprogram-login

> 返回示例

> 200 Response

```json
{}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

## POST openid登录

POST /miniprogram-login/login

使用微信小程序 openid 登录 directus 平台，方便内部管理员免密码快捷登录

> Body 请求参数

```json
{
  "openid": "o2dcp7bMPrm3aOOF9WVH5U2CbN-I"
}
```

### 请求参数

|名称|位置|类型|必选|说明|
|---|---|---|---|---|
|body|body|object| 否 |none|
|» openid|body|string| 是 |微信小程序的 openid|

> 返回示例

> 200 Response

```json
{
  "data": {
    "access_token": "string",
    "refresh_token": "string",
    "expires": 0
  }
}
```

### 返回结果

|状态码|状态码含义|说明|数据模型|
|---|---|---|---|
|200|[OK](https://tools.ietf.org/html/rfc7231#section-6.3.1)|none|Inline|

### 返回数据结构

状态码 **200**

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|» data|object|true|none||none|
|»» access_token|string|true|none||none|
|»» refresh_token|string|true|none||none|
|»» expires|integer|true|none||none|

# 数据模型

<h2 id="tocS_Custom">Custom</h2>

<a id="schemacustom"></a>
<a id="schema_Custom"></a>
<a id="tocScustom"></a>
<a id="tocscustom"></a>

```json
{
  "attendStatus": 0,
  "birthDate": "2019-08-24",
  "birthDateVar": "string",
  "birthDateVarPrefix": "string",
  "birthDateVarSuffix": "string",
  "carState": "string",
  "chooseLoveStatus": 0,
  "constellation": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "createUser": 0,
  "customAuthStatus": {
    "academicCertificationFailReason": "string",
    "academicCertificationSta": 0,
    "jobCertificationFailReason": "string",
    "jobCertificationSta": 0,
    "nameAuthenticationFailReason": "string",
    "nameAuthenticationSta": 0
  },
  "customAuthentication": {
    "academicCertification": "string",
    "academicCertificationFailReason": "string",
    "academicCertificationSta": 0,
    "createTime": "2019-08-24T14:15:22Z",
    "customId": 0,
    "id": 0,
    "jobCertification": "string",
    "jobCertificationFailReason": "string",
    "jobCertificationSta": 0,
    "nameAuthentication": "string",
    "nameAuthenticationFailReason": "string",
    "nameAuthenticationSta": 0,
    "updateTime": "2019-08-24T14:15:22Z"
  },
  "customId": 0,
  "customMark": {
    "createTime": "2019-08-24T14:15:22Z",
    "createUser": 0,
    "customId": 0,
    "customMarkId": 0,
    "markType": 0,
    "remark": "string",
    "showType": 0,
    "updateTime": "2019-08-24T14:15:22Z",
    "updateUser": 0
  },
  "customSetting": {
    "blindBox": 0,
    "choose": 0,
    "chooseIdentity": 0,
    "customId": 0,
    "one2one": 0,
    "status": 0
  },
  "customStatus": 0,
  "delStatus": 0,
  "eduBackground": "string",
  "eduImageUrl": "string",
  "eduImageUrlArray": [
    "string"
  ],
  "emotionalState": "string",
  "extension": "string",
  "familyIntro": "string",
  "familySituation": "string",
  "finalSchool": "string",
  "futureCity": "string",
  "hobby": "string",
  "homeTown": "string",
  "houseState": "string",
  "idealRemark": "string",
  "imageUrl": "string",
  "imageUrlArray": [
    "string"
  ],
  "isMember": 0,
  "jobImageUrl": "string",
  "loveExperience": "string",
  "loveIntro": "string",
  "markType": 0,
  "marryTime": "string",
  "modifySexType": "string",
  "nation": "string",
  "nickName": "string",
  "openid": "string",
  "permanentPlace": "string",
  "personalIntro": "string",
  "phoneNumber": "string",
  "publicSchedule": "string",
  "pureHeight": "string",
  "qualImageUrl": "string",
  "realName": "string",
  "referrer": "string",
  "regStatus": 0,
  "residencePlace": "string",
  "roundTime": "2019-08-24T14:15:22Z",
  "sexType": 0,
  "shareCode": "string",
  "status": 0,
  "updateTime": "2019-08-24T14:15:22Z",
  "updateUser": 0,
  "userType": 0,
  "weight": "string",
  "workCity": "string",
  "workCompany": "string",
  "workJob": "string",
  "wxNumber": "string",
  "yearIncome": "string"
}

```

Custom

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|attendStatus|integer(int32)|false|none||none|
|birthDate|string(date)|false|none||none|
|birthDateVar|string|false|none||none|
|birthDateVarPrefix|string|false|none||none|
|birthDateVarSuffix|string|false|none||none|
|carState|string|false|none||none|
|chooseLoveStatus|integer(int32)|false|none||none|
|constellation|string|false|none||none|
|createTime|string(date-time)|false|none||none|
|createUser|integer(int64)|false|none||none|
|customAuthStatus|[CustomAuthStatus](#schemacustomauthstatus)|false|none||none|
|customAuthentication|[CustomAuthentication](#schemacustomauthentication)|false|none||none|
|customId|integer(int64)|false|none||none|
|customMark|[CustomMark](#schemacustommark)|false|none||none|
|customSetting|[CustomSetting](#schemacustomsetting)|false|none||none|
|customStatus|integer(int32)|false|none||none|
|delStatus|integer(int32)|false|none||none|
|eduBackground|string|false|none||none|
|eduImageUrl|string|false|none||none|
|eduImageUrlArray|[string]|false|none||none|
|emotionalState|string|false|none||none|
|extension|string|false|none||none|
|familyIntro|string|false|none||none|
|familySituation|string|false|none||none|
|finalSchool|string|false|none||none|
|futureCity|string|false|none||none|
|hobby|string|false|none||none|
|homeTown|string|false|none||none|
|houseState|string|false|none||none|
|idealRemark|string|false|none||none|
|imageUrl|string|false|none||none|
|imageUrlArray|[string]|false|none||none|
|isMember|integer(int32)|false|none||none|
|jobImageUrl|string|false|none||none|
|loveExperience|string|false|none||none|
|loveIntro|string|false|none||none|
|markType|integer(int32)|false|none||none|
|marryTime|string|false|none||none|
|modifySexType|string|false|none||none|
|nation|string|false|none||none|
|nickName|string|false|none||none|
|openid|string|false|none||none|
|permanentPlace|string|false|none||none|
|personalIntro|string|false|none||none|
|phoneNumber|string|false|none||none|
|publicSchedule|string|false|none||none|
|pureHeight|string|false|none||none|
|qualImageUrl|string|false|none||none|
|realName|string|false|none||none|
|referrer|string|false|none||none|
|regStatus|integer(int32)|false|none||none|
|residencePlace|string|false|none||none|
|roundTime|string(date-time)|false|none||none|
|sexType|integer(int32)|false|none||none|
|shareCode|string|false|none||none|
|status|integer(int32)|false|none||none|
|updateTime|string(date-time)|false|none||none|
|updateUser|integer(int64)|false|none||none|
|userType|integer(int32)|false|none||none|
|weight|string|false|none||none|
|workCity|string|false|none||none|
|workCompany|string|false|none||none|
|workJob|string|false|none||none|
|wxNumber|string|false|none||none|
|yearIncome|string|false|none||none|

<h2 id="tocS_CustomAuthStatus">CustomAuthStatus</h2>

<a id="schemacustomauthstatus"></a>
<a id="schema_CustomAuthStatus"></a>
<a id="tocScustomauthstatus"></a>
<a id="tocscustomauthstatus"></a>

```json
{
  "academicCertificationFailReason": "string",
  "academicCertificationSta": 0,
  "jobCertificationFailReason": "string",
  "jobCertificationSta": 0,
  "nameAuthenticationFailReason": "string",
  "nameAuthenticationSta": 0
}

```

CustomAuthStatus

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|academicCertificationFailReason|string|false|none||none|
|academicCertificationSta|integer(int32)|false|none||none|
|jobCertificationFailReason|string|false|none||none|
|jobCertificationSta|integer(int32)|false|none||none|
|nameAuthenticationFailReason|string|false|none||none|
|nameAuthenticationSta|integer(int32)|false|none||none|

<h2 id="tocS_CustomAuthentication">CustomAuthentication</h2>

<a id="schemacustomauthentication"></a>
<a id="schema_CustomAuthentication"></a>
<a id="tocScustomauthentication"></a>
<a id="tocscustomauthentication"></a>

```json
{
  "academicCertification": "string",
  "academicCertificationFailReason": "string",
  "academicCertificationSta": 0,
  "createTime": "2019-08-24T14:15:22Z",
  "customId": 0,
  "id": 0,
  "jobCertification": "string",
  "jobCertificationFailReason": "string",
  "jobCertificationSta": 0,
  "nameAuthentication": "string",
  "nameAuthenticationFailReason": "string",
  "nameAuthenticationSta": 0,
  "updateTime": "2019-08-24T14:15:22Z"
}

```

CustomAuthentication

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|academicCertification|string|false|none||none|
|academicCertificationFailReason|string|false|none||none|
|academicCertificationSta|integer(int32)|false|none||none|
|createTime|string(date-time)|false|none||none|
|customId|integer(int64)|false|none||none|
|id|integer(int64)|false|none||none|
|jobCertification|string|false|none||none|
|jobCertificationFailReason|string|false|none||none|
|jobCertificationSta|integer(int32)|false|none||none|
|nameAuthentication|string|false|none||none|
|nameAuthenticationFailReason|string|false|none||none|
|nameAuthenticationSta|integer(int32)|false|none||none|
|updateTime|string(date-time)|false|none||none|

<h2 id="tocS_CustomMark">CustomMark</h2>

<a id="schemacustommark"></a>
<a id="schema_CustomMark"></a>
<a id="tocScustommark"></a>
<a id="tocscustommark"></a>

```json
{
  "createTime": "2019-08-24T14:15:22Z",
  "createUser": 0,
  "customId": 0,
  "customMarkId": 0,
  "markType": 0,
  "remark": "string",
  "showType": 0,
  "updateTime": "2019-08-24T14:15:22Z",
  "updateUser": 0
}

```

CustomMark

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createTime|string(date-time)|false|none||none|
|createUser|integer(int64)|false|none||none|
|customId|integer(int64)|false|none||none|
|customMarkId|integer(int64)|false|none||none|
|markType|integer(int32)|false|none||none|
|remark|string|false|none||none|
|showType|integer(int32)|false|none||none|
|updateTime|string(date-time)|false|none||none|
|updateUser|integer(int64)|false|none||none|

<h2 id="tocS_CustomSetting">CustomSetting</h2>

<a id="schemacustomsetting"></a>
<a id="schema_CustomSetting"></a>
<a id="tocScustomsetting"></a>
<a id="tocscustomsetting"></a>

```json
{
  "blindBox": 0,
  "choose": 0,
  "chooseIdentity": 0,
  "customId": 0,
  "one2one": 0,
  "status": 0
}

```

CustomSetting

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|blindBox|integer(int32)|false|none||none|
|choose|integer(int32)|false|none||none|
|chooseIdentity|integer(int32)|false|none||none|
|customId|integer(int64)|false|none||none|
|one2one|integer(int32)|false|none||none|
|status|integer(int32)|false|none||none|

<h2 id="tocS_DataBean">DataBean</h2>

<a id="schemadatabean"></a>
<a id="schema_DataBean"></a>
<a id="tocSdatabean"></a>
<a id="tocsdatabean"></a>

```json
{
  "code": "string",
  "data": {},
  "msg": "string",
  "success": true
}

```

DataBean

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|string|false|none||none|
|data|object|false|none||none|
|msg|string|false|none||none|
|success|boolean|false|none||none|

<h2 id="tocS_WxLoginRO">WxLoginRO</h2>

<a id="schemawxloginro"></a>
<a id="schema_WxLoginRO"></a>
<a id="tocSwxloginro"></a>
<a id="tocswxloginro"></a>

```json
{
  "avatarUrl": "头像",
  "jsCode": "微信返回的jscode",
  "nickName": "微信名",
  "referrer": 2291
}

```

WxLoginRO

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|avatarUrl|string|false|none||头像|
|jsCode|string|true|none||jsCode|
|nickName|string|false|none||昵称|
|referrer|string|false|none||推荐人|

<h2 id="tocS_合伙人信息">合伙人信息</h2>

<a id="schema合伙人信息"></a>
<a id="schema_合伙人信息"></a>
<a id="tocS合伙人信息"></a>
<a id="tocs合伙人信息"></a>

```json
{
  "reason": "string",
  "status": 0
}

```

合伙人信息

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|reason|string|false|none||申请加入理由,必填|
|status|integer(int32)|false|none||是否满足条件: 0 否 1 是|

<h2 id="tocS_客服回复信息">客服回复信息</h2>

<a id="schema客服回复信息"></a>
<a id="schema_客服回复信息"></a>
<a id="tocS客服回复信息"></a>
<a id="tocs客服回复信息"></a>

```json
{
  "answer": "string",
  "consultId": 0,
  "customId": 0,
  "question": "string",
  "status": 0
}

```

客服回复信息

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|answer|string|false|none||回复内容,必填|
|consultId|integer(int32)|false|none||问题编号|
|customId|integer(int32)|false|none||none|
|question|string|false|none||咨询内容,选填|
|status|integer(int32)|false|none||咨询状态: 0 未解决 1 解决|

<h2 id="tocS_用户上传照片信息">用户上传照片信息</h2>

<a id="schema用户上传照片信息"></a>
<a id="schema_用户上传照片信息"></a>
<a id="tocS用户上传照片信息"></a>
<a id="tocs用户上传照片信息"></a>

```json
{
  "blindImageUrl": "string",
  "customId": 0,
  "imageUrl": "string",
  "personalImageUrl": "string"
}

```

用户上传照片信息

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|blindImageUrl|string|false|none||盲盒图片,以,间隔|
|customId|integer(int64)|false|none||客户id,选填|
|imageUrl|string|false|none||生活照片(非盲盒照片),以,间隔|
|personalImageUrl|string|false|none||个人图像(首页照片)|

<h2 id="tocS_用户上传资质信息">用户上传资质信息</h2>

<a id="schema用户上传资质信息"></a>
<a id="schema_用户上传资质信息"></a>
<a id="tocS用户上传资质信息"></a>
<a id="tocs用户上传资质信息"></a>

```json
{
  "academicCertification": "string",
  "customId": 0,
  "jobCertification": "string",
  "nameAuthentication": "string"
}

```

用户上传资质信息

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|academicCertification|string|false|none||学历图片,以,间隔|
|customId|integer(int64)|false|none||用户id,选填|
|jobCertification|string|false|none||工作认证图片,以,间隔|
|nameAuthentication|string|false|none||实名认证图片,以,间隔|

<h2 id="tocS_用户咨询信息">用户咨询信息</h2>

<a id="schema用户咨询信息"></a>
<a id="schema_用户咨询信息"></a>
<a id="tocS用户咨询信息"></a>
<a id="tocs用户咨询信息"></a>

```json
{
  "id": 0,
  "question": "string",
  "status": 0
}

```

用户咨询信息

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int32)|false|none||问题编号,首次咨询不用携带|
|question|string|false|none||咨询内容|
|status|integer(int32)|false|none||咨询状态: 0 未解决 1 解决|

<h2 id="tocS_ChooseCustomRespVo">ChooseCustomRespVo</h2>

<a id="schemachoosecustomrespvo"></a>
<a id="schema_ChooseCustomRespVo"></a>
<a id="tocSchoosecustomrespvo"></a>
<a id="tocschoosecustomrespvo"></a>

```json
{
  "birthDate": "string",
  "chooseLoveStatus": 0,
  "customId": 2291,
  "eduBackground": "string",
  "homeTown": "string",
  "imageUrl": "string",
  "nation": "string",
  "nickName": "string",
  "pureHeight": "string",
  "residencePlace": "string",
  "sexType": 0,
  "shareCode": "string",
  "weight": "string",
  "workCity": "string",
  "workCompany": "string",
  "workJob": "string"
}

```

ChooseCustomRespVo

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|birthDate|string|false|none||出生年月|
|chooseLoveStatus|integer(int32)|false|none||互选结果 -1:自我查询，忽略状态, 0: 双方不喜欢, 1:我喜欢对方, 2：相互喜欢 3:对方喜欢我|
|customId|integer(int32)|false|none||客户id|
|eduBackground|string|false|none||学历背景|
|homeTown|string|false|none||家乡|
|imageUrl|string|false|none||照片|
|nation|string|false|none||民族|
|nickName|string|false|none||昵称|
|pureHeight|string|false|none||身高cm|
|residencePlace|string|false|none||现居住地|
|sexType|integer(int32)|false|none||性别 1男，0女|
|shareCode|string|false|none||分享码|
|weight|string|false|none||体重|
|workCity|string|false|none||工作地|
|workCompany|string|false|none||工作单位|
|workJob|string|false|none||职业|

<h2 id="tocS_CmsSettingRespVO">CmsSettingRespVO</h2>

<a id="schemacmssettingrespvo"></a>
<a id="schema_CmsSettingRespVO"></a>
<a id="tocScmssettingrespvo"></a>
<a id="tocscmssettingrespvo"></a>

```json
{
  "addPrivatePoolTitle": "string",
  "addPublicPoolTitle": "string",
  "blindBoxTitle": "string",
  "freeSingleTitle": "string",
  "freeSingleUrl": "string",
  "groupQrCode": "string",
  "noBlindBoxTitle": "string",
  "paySingleTitle": "string",
  "paySingleUrl": "string",
  "privatePoolTitle": "string",
  "publicPoolTitle": "string",
  "serviceWechatCode": "string",
  "visitorTitle": "string"
}

```

CmsSettingRespVO

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|addPrivatePoolTitle|string|false|none||addPrivatePoolTitle|
|addPublicPoolTitle|string|false|none||addPublicPoolTitle|
|blindBoxTitle|string|false|none||blindBoxTitle|
|freeSingleTitle|string|false|none||freeSingleTitle|
|freeSingleUrl|string|false|none||freeSingleUrl|
|groupQrCode|string|false|none||groupQrCode|
|noBlindBoxTitle|string|false|none||noBlindBoxTitle|
|paySingleTitle|string|false|none||paySingleTitle|
|paySingleUrl|string|false|none||paySingleUrl|
|privatePoolTitle|string|false|none||privatePoolTitle|
|publicPoolTitle|string|false|none||publicPoolTitle|
|serviceWechatCode|string|false|none||serviceWechatCode|
|visitorTitle|string|false|none||visitorTitle|

<h2 id="tocS_CustomDetailRespVo">CustomDetailRespVo</h2>

<a id="schemacustomdetailrespvo"></a>
<a id="schema_CustomDetailRespVo"></a>
<a id="tocScustomdetailrespvo"></a>
<a id="tocscustomdetailrespvo"></a>

```json
{
  "academicCertificationSta": 0,
  "birthDate": "2019-08-24",
  "carState": "string",
  "chooseLoveStatus": 0,
  "constellation": "string",
  "customId": 2291,
  "customStatus": 0,
  "eduBackground": "string",
  "emotionalState": "string",
  "familyIntro": "string",
  "familySituation": "string",
  "finalSchool": "string",
  "futureCity": "string",
  "hobby": "string",
  "homeTown": "string",
  "houseState": "string",
  "idealRemark": "string",
  "imageUrl": "string",
  "jobCertificationSta": 0,
  "loveExperience": "string",
  "loveIntro": "string",
  "marryTime": "string",
  "nameAuthenticationSta": 0,
  "nation": "string",
  "nickName": "string",
  "permanentPlace": "string",
  "personalIntro": "string",
  "pureHeight": "string",
  "residencePlace": "string",
  "sexType": 0,
  "shareCode": "string",
  "weight": "string",
  "workCity": "string",
  "workCompany": "string",
  "workJob": "string",
  "yearIncome": "string"
}

```

CustomDetailRespVo

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|academicCertificationSta|integer(int32)|false|none||学历认证状态 0-认证中|1-认证成功|2-认证失败|
|birthDate|string(date)|false|none||出生年月|
|carState|string|false|none||车辆情况|
|chooseLoveStatus|integer(int32)|false|none||互选结果 -1:自我查询，忽略状态, 0: 双方不喜欢, 1:我喜欢对方, 2：相互喜欢 3:对方喜欢我|
|constellation|string|false|none||星座|
|customId|integer(int64)|false|none||客户id|
|customStatus|integer(int32)|false|none||客户认证类型  0：非认证，1：认证，2：高级会员|
|eduBackground|string|false|none||学历|
|emotionalState|string|false|none||感情状况|
|familyIntro|string|false|none||家庭情况|
|familySituation|string|false|none||家庭情况|
|finalSchool|string|false|none||毕业学校|
|futureCity|string|false|none||未来发展城市|
|hobby|string|false|none||业余兴趣爱好|
|homeTown|string|false|none||家乡|
|houseState|string|false|none||房产情况|
|idealRemark|string|false|none||理想的他/她|
|imageUrl|string|false|none||照片|
|jobCertificationSta|integer(int32)|false|none||工作认证状态 0-认证中|1-认证成功|2-认证失败|
|loveExperience|string|false|none||情感经历|
|loveIntro|string|false|none||感情观|
|marryTime|string|false|none||none|
|nameAuthenticationSta|integer(int32)|false|none||实名认证状态 0-认证中|1-实名认证成功|2-实名认证失败|
|nation|string|false|none||民族|
|nickName|string|false|none||昵称|
|permanentPlace|string|false|none||户口所在地|
|personalIntro|string|false|none||个人介绍|
|pureHeight|string|false|none||身高cm|
|residencePlace|string|false|none||居住地|
|sexType|integer(int32)|false|none||性别 1男，0女|
|shareCode|string|false|none||分享码|
|weight|string|false|none||体重|
|workCity|string|false|none||工作地/现居地|
|workCompany|string|false|none||工作单位|
|workJob|string|false|none||职业|
|yearIncome|string|false|none||年收入万元|

<h2 id="tocS_CustomPersonRespVo">CustomPersonRespVo</h2>

<a id="schemacustompersonrespvo"></a>
<a id="schema_CustomPersonRespVo"></a>
<a id="tocScustompersonrespvo"></a>
<a id="tocscustompersonrespvo"></a>

```json
{
  "academicCertificationSta": 0,
  "birthDate": "2019-08-24",
  "carState": "string",
  "chooseLoveStatus": 0,
  "constellation": "string",
  "customId": 2291,
  "customSetting": {
    "blindBox": 0,
    "choose": 0,
    "chooseIdentity": 0,
    "customId": 0,
    "one2one": 0,
    "status": 0
  },
  "customStatus": 0,
  "eduBackground": "string",
  "emotionalState": "string",
  "familyIntro": "string",
  "familySituation": "string",
  "finalSchool": "string",
  "futureCity": "string",
  "homeTown": "string",
  "houseState": "string",
  "idealRemark": "string",
  "imageUrl": "string",
  "jobCertificationSta": 0,
  "loveExperience": "string",
  "loveIntro": "string",
  "marryTime": "string",
  "nameAuthenticationSta": 0,
  "nation": "string",
  "nickName": "string",
  "openid": "string",
  "permanentPlace": "string",
  "personalIntro": "string",
  "phoneNumber": "string",
  "pureHeight": "string",
  "residencePlace": "string",
  "sexType": 0,
  "shareCode": "string",
  "weight": "string",
  "workCity": "string",
  "workCompany": "string",
  "workJob": "string",
  "wxNumber": "string",
  "yearIncome": "string"
}

```

CustomPersonRespVo

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|academicCertificationSta|integer(int32)|false|none||学历认证状态 0-认证中|1-认证成功|2-认证失败|
|birthDate|string(date)|false|none||出生年月|
|carState|string|false|none||none|
|chooseLoveStatus|integer(int32)|false|none||互选结果 -1:自我查询，忽略状态, 0: 双方不喜欢, 1:我喜欢对方, 2：相互喜欢 3:对方喜欢我|
|constellation|string|false|none||星座|
|customId|integer(int64)|false|none||客户id|
|customSetting|[CustomSetting](#schemacustomsetting)|false|none||none|
|customStatus|integer(int32)|false|none||客户认证类型  0 认证中，1 认证成功，2 认证失败 ,3 高级会员|
|eduBackground|string|false|none||学历|
|emotionalState|string|false|none||感情状况|
|familyIntro|string|false|none||家庭情况|
|familySituation|string|false|none||家庭情况|
|finalSchool|string|false|none||毕业学校|
|futureCity|string|false|none||未来发展城市|
|homeTown|string|false|none||家乡|
|houseState|string|false|none||房产情况|
|idealRemark|string|false|none||理想的他/她|
|imageUrl|string|false|none||照片|
|jobCertificationSta|integer(int32)|false|none||工作认证状态 0-认证中|1-认证成功|2-认证失败|
|loveExperience|string|false|none||情感经历|
|loveIntro|string|false|none||感情观|
|marryTime|string|false|none||none|
|nameAuthenticationSta|integer(int32)|false|none||实名认证状态 0-认证中|1-实名认证成功|2-实名认证失败|
|nation|string|false|none||民族|
|nickName|string|false|none||昵称|
|openid|string|false|none||微信openid|
|permanentPlace|string|false|none||户口所在地|
|personalIntro|string|false|none||个人介绍|
|phoneNumber|string|false|none||手机号|
|pureHeight|string|false|none||身高cm|
|residencePlace|string|false|none||居住地|
|sexType|integer(int32)|false|none||性别 1男，0女|
|shareCode|string|false|none||分享码|
|weight|string|false|none||体重|
|workCity|string|false|none||工作地/现居地|
|workCompany|string|false|none||工作单位|
|workJob|string|false|none||职业|
|wxNumber|string|false|none||微信号|
|yearIncome|string|false|none||年收入万元|

<h2 id="tocS_CustomSettingInfoDto">CustomSettingInfoDto</h2>

<a id="schemacustomsettinginfodto"></a>
<a id="schema_CustomSettingInfoDto"></a>
<a id="tocScustomsettinginfodto"></a>
<a id="tocscustomsettinginfodto"></a>

```json
{
  "blindBox": 0,
  "choose": 0,
  "one2one": 0
}

```

CustomSettingInfoDto

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|blindBox|integer(int32)|false|none||是否拆盲盒: 1 拆盲盒 2 非拆盲盒|
|choose|integer(int32)|false|none||互选池： 0 不加互选池/隐身 1 公域互选池 2 私域互选池 3 部分隐身|
|one2one|integer(int32)|false|none||红娘1V1服务： 0 不需要 1 需要|

<h2 id="tocS_Pagination">Pagination</h2>

<a id="schemapagination"></a>
<a id="schema_Pagination"></a>
<a id="tocSpagination"></a>
<a id="tocspagination"></a>

```json
{
  "current": 0,
  "size": 0,
  "total": 0
}

```

Pagination

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|current|integer(int64)|false|none||none|
|size|integer(int64)|false|none||none|
|total|integer(int64)|false|none||none|

<h2 id="tocS_ResponseData">ResponseData</h2>

<a id="schemaresponsedata"></a>
<a id="schema_ResponseData"></a>
<a id="tocSresponsedata"></a>
<a id="tocsresponsedata"></a>

```json
{
  "code": 0,
  "data": {},
  "message": "string",
  "success": true
}

```

ResponseData

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|data|object|false|none||none|
|message|string|false|none||none|
|success|boolean|false|none||none|

<h2 id="tocS_统一响应实体类">统一响应实体类</h2>

<a id="schema统一响应实体类"></a>
<a id="schema_统一响应实体类"></a>
<a id="tocS统一响应实体类"></a>
<a id="tocs统一响应实体类"></a>

```json
{
  "code": 0,
  "data": {},
  "message": "string",
  "pagination": {
    "current": 0,
    "size": 0,
    "total": 0
  }
}

```

统一响应实体类

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|data|object|false|none||none|
|message|string|false|none||none|
|pagination|[Pagination](#schemapagination)|false|none||none|

<h2 id="tocS_统一响应实体类«long»">统一响应实体类«long»</h2>

<a id="schema统一响应实体类«long»"></a>
<a id="schema_统一响应实体类«long»"></a>
<a id="tocS统一响应实体类«long»"></a>
<a id="tocs统一响应实体类«long»"></a>

```json
{
  "code": 0,
  "data": 0,
  "message": "string",
  "pagination": {
    "current": 0,
    "size": 0,
    "total": 0
  }
}

```

统一响应实体类«long»

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|data|integer(int64)|false|none||none|
|message|string|false|none||none|
|pagination|[Pagination](#schemapagination)|false|none||none|

<h2 id="tocS_附件传输实体类">附件传输实体类</h2>

<a id="schema附件传输实体类"></a>
<a id="schema_附件传输实体类"></a>
<a id="tocS附件传输实体类"></a>
<a id="tocs附件传输实体类"></a>

```json
{
  "id": 0,
  "params": {}
}

```

附件传输实体类

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||id|
|params|object|false|none||none|

<h2 id="tocS_AuditDto">AuditDto</h2>

<a id="schemaauditdto"></a>
<a id="schema_AuditDto"></a>
<a id="tocSauditdto"></a>
<a id="tocsauditdto"></a>

```json
{
  "activityPrice": 0,
  "failureCause": "string",
  "id": 0,
  "payStatus": 0,
  "status": 0,
  "timePrice": 0
}

```

AuditDto

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|activityPrice|number|false|none||报名费设置不能为空,可为0|
|failureCause|string|false|none||none|
|id|integer(int32)|false|none||none|
|payStatus|integer(int32)|false|none||支付状态 0 待确认 1 未支付 2 已支付  3 已退款|
|status|integer(int32)|false|none||审核状态 0 未审核 1 审核中 2 审核通过 3 审核不通过|
|timePrice|number|false|none||守时金设置不能为空,可为0|

<h2 id="tocS_BindCustomReq">BindCustomReq</h2>

<a id="schemabindcustomreq"></a>
<a id="schema_BindCustomReq"></a>
<a id="tocSbindcustomreq"></a>
<a id="tocsbindcustomreq"></a>

```json
{
  "phoneNumber": "string",
  "verificationCode": "string"
}

```

BindCustomReq

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|phoneNumber|string|false|none||none|
|verificationCode|string|false|none||none|

<h2 id="tocS_RefundBaseDto">RefundBaseDto</h2>

<a id="schemarefundbasedto"></a>
<a id="schema_RefundBaseDto"></a>
<a id="tocSrefundbasedto"></a>
<a id="tocsrefundbasedto"></a>

```json
{
  "id": 0,
  "refund": 0,
  "refundRemark": "string"
}

```

RefundBaseDto

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int32)|false|none||编号|
|refund|number|false|none||退款金额|
|refundRemark|string|false|none||none|

<h2 id="tocS_活动签到">活动签到</h2>

<a id="schema活动签到"></a>
<a id="schema_活动签到"></a>
<a id="tocS活动签到"></a>
<a id="tocs活动签到"></a>

```json
{
  "activityCustomerId": 0,
  "signTime": "string"
}

```

活动签到

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|activityCustomerId|integer(int32)|false|none||活动报名信息id|
|signTime|string|false|none||活动签到时间|

<h2 id="tocS_活动互选">活动互选</h2>

<a id="schema活动互选"></a>
<a id="schema_活动互选"></a>
<a id="tocS活动互选"></a>
<a id="tocs活动互选"></a>

```json
{
  "activityId": 0
}

```

活动互选

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|activityId|integer(int64)|false|none||活动id|

<h2 id="tocS_PublicChooseQueryDto">PublicChooseQueryDto</h2>

<a id="schemapublicchoosequerydto"></a>
<a id="schema_PublicChooseQueryDto"></a>
<a id="tocSpublicchoosequerydto"></a>
<a id="tocspublicchoosequerydto"></a>

```json
{
  "page": 0,
  "pageSize": 0,
  "sexType": "string",
  "blindBox": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|page|integer(int32)|false|none||分页参数|
|pageSize|integer(int32)|false|none||每页大小|
|sexType|string(string)|false|none||性别 1男，0女,2 未知|
|blindBox|integer(int32)|false|none||盲盒/非盲盒|

<h2 id="tocS_RequestDto">RequestDto</h2>

<a id="schemarequestdto"></a>
<a id="schema_RequestDto"></a>
<a id="tocSrequestdto"></a>
<a id="tocsrequestdto"></a>

```json
{
  "openid": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|openid|string|true|none||openid|

<h2 id="tocS_ActivityCustomBaseDto">ActivityCustomBaseDto</h2>

<a id="schemaactivitycustombasedto"></a>
<a id="schema_ActivityCustomBaseDto"></a>
<a id="tocSactivitycustombasedto"></a>
<a id="tocsactivitycustombasedto"></a>

```json
{
  "activityId": 0,
  "customId": 0,
  "loverStatus": 0
}

```

报名用户业务对象Dto

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|activityId|integer(int64)|true|none||活动id|
|customId|integer(int64)|true|none||参加活动用户id|
|loverStatus|integer(int32)|true|none||none|

<h2 id="tocS_TraitQuestionTestBo">TraitQuestionTestBo</h2>

<a id="schematraitquestiontestbo"></a>
<a id="schema_TraitQuestionTestBo"></a>
<a id="tocStraitquestiontestbo"></a>
<a id="tocstraitquestiontestbo"></a>

```json
{
  "questionCode": "string",
  "answerCode": "string"
}

```

问题测试请求

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|questionCode|string|false|none||问题编号|
|answerCode|string|false|none||问题编码|

<h2 id="tocS_CustomQueryVo">CustomQueryVo</h2>

<a id="schemacustomqueryvo"></a>
<a id="schema_CustomQueryVo"></a>
<a id="tocScustomqueryvo"></a>
<a id="tocscustomqueryvo"></a>

```json
{
  "id": 0,
  "customId": 0,
  "realName": "string",
  "wxNumber": "string",
  "sexType": "string",
  "birthDate": "2019-08-24T14:15:22Z",
  "pureHeight": "string",
  "homeTown": "string",
  "eduBackground": "string",
  "finalSchool": "string",
  "familySituation": "string",
  "emotionalState": "string",
  "loveExperience": "string",
  "workCity": "string",
  "workJob": "string",
  "workCompany": "string",
  "yearIncome": "string",
  "houseState": "string",
  "futureCity": "string",
  "personalIntro": "string",
  "familyIntro": "string",
  "loveIntro": "string",
  "verifyStatus": "string",
  "nickName": "string",
  "constellation": "string",
  "marryTime": "string",
  "idealRemark": "string",
  "carState": "string",
  "publicSchedule": "string",
  "residencePlace": "string",
  "permanentPlace": "string",
  "weight": "string",
  "nation": "string",
  "hobby": "string",
  "memberType": "string",
  "verifyPhoneStatus": "string",
  "friendName": "string",
  "nameCertifiedStatus": "string",
  "eduCertifiedStatus": "string",
  "jobCertifiedStatus": "string",
  "remark": "string",
  "isDeleted": "string",
  "settingDetail": "string"
}

```

客户匹配设置视图对象 t_custom_query

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||none|
|customId|integer(int64)|false|none||用户id|
|realName|string|false|none||真实姓名|
|wxNumber|string|false|none||微信号|
|sexType|string|false|none||性别 1男，0女,2 未知|
|birthDate|string(date-time)|false|none||出生年月|
|pureHeight|string|false|none||身高cm|
|homeTown|string|false|none||家乡|
|eduBackground|string|false|none||学历|
|finalSchool|string|false|none||毕业学校|
|familySituation|string|false|none||家庭情况|
|emotionalState|string|false|none||感情状况|
|loveExperience|string|false|none||情感经历|
|workCity|string|false|none||工作地|
|workJob|string|false|none||职业|
|workCompany|string|false|none||工作单位|
|yearIncome|string|false|none||年收入万元|
|houseState|string|false|none||房产情况|
|futureCity|string|false|none||未来发展城市|
|personalIntro|string|false|none||个人介绍|
|familyIntro|string|false|none||家庭情况|
|loveIntro|string|false|none||感情观|
|verifyStatus|string|false|none||认证状态  0：未认证，1：认证|
|nickName|string|false|none||微信昵称|
|constellation|string|false|none||星座|
|marryTime|string|false|none||希望多久结婚|
|idealRemark|string|false|none||理想的他/她|
|carState|string|false|none||车辆情况|
|publicSchedule|string|false|none||推文排期|
|residencePlace|string|false|none||居住地|
|permanentPlace|string|false|none||户口所在地|
|weight|string|false|none||身高|
|nation|string|false|none||名族|
|hobby|string|false|none||兴趣爱好|
|memberType|string|false|none||0 非会员 1 VIP 2SVIP|
|verifyPhoneStatus|string|false|none||0未验证 1已验证|
|friendName|string|false|none||朋友姓名|
|nameCertifiedStatus|string|false|none||实名认证状态 0-认证中|1-认证成功|2-认证失败|
|eduCertifiedStatus|string|false|none||学历认证状态 0-认证中|1-认证成功|2-认证失败|
|jobCertifiedStatus|string|false|none||工作认证状态|
|remark|string|false|none||备注|
|isDeleted|string|false|none||已删除(0:否 1:是)|
|settingDetail|string|false|none||设置详情|

<h2 id="tocS_RCustomQueryVo">RCustomQueryVo</h2>

<a id="schemarcustomqueryvo"></a>
<a id="schema_RCustomQueryVo"></a>
<a id="tocSrcustomqueryvo"></a>
<a id="tocsrcustomqueryvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "customId": 0,
    "realName": "string",
    "wxNumber": "string",
    "sexType": "string",
    "birthDate": "2019-08-24T14:15:22Z",
    "pureHeight": "string",
    "homeTown": "string",
    "eduBackground": "string",
    "finalSchool": "string",
    "familySituation": "string",
    "emotionalState": "string",
    "loveExperience": "string",
    "workCity": "string",
    "workJob": "string",
    "workCompany": "string",
    "yearIncome": "string",
    "houseState": "string",
    "futureCity": "string",
    "personalIntro": "string",
    "familyIntro": "string",
    "loveIntro": "string",
    "verifyStatus": "string",
    "nickName": "string",
    "constellation": "string",
    "marryTime": "string",
    "idealRemark": "string",
    "carState": "string",
    "publicSchedule": "string",
    "residencePlace": "string",
    "permanentPlace": "string",
    "weight": "string",
    "nation": "string",
    "hobby": "string",
    "memberType": "string",
    "verifyPhoneStatus": "string",
    "friendName": "string",
    "nameCertifiedStatus": "string",
    "eduCertifiedStatus": "string",
    "jobCertifiedStatus": "string",
    "remark": "string",
    "isDeleted": "string",
    "settingDetail": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[CustomQueryVo](#schemacustomqueryvo)|false|none||客户匹配设置视图对象 t_custom_query|

<h2 id="tocS_OssFileVo">OssFileVo</h2>

<a id="schemaossfilevo"></a>
<a id="schema_OssFileVo"></a>
<a id="tocSossfilevo"></a>
<a id="tocsossfilevo"></a>

```json
{
  "ossId": 0,
  "url": "string",
  "fileName": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|ossId|integer(int64)|false|none||对象存储主键|
|url|string|false|none||URL地址|
|fileName|string|false|none||文件名|

<h2 id="tocS_ROssFileVo">ROssFileVo</h2>

<a id="schemarossfilevo"></a>
<a id="schema_ROssFileVo"></a>
<a id="tocSrossfilevo"></a>
<a id="tocsrossfilevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "ossId": 0,
    "url": "string",
    "fileName": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[OssFileVo](#schemaossfilevo)|false|none||none|

<h2 id="tocS_RListSocialGroupTypeVo">RListSocialGroupTypeVo</h2>

<a id="schemarlistsocialgrouptypevo"></a>
<a id="schema_RListSocialGroupTypeVo"></a>
<a id="tocSrlistsocialgrouptypevo"></a>
<a id="tocsrlistsocialgrouptypevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "id": 0,
      "typeName": "string",
      "enable": 0
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[SocialGroupTypeVo](#schemasocialgrouptypevo)]|false|none||[社群类型视图对象 t_social_group_type]|

<h2 id="tocS_WxMpConfigBo">WxMpConfigBo</h2>

<a id="schemawxmpconfigbo"></a>
<a id="schema_WxMpConfigBo"></a>
<a id="tocSwxmpconfigbo"></a>
<a id="tocswxmpconfigbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "appName": "string",
  "appId": "string",
  "secret": "string",
  "token": "string",
  "aesKey": "string",
  "phoneNumbers": "string",
  "remark": "string",
  "delFlag": "string",
  "enable": 0
}

```

【微信公众号配置】业务对象 t_wx_mp_config

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||自增id|
|appName|string(string)|true|none||应用名称|
|appId|string(string)|true|none||应用编号|
|secret|string(string)|true|none||密钥|
|token|string(string)|true|none||令牌|
|aesKey|string(string)|true|none||aes加密密钥|
|phoneNumbers|string(string)|false|none||运维人员手机号, 用逗号隔开|
|remark|string(string)|false|none||备注|
|delFlag|string(string)|false|none||逻辑删除：0 正常，1 删除|
|enable|integer(int32)|true|none||启用状态 0 启用  1 禁用|

<h2 id="tocS_RWxMpConfigVo">RWxMpConfigVo</h2>

<a id="schemarwxmpconfigvo"></a>
<a id="schema_RWxMpConfigVo"></a>
<a id="tocSrwxmpconfigvo"></a>
<a id="tocsrwxmpconfigvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "appName": "string",
    "appId": "string",
    "secret": "string",
    "token": "string",
    "aesKey": "string",
    "phoneNumbers": "string",
    "enable": 0,
    "remark": "string",
    "delFlag": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[WxMpConfigVo](#schemawxmpconfigvo)|false|none||【微信公众号配置】视图对象 t_wx_mp_config|

<h2 id="tocS_WxMpConfigVo">WxMpConfigVo</h2>

<a id="schemawxmpconfigvo"></a>
<a id="schema_WxMpConfigVo"></a>
<a id="tocSwxmpconfigvo"></a>
<a id="tocswxmpconfigvo"></a>

```json
{
  "id": 0,
  "appName": "string",
  "appId": "string",
  "secret": "string",
  "token": "string",
  "aesKey": "string",
  "phoneNumbers": "string",
  "enable": 0,
  "remark": "string",
  "delFlag": "string"
}

```

【微信公众号配置】视图对象 t_wx_mp_config

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|appName|string|false|none||应用名称|
|appId|string|false|none||应用编号|
|secret|string|false|none||密钥|
|token|string|false|none||令牌|
|aesKey|string|false|none||aes加密密钥|
|phoneNumbers|string|false|none||运维人员手机号|
|enable|integer(int32)|false|none||none|
|remark|string|false|none||备注|
|delFlag|string|false|none||逻辑删除：0 正常，1 删除|

<h2 id="tocS_TableDataInfoWxMpConfigVo">TableDataInfoWxMpConfigVo</h2>

<a id="schematabledatainfowxmpconfigvo"></a>
<a id="schema_TableDataInfoWxMpConfigVo"></a>
<a id="tocStabledatainfowxmpconfigvo"></a>
<a id="tocstabledatainfowxmpconfigvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "appName": "string",
      "appId": "string",
      "secret": "string",
      "token": "string",
      "aesKey": "string",
      "phoneNumbers": "string",
      "enable": 0,
      "remark": "string",
      "delFlag": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[WxMpConfigVo](#schemawxmpconfigvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_WxMsgTypeBo">WxMsgTypeBo</h2>

<a id="schemawxmsgtypebo"></a>
<a id="schema_WxMsgTypeBo"></a>
<a id="tocSwxmsgtypebo"></a>
<a id="tocswxmsgtypebo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "type": 0,
  "typeName": "string",
  "remark": "string",
  "delFlag": "string",
  "enable": 0
}

```

微信模板消息类型业务对象 t_wx_msg_type

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||主键id|
|type|integer(int32)|true|none||模板消息类型|
|typeName|string(string)|true|none||模板消息类型名称|
|remark|string(string)|false|none||备注|
|delFlag|string(string)|false|none||逻辑删除：0 正常，1 删除|
|enable|integer(int32)|true|none||启用状态 0 启用  1 禁用|

<h2 id="tocS_AppMsgBo">AppMsgBo</h2>

<a id="schemaappmsgbo"></a>
<a id="schema_AppMsgBo"></a>
<a id="tocSappmsgbo"></a>
<a id="tocsappmsgbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "receiverId": 0,
  "senderId": 0,
  "msgType": 0,
  "readFlag": 0,
  "title": "string",
  "content": "string",
  "delCustomIds": "string",
  "delFlag": "string",
  "remark": "string"
}

```

站内信息业务对象 t_app_msg

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||消息主键id|
|receiverId|integer(int64)|true|none||接收人id|
|senderId|integer(int64)|true|none||发送人id|
|msgType|integer(int32)|true|none||消息类型|
|readFlag|integer(int32)|false|none||阅读状态：0 未读，1 已读|
|title|string(string)|false|none||none|
|content|string(string)|true|none||none|
|delCustomIds|string(string)|false|none||删除该消息的玩家ids|
|delFlag|string(string)|false|none||逻辑删除：0 正常，1 删除|
|remark|string(string)|false|none||备注|

<h2 id="tocS_AppMsgConfigBo">AppMsgConfigBo</h2>

<a id="schemaappmsgconfigbo"></a>
<a id="schema_AppMsgConfigBo"></a>
<a id="tocSappmsgconfigbo"></a>
<a id="tocsappmsgconfigbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "type": 0,
  "typeName": "string",
  "title": "string",
  "content": "string",
  "remark": "string",
  "delFlag": "string",
  "enable": 0
}

```

站内消息配置业务对象 t_app_msg_config

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||主键id|
|type|integer(int32)|true|none||类型|
|typeName|string(string)|true|none||类型名称|
|title|string(string)|false|none||默认消息标题|
|content|string(string)|false|none||默认消息内容|
|remark|string(string)|false|none||备注|
|delFlag|string(string)|false|none||逻辑删除：0 正常，1 删除|
|enable|integer(int32)|false|none||启用状态 0 启用  1 禁用|

<h2 id="tocS_WxMsgTestBo">WxMsgTestBo</h2>

<a id="schemawxmsgtestbo"></a>
<a id="schema_WxMsgTestBo"></a>
<a id="tocSwxmsgtestbo"></a>
<a id="tocswxmsgtestbo"></a>

```json
{
  "wxMpConfigId": 0,
  "userType": 0,
  "notifyPhones": "string",
  "msgSubType": 0,
  "paramOne": "string",
  "paramTwo": "string",
  "paramThree": "string",
  "paramFour": "string",
  "paramFive": "string",
  "paramRemark": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|wxMpConfigId|integer(int64)|false|none||none|
|userType|integer(int32)|false|none||none|
|notifyPhones|string|false|none||none|
|msgSubType|integer(int32)|false|none||none|
|paramOne|string|false|none||none|
|paramTwo|string|false|none||none|
|paramThree|string|false|none||none|
|paramFour|string|false|none||none|
|paramFive|string|false|none||none|
|paramRemark|string|false|none||none|

<h2 id="tocS_AppMsgTestBo">AppMsgTestBo</h2>

<a id="schemaappmsgtestbo"></a>
<a id="schema_AppMsgTestBo"></a>
<a id="tocSappmsgtestbo"></a>
<a id="tocsappmsgtestbo"></a>

```json
{
  "receiveType": "string",
  "platformType": 0,
  "receiverPhone": "string",
  "receiverId": 0,
  "senderId": 0,
  "msgType": 0,
  "title": "string",
  "content": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|receiveType|string|false|none||none|
|platformType|integer(int32)|false|none||none|
|receiverPhone|string|false|none||none|
|receiverId|integer(int64)|false|none||none|
|senderId|integer(int64)|false|none||none|
|msgType|integer(int32)|false|none||none|
|title|string|false|none||none|
|content|string|false|none||none|

<h2 id="tocS_RWxMsgTypeVo">RWxMsgTypeVo</h2>

<a id="schemarwxmsgtypevo"></a>
<a id="schema_RWxMsgTypeVo"></a>
<a id="tocSrwxmsgtypevo"></a>
<a id="tocsrwxmsgtypevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "type": 0,
    "typeName": "string",
    "enable": 0,
    "remark": "string",
    "delFlag": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[WxMsgTypeVo](#schemawxmsgtypevo)|false|none||微信模板消息类型视图对象 t_wx_msg_type|

<h2 id="tocS_WxMsgTypeVo">WxMsgTypeVo</h2>

<a id="schemawxmsgtypevo"></a>
<a id="schema_WxMsgTypeVo"></a>
<a id="tocSwxmsgtypevo"></a>
<a id="tocswxmsgtypevo"></a>

```json
{
  "id": 0,
  "type": 0,
  "typeName": "string",
  "enable": 0,
  "remark": "string",
  "delFlag": "string"
}

```

微信模板消息类型视图对象 t_wx_msg_type

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||主键id|
|type|integer(int32)|false|none||模板消息类型|
|typeName|string|false|none||模板消息类型名称|
|enable|integer(int32)|false|none||状态，0:禁用 1:启用|
|remark|string|false|none||备注|
|delFlag|string|false|none||逻辑删除：0 正常，1 删除|

<h2 id="tocS_TableDataInfoWxMsgTypeVo">TableDataInfoWxMsgTypeVo</h2>

<a id="schematabledatainfowxmsgtypevo"></a>
<a id="schema_TableDataInfoWxMsgTypeVo"></a>
<a id="tocStabledatainfowxmsgtypevo"></a>
<a id="tocstabledatainfowxmsgtypevo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "type": 0,
      "typeName": "string",
      "enable": 0,
      "remark": "string",
      "delFlag": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[WxMsgTypeVo](#schemawxmsgtypevo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RListWxMsgTypeVo">RListWxMsgTypeVo</h2>

<a id="schemarlistwxmsgtypevo"></a>
<a id="schema_RListWxMsgTypeVo"></a>
<a id="tocSrlistwxmsgtypevo"></a>
<a id="tocsrlistwxmsgtypevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "id": 0,
      "type": 0,
      "typeName": "string",
      "enable": 0,
      "remark": "string",
      "delFlag": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[WxMsgTypeVo](#schemawxmsgtypevo)]|false|none||[微信模板消息类型视图对象 t_wx_msg_type]|

<h2 id="tocS_RListWxMpConfigVo">RListWxMpConfigVo</h2>

<a id="schemarlistwxmpconfigvo"></a>
<a id="schema_RListWxMpConfigVo"></a>
<a id="tocSrlistwxmpconfigvo"></a>
<a id="tocsrlistwxmpconfigvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "id": 0,
      "appName": "string",
      "appId": "string",
      "secret": "string",
      "token": "string",
      "aesKey": "string",
      "phoneNumbers": "string",
      "enable": 0,
      "remark": "string",
      "delFlag": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[WxMpConfigVo](#schemawxmpconfigvo)]|false|none||[【微信公众号配置】视图对象 t_wx_mp_config]|

<h2 id="tocS_AppMsgConfigVo">AppMsgConfigVo</h2>

<a id="schemaappmsgconfigvo"></a>
<a id="schema_AppMsgConfigVo"></a>
<a id="tocSappmsgconfigvo"></a>
<a id="tocsappmsgconfigvo"></a>

```json
{
  "id": 0,
  "type": 0,
  "typeName": "string",
  "enable": 0,
  "title": "string",
  "content": "string",
  "remark": "string"
}

```

站内消息配置视图对象 t_app_msg_config

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||主键id|
|type|integer(int32)|false|none||类型|
|typeName|string|false|none||类型名称|
|enable|integer(int32)|false|none||none|
|title|string|false|none||默认消息标题|
|content|string|false|none||默认消息内容|
|remark|string|false|none||备注|

<h2 id="tocS_RAppMsgConfigVo">RAppMsgConfigVo</h2>

<a id="schemarappmsgconfigvo"></a>
<a id="schema_RAppMsgConfigVo"></a>
<a id="tocSrappmsgconfigvo"></a>
<a id="tocsrappmsgconfigvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "type": 0,
    "typeName": "string",
    "enable": 0,
    "title": "string",
    "content": "string",
    "remark": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[AppMsgConfigVo](#schemaappmsgconfigvo)|false|none||站内消息配置视图对象 t_app_msg_config|

<h2 id="tocS_TableDataInfoAppMsgConfigVo">TableDataInfoAppMsgConfigVo</h2>

<a id="schematabledatainfoappmsgconfigvo"></a>
<a id="schema_TableDataInfoAppMsgConfigVo"></a>
<a id="tocStabledatainfoappmsgconfigvo"></a>
<a id="tocstabledatainfoappmsgconfigvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "type": 0,
      "typeName": "string",
      "enable": 0,
      "title": "string",
      "content": "string",
      "remark": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[AppMsgConfigVo](#schemaappmsgconfigvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RListAppMsgConfigVo">RListAppMsgConfigVo</h2>

<a id="schemarlistappmsgconfigvo"></a>
<a id="schema_RListAppMsgConfigVo"></a>
<a id="tocSrlistappmsgconfigvo"></a>
<a id="tocsrlistappmsgconfigvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "id": 0,
      "type": 0,
      "typeName": "string",
      "enable": 0,
      "title": "string",
      "content": "string",
      "remark": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[AppMsgConfigVo](#schemaappmsgconfigvo)]|false|none||[站内消息配置视图对象 t_app_msg_config]|

<h2 id="tocS_AppMsgVo">AppMsgVo</h2>

<a id="schemaappmsgvo"></a>
<a id="schema_AppMsgVo"></a>
<a id="tocSappmsgvo"></a>
<a id="tocsappmsgvo"></a>

```json
{
  "id": 0,
  "receiverId": 0,
  "senderId": 0,
  "msgType": 0,
  "readFlag": 0,
  "title": "string",
  "content": "string",
  "delCustomIds": "string",
  "remark": "string",
  "msgTypeName": "string",
  "createTime": "2019-08-24T14:15:22Z"
}

```

站内信息视图对象 t_app_msg

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||消息主键id|
|receiverId|integer(int64)|false|none||接收人id|
|senderId|integer(int64)|false|none||发送人id|
|msgType|integer(int32)|false|none||消息类型|
|readFlag|integer(int32)|false|none||阅读状态：0 未读，1 已读|
|title|string|false|none||none|
|content|string|false|none||none|
|delCustomIds|string|false|none||none|
|remark|string|false|none||备注|
|msgTypeName|string|false|none||none|
|createTime|string(date-time)|false|none||none|

<h2 id="tocS_RAppMsgVo">RAppMsgVo</h2>

<a id="schemarappmsgvo"></a>
<a id="schema_RAppMsgVo"></a>
<a id="tocSrappmsgvo"></a>
<a id="tocsrappmsgvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "receiverId": 0,
    "senderId": 0,
    "msgType": 0,
    "readFlag": 0,
    "title": "string",
    "content": "string",
    "delCustomIds": "string",
    "remark": "string",
    "msgTypeName": "string",
    "createTime": "2019-08-24T14:15:22Z"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[AppMsgVo](#schemaappmsgvo)|false|none||站内信息视图对象 t_app_msg|

<h2 id="tocS_TableDataInfoAppMsgVo">TableDataInfoAppMsgVo</h2>

<a id="schematabledatainfoappmsgvo"></a>
<a id="schema_TableDataInfoAppMsgVo"></a>
<a id="tocStabledatainfoappmsgvo"></a>
<a id="tocstabledatainfoappmsgvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "receiverId": 0,
      "senderId": 0,
      "msgType": 0,
      "readFlag": 0,
      "title": "string",
      "content": "string",
      "delCustomIds": "string",
      "remark": "string",
      "msgTypeName": "string",
      "createTime": "2019-08-24T14:15:22Z"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[AppMsgVo](#schemaappmsgvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_CustomSettingQueryVo">CustomSettingQueryVo</h2>

<a id="schemacustomsettingqueryvo"></a>
<a id="schema_CustomSettingQueryVo"></a>
<a id="tocScustomsettingqueryvo"></a>
<a id="tocscustomsettingqueryvo"></a>

```json
{
  "birthDates": [
    "string"
  ],
  "pureHeights": [
    "string"
  ],
  "eduBackgrounds": [
    "string"
  ],
  "emotionalStates": [
    "string"
  ],
  "homeTown": "string",
  "verifyStatus": "string",
  "weights": [
    "string"
  ],
  "constellations": [
    "string"
  ],
  "yearIncome": "string",
  "residencePlace": "string",
  "workCity": "string",
  "workJobs": [
    "string"
  ],
  "houseStates": [
    "string"
  ],
  "carStates": [
    "string"
  ],
  "sexType": "string"
}

```

客户匹配设置视图对象 t_custom_query

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|birthDates|[string]|false|none||出生年月范围|
|pureHeights|[string]|false|none||身高范围|
|eduBackgrounds|[string]|false|none||学历范围|
|emotionalStates|[string]|false|none||感情状况|
|homeTown|string|false|none||家乡，格式：广东省/深圳市|
|verifyStatus|string|false|none||认证情况, 1-未三重认证，2-已三重认证|
|weights|[string]|false|none||身高范围|
|constellations|[string]|false|none||星座|
|yearIncome|string|false|none||收入范围, 数据格式：30-40W|
|residencePlace|string|false|none||现居地，数据格式：广东省/深圳市/南山区|
|workCity|string|false|none||工作地，数据格式：广东省/深圳市/南山区|
|workJobs|[string]|false|none||职业（多选）|
|houseStates|[string]|false|none||深圳房产情况，1-深圳有房、2-深圳无房|
|carStates|[string]|false|none||深圳车辆情况，1-深圳有车，2-深圳无车|
|sexType|string|false|none||性别 1男，0女,2 未知|

<h2 id="tocS_RCustomSettingQueryVo">RCustomSettingQueryVo</h2>

<a id="schemarcustomsettingqueryvo"></a>
<a id="schema_RCustomSettingQueryVo"></a>
<a id="tocSrcustomsettingqueryvo"></a>
<a id="tocsrcustomsettingqueryvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "birthDates": [
      "string"
    ],
    "pureHeights": [
      "string"
    ],
    "eduBackgrounds": [
      "string"
    ],
    "emotionalStates": [
      "string"
    ],
    "homeTown": "string",
    "verifyStatus": "string",
    "weights": [
      "string"
    ],
    "constellations": [
      "string"
    ],
    "yearIncome": "string",
    "residencePlace": "string",
    "workCity": "string",
    "workJobs": [
      "string"
    ],
    "houseStates": [
      "string"
    ],
    "carStates": [
      "string"
    ],
    "sexType": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[CustomSettingQueryVo](#schemacustomsettingqueryvo)|false|none||客户匹配设置视图对象 t_custom_query|

<h2 id="tocS_LoginDto">LoginDto</h2>

<a id="schemalogindto"></a>
<a id="schema_LoginDto"></a>
<a id="tocSlogindto"></a>
<a id="tocslogindto"></a>

```json
{
  "code": "string",
  "jsCode": "string",
  "brandType": 0,
  "referrer": "string",
  "phone": "string",
  "openid": "string",
  "loginMethodCode": 0,
  "loginPlatform": 0
}

```

用户登录对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|string|true|none||快捷登录获取手机号code、手机短信验证码code|
|jsCode|string|false|none||适用于微信小程序静默登录/h5登录: 通过jsCode判断是否静默登录|
|brandType|integer(int32)|false|none||品牌类型 1=yxr 2=jxh 3=mbti|
|referrer|string|false|none||推荐人|
|phone|string|false|none||手机号|
|openid|string|false|none||openid(h5登录使用)|
|loginMethodCode|integer(int32)|true|none||登录方式 ,0=h5的openid登录 1=小程序静默登录  2=手机号短信验证码登录|
|loginPlatform|integer(int32)|true|none||登录平台 ,0 h5 1 小程序|

<h2 id="tocS_JSONObject">JSONObject</h2>

<a id="schemajsonobject"></a>
<a id="schema_JSONObject"></a>
<a id="tocSjsonobject"></a>
<a id="tocsjsonobject"></a>

```json
{
  "empty": true,
  "property1": {},
  "property2": {}
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|**additionalProperties**|object|false|none||none|
|empty|boolean|false|none||none|

<h2 id="tocS_AppResultVO">AppResultVO</h2>

<a id="schemaappresultvo"></a>
<a id="schema_AppResultVO"></a>
<a id="tocSappresultvo"></a>
<a id="tocsappresultvo"></a>

```json
{
  "appid": "string",
  "partnerId": "string",
  "prepayId": "string",
  "packageValue": "string",
  "noncestr": "string",
  "timestamp": "string",
  "sign": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|appid|string|false|none||none|
|partnerId|string|false|none||none|
|prepayId|string|false|none||none|
|packageValue|string|false|none||none|
|noncestr|string|false|none||none|
|timestamp|string|false|none||none|
|sign|string|false|none||none|

<h2 id="tocS_JsapiResultVO">JsapiResultVO</h2>

<a id="schemajsapiresultvo"></a>
<a id="schema_JsapiResultVO"></a>
<a id="tocSjsapiresultvo"></a>
<a id="tocsjsapiresultvo"></a>

```json
{
  "appId": "string",
  "timeStamp": "string",
  "nonceStr": "string",
  "packageValue": "string",
  "signType": "string",
  "paySign": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|appId|string|false|none||none|
|timeStamp|string|false|none||none|
|nonceStr|string|false|none||none|
|packageValue|string|false|none||none|
|signType|string|false|none||none|
|paySign|string|false|none||none|

<h2 id="tocS_RUnifiedPayResponseVO">RUnifiedPayResponseVO</h2>

<a id="schemarunifiedpayresponsevo"></a>
<a id="schema_RUnifiedPayResponseVO"></a>
<a id="tocSrunifiedpayresponsevo"></a>
<a id="tocsrunifiedpayresponsevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "payCode": 0,
    "redirectUrl": "string",
    "h5Url": "string",
    "codeUrl": "string",
    "jsapiResultVO": {
      "appId": "string",
      "timeStamp": "string",
      "nonceStr": "string",
      "packageValue": "string",
      "signType": "string",
      "paySign": "string"
    },
    "appResultVO": {
      "appid": "string",
      "partnerId": "string",
      "prepayId": "string",
      "packageValue": "string",
      "noncestr": "string",
      "timestamp": "string",
      "sign": "string"
    }
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[UnifiedPayResponseVO](#schemaunifiedpayresponsevo)|false|none||none|

<h2 id="tocS_UnifiedPayResponseVO">UnifiedPayResponseVO</h2>

<a id="schemaunifiedpayresponsevo"></a>
<a id="schema_UnifiedPayResponseVO"></a>
<a id="tocSunifiedpayresponsevo"></a>
<a id="tocsunifiedpayresponsevo"></a>

```json
{
  "payCode": 0,
  "redirectUrl": "string",
  "h5Url": "string",
  "codeUrl": "string",
  "jsapiResultVO": {
    "appId": "string",
    "timeStamp": "string",
    "nonceStr": "string",
    "packageValue": "string",
    "signType": "string",
    "paySign": "string"
  },
  "appResultVO": {
    "appid": "string",
    "partnerId": "string",
    "prepayId": "string",
    "packageValue": "string",
    "noncestr": "string",
    "timestamp": "string",
    "sign": "string"
  }
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|payCode|integer(int32)|false|none||支付方式  1=微信支付，2=支付宝支付|
|redirectUrl|string|false|none||支付宝跳转url|
|h5Url|string|false|none||h5跳转url|
|codeUrl|string|false|none||扫码支付跳转url|
|jsapiResultVO|[JsapiResultVO](#schemajsapiresultvo)|false|none||none|
|appResultVO|[AppResultVO](#schemaappresultvo)|false|none||none|

<h2 id="tocS_CustomVo">CustomVo</h2>

<a id="schemacustomvo"></a>
<a id="schema_CustomVo"></a>
<a id="tocScustomvo"></a>
<a id="tocscustomvo"></a>

```json
{
  "customId": 0,
  "realName": "string",
  "phoneNumber": "string",
  "wxNumber": "string",
  "sexType": "string",
  "birthDate": "2019-08-24T14:15:22Z",
  "pureHeight": "string",
  "homeTown": "string",
  "eduBackground": "string",
  "finalSchool": "string",
  "familySituation": "string",
  "emotionalState": "string",
  "loveExperience": "string",
  "workCity": "string",
  "workJob": "string",
  "workCompany": "string",
  "yearIncome": "string",
  "houseState": "string",
  "futureCity": "string",
  "futurePlan": "string",
  "personalIntro": "string",
  "familyIntro": "string",
  "loveIntro": "string",
  "imageUrl": "string",
  "openid": "string",
  "verifyStatus": 0,
  "extension": "string",
  "eduImageUrl": "string",
  "referrer": "string",
  "nickName": "string",
  "constellation": "string",
  "marryTime": "string",
  "idealRemark": "string",
  "carState": "string",
  "publicSchedule": "string",
  "shareCode": "string",
  "residencePlace": "string",
  "permanentPlace": "string",
  "userType": "string",
  "weight": "string",
  "nation": "string",
  "hobby": "string",
  "memberType": "string",
  "verifyPhoneStatus": "string",
  "friendName": "string",
  "isDeleted": "string",
  "nameCertifiedStatus": 0,
  "eduCertifiedStatus": 0,
  "jobCertifiedStatus": 0,
  "loveStatus": 0,
  "avatarUrl": "string"
}

```

客户信息视图对象 t_custom

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|customId|integer(int64)|false|none||用户id|
|realName|string|false|none||真实姓名|
|phoneNumber|string|false|none||手机号|
|wxNumber|string|false|none||微信号|
|sexType|string|false|none||性别 1男，0女,2 未知|
|birthDate|string(date-time)|false|none||出生年月|
|pureHeight|string|false|none||身高cm|
|homeTown|string|false|none||家乡|
|eduBackground|string|false|none||学历|
|finalSchool|string|false|none||毕业学校|
|familySituation|string|false|none||家庭情况|
|emotionalState|string|false|none||感情状况|
|loveExperience|string|false|none||情感经历|
|workCity|string|false|none||工作地|
|workJob|string|false|none||职业|
|workCompany|string|false|none||工作单位|
|yearIncome|string|false|none||年收入万元|
|houseState|string|false|none||房产情况|
|futureCity|string|false|none||未来发展城市|
|futurePlan|string|false|none||未来发展规划|
|personalIntro|string|false|none||个人介绍|
|familyIntro|string|false|none||家庭情况|
|loveIntro|string|false|none||感情观|
|imageUrl|string|false|none||照片|
|openid|string|false|none||微信openid|
|verifyStatus|integer(int32)|false|none||认证状态  0：未认证，1：认证|
|extension|string|false|none||扩展字段存储json大字段|
|eduImageUrl|string|false|none||学历照片|
|referrer|string|false|none||推荐人|
|nickName|string|false|none||微信昵称|
|constellation|string|false|none||星座|
|marryTime|string|false|none||希望多久结婚|
|idealRemark|string|false|none||理想的他/她|
|carState|string|false|none||车辆情况|
|publicSchedule|string|false|none||推文排期|
|shareCode|string|false|none||分享码|
|residencePlace|string|false|none||居住地|
|permanentPlace|string|false|none||户口所在地|
|userType|string|false|none||0 h5用户 1 小程序用户|
|weight|string|false|none||身高|
|nation|string|false|none||名族|
|hobby|string|false|none||兴趣爱好|
|memberType|string|false|none||0 非会员 1 VIP 2SVIP|
|verifyPhoneStatus|string|false|none||0未验证 1已验证|
|friendName|string|false|none||朋友姓名|
|isDeleted|string|false|none||已删除(0:否 1:是)|
|nameCertifiedStatus|integer(int32)|false|none||实名认证状态 0-认证中|1-认证成功|2-认证失败|
|eduCertifiedStatus|integer(int32)|false|none||学历认证状态 0-认证中|1-认证成功|2-认证失败|
|jobCertifiedStatus|integer(int32)|false|none||工作认证状态|
|loveStatus|integer(int32)|false|none||选择状态值 2:不喜欢 1:喜欢 0：默认|
|avatarUrl|string|false|none||用户图像|

<h2 id="tocS_CustomBaseInfoDto">CustomBaseInfoDto</h2>

<a id="schemacustombaseinfodto"></a>
<a id="schema_CustomBaseInfoDto"></a>
<a id="tocScustombaseinfodto"></a>
<a id="tocscustombaseinfodto"></a>

```json
{
  "openid": "string",
  "sexType": "string",
  "phoneNumber": "string",
  "weight": "string",
  "birthDate": "2019-08-24T14:15:22Z",
  "eduBackground": "string",
  "loveExperience": "string",
  "emotionalState": "string",
  "workCity": "string",
  "residencePlace": "string",
  "shareCustomId": 0,
  "platformType": 0,
  "inviteType": 0,
  "inviterCustomId": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|openid|string|true|none||none|
|sexType|string|false|none||性别 1男，0女|
|phoneNumber|string|true|none||手机号|
|weight|string|false|none||none|
|birthDate|string(date-time)|false|none||出生年月日|
|eduBackground|string|false|none||学历|
|loveExperience|string|false|none||情感经历|
|emotionalState|string|false|none||感情状况|
|workCity|string|false|none||工作所在地|
|residencePlace|string|false|none||现居地|
|shareCustomId|integer(int64)|false|none||引荐人Id|
|platformType|integer(int32)|true|none||0 h5用户 1 小程序用户|
|inviteType|integer(int32)|false|none||邀请类型, 1-邀请, 2-代言|
|inviterCustomId|integer(int64)|false|none||邀请用户编号|

<h2 id="tocS_CustomCenterBaseInfoDto">CustomCenterBaseInfoDto</h2>

<a id="schemacustomcenterbaseinfodto"></a>
<a id="schema_CustomCenterBaseInfoDto"></a>
<a id="tocScustomcenterbaseinfodto"></a>
<a id="tocscustomcenterbaseinfodto"></a>

```json
{
  "avatarUrl": "string",
  "realName": "string",
  "nickName": "string",
  "constellation": "string",
  "weight": "string",
  "nation": "string",
  "phoneNumber": "string",
  "wxNumber": "string",
  "sexType": "string",
  "birthDate": "2019-08-24T14:15:22Z",
  "pureHeight": "string",
  "homeTown": "string",
  "eduBackground": "string",
  "finalSchool": "string",
  "familySituation": "string",
  "emotionalState": "string",
  "loveExperience": "string",
  "workCity": "string",
  "workJob": "string",
  "workCompany": "string",
  "yearIncome": "string",
  "houseState": "string",
  "futureCity": "string",
  "futurePlan": "string",
  "personalIntro": "string",
  "familyIntro": "string",
  "loveIntro": "string",
  "imageUrl": "string",
  "hobby": "string",
  "idealRemark": "string",
  "residencePlace": "string",
  "permanentPlace": "string",
  "marryTime": "string",
  "carState": "string",
  "customSettingDto": {
    "id": 0,
    "customId": 0,
    "choose": 0,
    "blindBox": 0,
    "one2one": 0,
    "hideYearIncomeStatus": 0,
    "hideSchoolStatus": 0,
    "hidePersonalIntroStatus": 0,
    "hideLoveIntroStatus": 0,
    "hideHobbyStatus": 0,
    "hideIdealRemarkStatus": 0,
    "displayOnMp": 0,
    "displayOnXhs": 0,
    "displayOnMedia": 0
  }
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|avatarUrl|string|false|none||用户图像|
|realName|string|false|none||真实姓名|
|nickName|string|false|none||昵称|
|constellation|string|false|none||星座|
|weight|string|false|none||体重|
|nation|string|false|none||民族|
|phoneNumber|string|false|none||手机号|
|wxNumber|string|false|none||微信号|
|sexType|string|false|none||性别 1男，0女|
|birthDate|string(date-time)|false|none||出生年月|
|pureHeight|string|false|none||身高cm|
|homeTown|string|false|none||家乡|
|eduBackground|string|false|none||学历|
|finalSchool|string|false|none||毕业学校|
|familySituation|string|false|none||家庭情况|
|emotionalState|string|false|none||感情状况|
|loveExperience|string|false|none||情感经历|
|workCity|string|false|none||工作地|
|workJob|string|false|none||职业|
|workCompany|string|false|none||工作单位|
|yearIncome|string|false|none||年收入万元|
|houseState|string|false|none||房产情况:有/无|
|futureCity|string|false|none||未来发展城市|
|futurePlan|string|false|none||未来发展规划|
|personalIntro|string|false|none||个人兴趣爱好|
|familyIntro|string|false|none||家庭情况|
|loveIntro|string|false|none||感情观|
|imageUrl|string|false|none||个人照片,多张以逗号分隔|
|hobby|string|false|none||兴趣爱好|
|idealRemark|string|false|none||理想的他/她|
|residencePlace|string|false|none||居住地|
|permanentPlace|string|false|none||户口所在地|
|marryTime|string|false|none||结婚时间|
|carState|string|false|none||车辆情况：有/无|
|customSettingDto|[CustomSettingDto](#schemacustomsettingdto)|false|none||用户个性设置视图对象 t_custom_setting|

<h2 id="tocS_CustomVerifyDto">CustomVerifyDto</h2>

<a id="schemacustomverifydto"></a>
<a id="schema_CustomVerifyDto"></a>
<a id="tocScustomverifydto"></a>
<a id="tocscustomverifydto"></a>

```json
{
  "verifyType": 0,
  "certPhoto": [
    "string"
  ],
  "nameAuthType": 0,
  "nameAuthName": "string",
  "nameAuthCertNo": "string",
  "academicAuthType": 0,
  "academicAuthName": "string",
  "academicAuthSit": "string",
  "jobAuthType": 0,
  "jobAuthCompanyAllName": "string",
  "jobAuthCompanyName": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|verifyType|integer(int32)|true|none||1-实名认证, 2-学历认证, 3,工作认证|
|certPhoto|[string]|true|none||实名认证图片|
|nameAuthType|integer(int32)|false|none||实名认证方式，1-居民身份证，2-护照，3-社会保障卡|
|nameAuthName|string|false|none||实名认证名字|
|nameAuthCertNo|string|false|none||实名认证证件号|
|academicAuthType|integer(int32)|false|none||学历认证方式，1-学位证书，2-毕业证书，3-学信网截图|
|academicAuthName|string|false|none||学历认证学校名称|
|academicAuthSit|string|false|none||学历认证学位|
|jobAuthType|integer(int32)|false|none||工作认证方式，1-劳动合同，2-公司名片/工卡，3-社保缴费记录，4-自由职业证明|
|jobAuthCompanyAllName|string|false|none||工作认证公司全称|
|jobAuthCompanyName|string|false|none||工作认证公司简称|

<h2 id="tocS_CustomSettingDto">CustomSettingDto</h2>

<a id="schemacustomsettingdto"></a>
<a id="schema_CustomSettingDto"></a>
<a id="tocScustomsettingdto"></a>
<a id="tocscustomsettingdto"></a>

```json
{
  "id": 0,
  "customId": 0,
  "choose": 0,
  "blindBox": 0,
  "one2one": 0,
  "hideYearIncomeStatus": 0,
  "hideSchoolStatus": 0,
  "hidePersonalIntroStatus": 0,
  "hideLoveIntroStatus": 0,
  "hideHobbyStatus": 0,
  "hideIdealRemarkStatus": 0,
  "displayOnMp": 0,
  "displayOnXhs": 0,
  "displayOnMedia": 0
}

```

用户个性设置视图对象 t_custom_setting

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|customId|integer(int64)|false|none||用户id|
|choose|integer(int32)|false|none||互选池：0-不加互选池，1-公域互选池，2-私域互选池|
|blindBox|integer(int32)|false|none||是否拆盲盒：1-打码照片展示 2-正常照片展示 3-无照片展示|
|one2one|integer(int32)|false|none||红娘1v1服务:0-不需要，1-需要|
|hideYearIncomeStatus|integer(int32)|false|none||是否隐藏年收入：0 不隐藏 1 隐藏|
|hideSchoolStatus|integer(int32)|false|none||是否隐藏毕业学校 0 不隐藏 1 隐藏|
|hidePersonalIntroStatus|integer(int32)|false|none||none|
|hideLoveIntroStatus|integer(int32)|false|none||none|
|hideHobbyStatus|integer(int32)|false|none||none|
|hideIdealRemarkStatus|integer(int32)|false|none||none|
|displayOnMp|integer(int32)|false|none||是否在公众号展示：1=是 0=否|
|displayOnXhs|integer(int32)|false|none||是否在小红书展示：1=是 0=否|
|displayOnMedia|integer(int32)|false|none||是否在视频媒体展示：1=是 0=否|

<h2 id="tocS_CustomVerifyReqVo">CustomVerifyReqVo</h2>

<a id="schemacustomverifyreqvo"></a>
<a id="schema_CustomVerifyReqVo"></a>
<a id="tocScustomverifyreqvo"></a>
<a id="tocscustomverifyreqvo"></a>

```json
{
  "verifyType": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|verifyType|integer(int32)|true|none||1实名认证，2 学历认证 3工作认证|

<h2 id="tocS_CustomVerifyRespVo">CustomVerifyRespVo</h2>

<a id="schemacustomverifyrespvo"></a>
<a id="schema_CustomVerifyRespVo"></a>
<a id="tocScustomverifyrespvo"></a>
<a id="tocscustomverifyrespvo"></a>

```json
{
  "customId": 0,
  "verifyStatus": 0,
  "verifyStatusName": "string",
  "verifyImageUrl": [
    "string"
  ],
  "verifyFailReason": "string",
  "nameAuthType": 0,
  "nameAuthName": "string",
  "nameAuthCertNo": "string",
  "academicAuthType": 0,
  "academicAuthName": "string",
  "academicAuthSit": "string",
  "jobAuthType": 0,
  "jobAuthCompanyAllName": "string",
  "jobAuthCompanyName": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|customId|integer(int64)|false|none||用户id|
|verifyStatus|integer(int32)|false|none||认证状态 0-认证中|1-实名认证成功|2-实名认证失败|
|verifyStatusName|string|false|none||认证状态：In_Certification-认证中, Certification_Successful-认证成功,Certification_Failed-认证失败|
|verifyImageUrl|[string]|false|none||认证资料|
|verifyFailReason|string|false|none||认证失败原因|
|nameAuthType|integer(int32)|false|none||实名认证方式，1-居民身份证，2-护照，3-社会保障卡|
|nameAuthName|string|false|none||实名认证名字|
|nameAuthCertNo|string|false|none||实名认证证件号|
|academicAuthType|integer(int32)|false|none||学历认证方式，1-学位证书，2-毕业证书，3-学信网截图|
|academicAuthName|string|false|none||学历认证学校名称|
|academicAuthSit|string|false|none||学历认证学位|
|jobAuthType|integer(int32)|false|none||工作认证方式，1-劳动合同，2-公司名片/工卡，3-社保缴费记录，4-自由职业证明|
|jobAuthCompanyAllName|string|false|none||工作认证公司全称|
|jobAuthCompanyName|string|false|none||工作认证公司简称|

<h2 id="tocS_GenTable">GenTable</h2>

<a id="schemagentable"></a>
<a id="schema_GenTable"></a>
<a id="tocSgentable"></a>
<a id="tocsgentable"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "tableId": 0,
  "tableName": "string",
  "tableComment": "string",
  "subTableName": "string",
  "subTableFkName": "string",
  "className": "string",
  "tplCategory": "string",
  "packageName": "string",
  "moduleName": "string",
  "businessName": "string",
  "functionName": "string",
  "functionAuthor": "string",
  "genType": "string",
  "genPath": "string",
  "pkColumn": {
    "createBy": "string",
    "createTime": "2019-08-24T14:15:22Z",
    "updateBy": "string",
    "updateTime": "2019-08-24T14:15:22Z",
    "params": {
      "property1": {},
      "property2": {}
    },
    "columnId": 0,
    "tableId": 0,
    "columnName": "string",
    "columnComment": "string",
    "columnType": "string",
    "javaType": "string",
    "javaField": "string",
    "isPk": "string",
    "isIncrement": "string",
    "isRequired": "string",
    "isInsert": "string",
    "isEdit": "string",
    "isList": "string",
    "isQuery": "string",
    "queryType": "string",
    "htmlType": "string",
    "dictType": "string",
    "sort": 0,
    "list": true,
    "pk": true,
    "insert": true,
    "edit": true,
    "usableColumn": true,
    "superColumn": true,
    "required": true,
    "capJavaField": "string",
    "increment": true,
    "query": true
  },
  "subTable": {
    "createBy": "string",
    "createTime": "2019-08-24T14:15:22Z",
    "updateBy": "string",
    "updateTime": "2019-08-24T14:15:22Z",
    "params": {
      "property1": {},
      "property2": {}
    },
    "tableId": 0,
    "tableName": "string",
    "tableComment": "string",
    "subTableName": "string",
    "subTableFkName": "string",
    "className": "string",
    "tplCategory": "string",
    "packageName": "string",
    "moduleName": "string",
    "businessName": "string",
    "functionName": "string",
    "functionAuthor": "string",
    "genType": "string",
    "genPath": "string",
    "pkColumn": {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "columnId": 0,
      "tableId": 0,
      "columnName": "string",
      "columnComment": "string",
      "columnType": "string",
      "javaType": "string",
      "javaField": "string",
      "isPk": "string",
      "isIncrement": "string",
      "isRequired": "string",
      "isInsert": "string",
      "isEdit": "string",
      "isList": "string",
      "isQuery": "string",
      "queryType": "string",
      "htmlType": "string",
      "dictType": "string",
      "sort": 0,
      "list": true,
      "pk": true,
      "insert": true,
      "edit": true,
      "usableColumn": true,
      "superColumn": true,
      "required": true,
      "capJavaField": "string",
      "increment": true,
      "query": true
    },
    "subTable": {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "tableId": 0,
      "tableName": "string",
      "tableComment": "string",
      "subTableName": "string",
      "subTableFkName": "string",
      "className": "string",
      "tplCategory": "string",
      "packageName": "string",
      "moduleName": "string",
      "businessName": "string",
      "functionName": "string",
      "functionAuthor": "string",
      "genType": "string",
      "genPath": "string",
      "pkColumn": {
        "createBy": "string",
        "createTime": "2019-08-24T14:15:22Z",
        "updateBy": "string",
        "updateTime": "2019-08-24T14:15:22Z",
        "params": {
          "property1": {},
          "property2": {}
        },
        "columnId": 0,
        "tableId": 0,
        "columnName": "string",
        "columnComment": "string",
        "columnType": "string",
        "javaType": "string",
        "javaField": "string",
        "isPk": "string",
        "isIncrement": "string",
        "isRequired": "string",
        "isInsert": "string",
        "isEdit": "string",
        "isList": "string",
        "isQuery": "string",
        "queryType": "string",
        "htmlType": "string",
        "dictType": "string",
        "sort": 0,
        "list": true,
        "pk": true,
        "insert": true,
        "edit": true,
        "usableColumn": true,
        "superColumn": true,
        "required": true,
        "capJavaField": "string",
        "increment": true,
        "query": true
      },
      "subTable": {
        "createBy": "string",
        "createTime": "2019-08-24T14:15:22Z",
        "updateBy": "string",
        "updateTime": "2019-08-24T14:15:22Z",
        "params": {
          "property1": {},
          "property2": {}
        },
        "tableId": 0,
        "tableName": "string",
        "tableComment": "string",
        "subTableName": "string",
        "subTableFkName": "string",
        "className": "string",
        "tplCategory": "string",
        "packageName": "string",
        "moduleName": "string",
        "businessName": "string",
        "functionName": "string",
        "functionAuthor": "string",
        "genType": "string",
        "genPath": "string",
        "pkColumn": {
          "createBy": null,
          "createTime": null,
          "updateBy": null,
          "updateTime": null,
          "params": null,
          "columnId": null,
          "tableId": null,
          "columnName": null,
          "columnComment": null,
          "columnType": null,
          "javaType": null,
          "javaField": null,
          "isPk": null,
          "isIncrement": null,
          "isRequired": null,
          "isInsert": null,
          "isEdit": null,
          "isList": null,
          "isQuery": null,
          "queryType": null,
          "htmlType": null,
          "dictType": null,
          "sort": null,
          "list": null,
          "pk": null,
          "insert": null,
          "edit": null,
          "usableColumn": null,
          "superColumn": null,
          "required": null,
          "capJavaField": null,
          "increment": null,
          "query": null
        },
        "subTable": {
          "createBy": null,
          "createTime": null,
          "updateBy": null,
          "updateTime": null,
          "params": null,
          "tableId": null,
          "tableName": null,
          "tableComment": null,
          "subTableName": null,
          "subTableFkName": null,
          "className": null,
          "tplCategory": null,
          "packageName": null,
          "moduleName": null,
          "businessName": null,
          "functionName": null,
          "functionAuthor": null,
          "genType": null,
          "genPath": null,
          "pkColumn": null,
          "subTable": null,
          "columns": null,
          "options": null,
          "remark": null,
          "treeCode": null,
          "treeParentCode": null,
          "treeName": null,
          "menuIds": null,
          "parentMenuId": null,
          "parentMenuName": null,
          "sub": null,
          "tree": null,
          "crud": null
        },
        "columns": [
          {}
        ],
        "options": "string",
        "remark": "string",
        "treeCode": "string",
        "treeParentCode": "string",
        "treeName": "string",
        "menuIds": [
          0
        ],
        "parentMenuId": "string",
        "parentMenuName": "string",
        "sub": true,
        "tree": true,
        "crud": true
      },
      "columns": [
        {
          "createBy": "string",
          "createTime": "2019-08-24T14:15:22Z",
          "updateBy": "string",
          "updateTime": "2019-08-24T14:15:22Z",
          "params": {},
          "columnId": 0,
          "tableId": 0,
          "columnName": "string",
          "columnComment": "string",
          "columnType": "string",
          "javaType": "string",
          "javaField": "string",
          "isPk": "string",
          "isIncrement": "string",
          "isRequired": "string",
          "isInsert": "string",
          "isEdit": "string",
          "isList": "string",
          "isQuery": "string",
          "queryType": "string",
          "htmlType": "string",
          "dictType": "string",
          "sort": 0,
          "list": true,
          "pk": true,
          "insert": true,
          "edit": true,
          "usableColumn": true,
          "superColumn": true,
          "required": true,
          "capJavaField": "string",
          "increment": true,
          "query": true
        }
      ],
      "options": "string",
      "remark": "string",
      "treeCode": "string",
      "treeParentCode": "string",
      "treeName": "string",
      "menuIds": [
        0
      ],
      "parentMenuId": "string",
      "parentMenuName": "string",
      "sub": true,
      "tree": true,
      "crud": true
    },
    "columns": [
      {
        "createBy": "string",
        "createTime": "2019-08-24T14:15:22Z",
        "updateBy": "string",
        "updateTime": "2019-08-24T14:15:22Z",
        "params": {
          "property1": {},
          "property2": {}
        },
        "columnId": 0,
        "tableId": 0,
        "columnName": "string",
        "columnComment": "string",
        "columnType": "string",
        "javaType": "string",
        "javaField": "string",
        "isPk": "string",
        "isIncrement": "string",
        "isRequired": "string",
        "isInsert": "string",
        "isEdit": "string",
        "isList": "string",
        "isQuery": "string",
        "queryType": "string",
        "htmlType": "string",
        "dictType": "string",
        "sort": 0,
        "list": true,
        "pk": true,
        "insert": true,
        "edit": true,
        "usableColumn": true,
        "superColumn": true,
        "required": true,
        "capJavaField": "string",
        "increment": true,
        "query": true
      }
    ],
    "options": "string",
    "remark": "string",
    "treeCode": "string",
    "treeParentCode": "string",
    "treeName": "string",
    "menuIds": [
      0
    ],
    "parentMenuId": "string",
    "parentMenuName": "string",
    "sub": true,
    "tree": true,
    "crud": true
  },
  "columns": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "columnId": 0,
      "tableId": 0,
      "columnName": "string",
      "columnComment": "string",
      "columnType": "string",
      "javaType": "string",
      "javaField": "string",
      "isPk": "string",
      "isIncrement": "string",
      "isRequired": "string",
      "isInsert": "string",
      "isEdit": "string",
      "isList": "string",
      "isQuery": "string",
      "queryType": "string",
      "htmlType": "string",
      "dictType": "string",
      "sort": 0,
      "list": true,
      "pk": true,
      "insert": true,
      "edit": true,
      "usableColumn": true,
      "superColumn": true,
      "required": true,
      "capJavaField": "string",
      "increment": true,
      "query": true
    }
  ],
  "options": "string",
  "remark": "string",
  "treeCode": "string",
  "treeParentCode": "string",
  "treeName": "string",
  "menuIds": [
    0
  ],
  "parentMenuId": "string",
  "parentMenuName": "string",
  "sub": true,
  "tree": true,
  "crud": true
}

```

业务表 gen_table

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|tableId|integer(int64)|false|none||编号|
|tableName|string(string)|true|none||表名称|
|tableComment|string(string)|true|none||表描述|
|subTableName|string(string)|false|none||关联父表的表名|
|subTableFkName|string(string)|false|none||本表关联父表的外键名|
|className|string(string)|true|none||实体类名称(首字母大写)|
|tplCategory|string(string)|false|none||使用的模板（crud单表操作 tree树表操作 sub主子表操作）|
|packageName|string(string)|true|none||生成包路径|
|moduleName|string(string)|true|none||生成模块名|
|businessName|string(string)|true|none||生成业务名|
|functionName|string(string)|true|none||生成功能名|
|functionAuthor|string(string)|true|none||生成作者|
|genType|string(string)|false|none||生成代码方式（0zip压缩包 1自定义路径）|
|genPath|string(string)|false|none||生成路径（不填默认项目路径）|
|pkColumn|[GenTableColumn](#schemagentablecolumn)|false|none||代码生成业务字段表 gen_table_column|
|subTable|[GenTable](#schemagentable)|false|none||业务表 gen_table|
|columns|[[GenTableColumn](#schemagentablecolumn)]|false|none||表列信息|
|options|string(string)|false|none||其它生成选项|
|remark|string(string)|false|none||备注|
|treeCode|string(string)|false|none||树编码字段|
|treeParentCode|string(string)|false|none||树父编码字段|
|treeName|string(string)|false|none||树名称字段|
|menuIds|[integer]|false|none||none|
|parentMenuId|string(string)|false|none||上级菜单ID字段|
|parentMenuName|string(string)|false|none||上级菜单名称字段|
|sub|boolean(boolean)|false|none||none|
|tree|boolean(boolean)|false|none||none|
|crud|boolean(boolean)|false|none||none|

<h2 id="tocS_GenTableColumn">GenTableColumn</h2>

<a id="schemagentablecolumn"></a>
<a id="schema_GenTableColumn"></a>
<a id="tocSgentablecolumn"></a>
<a id="tocsgentablecolumn"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "columnId": 0,
  "tableId": 0,
  "columnName": "string",
  "columnComment": "string",
  "columnType": "string",
  "javaType": "string",
  "javaField": "string",
  "isPk": "string",
  "isIncrement": "string",
  "isRequired": "string",
  "isInsert": "string",
  "isEdit": "string",
  "isList": "string",
  "isQuery": "string",
  "queryType": "string",
  "htmlType": "string",
  "dictType": "string",
  "sort": 0,
  "list": true,
  "pk": true,
  "insert": true,
  "edit": true,
  "usableColumn": true,
  "superColumn": true,
  "required": true,
  "capJavaField": "string",
  "increment": true,
  "query": true
}

```

代码生成业务字段表 gen_table_column

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|columnId|integer(int64)|false|none||编号|
|tableId|integer(int64)|false|none||归属表编号|
|columnName|string|false|none||列名称|
|columnComment|string|false|none||列描述|
|columnType|string|false|none||列类型|
|javaType|string|false|none||JAVA类型|
|javaField|string|true|none||JAVA字段名|
|isPk|string|false|none||是否主键（1是）|
|isIncrement|string|false|none||是否自增（1是）|
|isRequired|string|false|none||是否必填（1是）|
|isInsert|string|false|none||是否为插入字段（1是）|
|isEdit|string|false|none||是否编辑字段（1是）|
|isList|string|false|none||是否列表字段（1是）|
|isQuery|string|false|none||是否查询字段（1是）|
|queryType|string|false|none||查询方式（EQ等于、NE不等于、GT大于、LT小于、LIKE模糊、BETWEEN范围）|
|htmlType|string|false|none||显示类型（input文本框、textarea文本域、select下拉框、checkbox复选框、radio单选框、datetime日期控件、image图片上传控件、upload文件上传控件、editor富文本控件）|
|dictType|string|false|none||字典类型|
|sort|integer(int32)|false|none||排序|
|list|boolean|false|none||none|
|pk|boolean|false|none||none|
|insert|boolean|false|none||none|
|edit|boolean|false|none||none|
|usableColumn|boolean|false|none||none|
|superColumn|boolean|false|none||none|
|required|boolean|false|none||none|
|capJavaField|string|false|none||none|
|increment|boolean|false|none||none|
|query|boolean|false|none||none|

<h2 id="tocS_RVoid">RVoid</h2>

<a id="schemarvoid"></a>
<a id="schema_RVoid"></a>
<a id="tocSrvoid"></a>
<a id="tocsrvoid"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {}
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|object|false|none||none|

<h2 id="tocS_PayWxConfigBo">PayWxConfigBo</h2>

<a id="schemapaywxconfigbo"></a>
<a id="schema_PayWxConfigBo"></a>
<a id="tocSpaywxconfigbo"></a>
<a id="tocspaywxconfigbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": "string",
  "appId": "string",
  "mchId": "string",
  "mchKey": "string",
  "privateKeyPath": "string",
  "privateCertPath": "string",
  "serialNo": "string",
  "notifyHostUrl": "string",
  "status": 0,
  "remark": "string",
  "isDelete": 0
}

```

微信支付配置业务对象 t_pay_wx_config

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|string(string)|true|none||自增id|
|appId|string(string)|true|none||应用编号|
|mchId|string(string)|true|none||商户号|
|mchKey|string(string)|true|none||密钥|
|privateKeyPath|string(string)|false|none||商户私钥路径|
|privateCertPath|string(string)|false|none||公钥路径|
|serialNo|string(string)|true|none||商户证书序列号|
|notifyHostUrl|string(string)|true|none||退款通知回调|
|status|integer(int32)|false|none||启用状态，0:禁用 1:启用|
|remark|string(string)|false|none||备注|
|isDelete|integer(int64)|false|none||逻辑删除：1 正常，0 删除|

<h2 id="tocS_CustomBo">CustomBo</h2>

<a id="schemacustombo"></a>
<a id="schema_CustomBo"></a>
<a id="tocScustombo"></a>
<a id="tocscustombo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "customId": 0,
  "realName": "string",
  "phoneNumber": "string",
  "wxNumber": "string",
  "sexType": "string",
  "birthDate": "2019-08-24T14:15:22Z",
  "pureHeight": "string",
  "homeTown": "string",
  "eduBackground": "string",
  "finalSchool": "string",
  "familySituation": "string",
  "emotionalState": "string",
  "loveExperience": "string",
  "workCity": "string",
  "workJob": "string",
  "workCompany": "string",
  "yearIncome": "string",
  "houseState": "string",
  "futureCity": "string",
  "futurePlan": "string",
  "createdBy": "string",
  "personalIntro": "string",
  "familyIntro": "string",
  "loveIntro": "string",
  "imageUrl": "string",
  "openid": "string",
  "verifyStatus": "string",
  "extension": "string",
  "eduImageUrl": "string",
  "referrer": "string",
  "nickName": "string",
  "constellation": "string",
  "marryTime": "string",
  "idealRemark": "string",
  "carState": "string",
  "publicSchedule": "string",
  "shareCode": "string",
  "residencePlace": "string",
  "permanentPlace": "string",
  "userType": "string",
  "weight": "string",
  "nation": "string",
  "hobby": "string",
  "memberType": "string",
  "verifyPhoneStatus": 0,
  "friendName": "string",
  "isDeleted": "string",
  "remark": "string",
  "nameCertifiedStatus": 0,
  "eduCertifiedStatus": 0,
  "jobCertifiedStatus": 0,
  "avatarUrl": "string"
}

```

客户信息业务对象 t_custom

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|customId|integer(int64)|true|none||用户id|
|realName|string(string)|true|none||真实姓名|
|phoneNumber|string(string)|true|none||手机号|
|wxNumber|string(string)|true|none||微信号|
|sexType|string(string)|true|none||性别 1男，0女,2 未知|
|birthDate|string(date-time)|true|none||出生年月|
|pureHeight|string(string)|true|none||身高cm|
|homeTown|string(string)|true|none||家乡|
|eduBackground|string(string)|true|none||学历|
|finalSchool|string(string)|true|none||毕业学校|
|familySituation|string(string)|true|none||家庭情况|
|emotionalState|string(string)|true|none||感情状况|
|loveExperience|string(string)|true|none||情感经历|
|workCity|string(string)|true|none||工作地|
|workJob|string(string)|true|none||职业|
|workCompany|string(string)|true|none||工作单位|
|yearIncome|string(string)|true|none||年收入万元|
|houseState|string(string)|true|none||房产情况|
|futureCity|string(string)|true|none||未来发展城市|
|futurePlan|string(string)|true|none||未来发展规划|
|createdBy|string(string)|true|none||创建人|
|personalIntro|string(string)|true|none||个人介绍|
|familyIntro|string(string)|true|none||家庭情况|
|loveIntro|string(string)|true|none||感情观|
|imageUrl|string(string)|true|none||照片|
|openid|string(string)|true|none||微信openid|
|verifyStatus|string(string)|true|none||认证状态  0：未认证，1：认证|
|extension|string(string)|false|none||扩展字段存储json大字段|
|eduImageUrl|string(string)|false|none||学历照片|
|referrer|string(string)|false|none||推荐人|
|nickName|string(string)|true|none||微信昵称|
|constellation|string(string)|false|none||星座|
|marryTime|string(string)|true|none||希望多久结婚|
|idealRemark|string(string)|true|none||理想的他/她|
|carState|string(string)|true|none||车辆情况|
|publicSchedule|string(string)|true|none||推文排期|
|shareCode|string(string)|true|none||分享码|
|residencePlace|string(string)|true|none||居住地|
|permanentPlace|string(string)|true|none||户口所在地|
|userType|string(string)|true|none||0 h5用户 1 小程序用户|
|weight|string(string)|true|none||身高|
|nation|string(string)|true|none||名族|
|hobby|string(string)|true|none||兴趣爱好|
|memberType|string(string)|true|none||0 非会员 1 VIP 2SVIP|
|verifyPhoneStatus|integer(int32)|true|none||0未验证 1已验证|
|friendName|string(string)|false|none||朋友姓名|
|isDeleted|string(string)|true|none||已删除(0:否 1:是)|
|remark|string(string)|false|none||备注|
|nameCertifiedStatus|integer(int32)|true|none||实名认证状态 0-认证中|1-认证成功|2-认证失败|
|eduCertifiedStatus|integer(int32)|true|none||学历认证状态 0-认证中|1-认证成功|2-认证失败|
|jobCertifiedStatus|integer(int32)|true|none||工作认证状态|
|avatarUrl|string(string)|false|none||用户图像|

<h2 id="tocS_CustomImageBo">CustomImageBo</h2>

<a id="schemacustomimagebo"></a>
<a id="schema_CustomImageBo"></a>
<a id="tocScustomimagebo"></a>
<a id="tocscustomimagebo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "imageId": 0,
  "customId": 0,
  "personalImageUrl": "string",
  "blindImageUrl": "string",
  "imageUrl": "string",
  "remark": "string"
}

```

照片管理业务对象 t_custom_image

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|imageId|integer(int64)|true|none||自增id|
|customId|integer(int64)|true|none||关联客户id|
|personalImageUrl|string(string)|true|none||个人资料照片|
|blindImageUrl|string(string)|true|none||盲盒照片|
|imageUrl|string(string)|true|none||非盲盒照片|
|remark|string(string)|false|none||备注|

<h2 id="tocS_CustomAuthencationBo">CustomAuthencationBo</h2>

<a id="schemacustomauthencationbo"></a>
<a id="schema_CustomAuthencationBo"></a>
<a id="tocScustomauthencationbo"></a>
<a id="tocscustomauthencationbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "customId": 0,
  "nameAuthenticationSta": 0,
  "nameAuthenticationFailReason": "string",
  "academicCertificationSta": 0,
  "academicCertificationFailReason": "string",
  "jobCertificationSta": 0,
  "jobCertificationFailReason": "string",
  "nameAuthentication": "string",
  "academicCertification": "string",
  "jobCertification": "string",
  "nameAuthType": 0,
  "nameAuthName": "string",
  "nameAuthCertNo": "string",
  "academicAuthType": 0,
  "academicAuthName": "string",
  "academicAuthSit": "string",
  "jobAuthType": 0,
  "jobAuthCompanyAllName": "string",
  "jobAuthCompanyName": "string"
}

```

客户认证资料业务对象 t_custom_authencation

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||自增id|
|customId|integer(int64)|true|none||客户id|
|nameAuthenticationSta|integer(int32)|true|none||实名认证状态 0-认证中|1-认证成功|2-认证失败|
|nameAuthenticationFailReason|string(string)|false|none||实名认证失败原因|
|academicCertificationSta|integer(int32)|true|none||学历认证状态 0-认证中|1-认证成功|2-认证失败|
|academicCertificationFailReason|string(string)|false|none||学历认证失败原因|
|jobCertificationSta|integer(int32)|true|none||工作认证状态|
|jobCertificationFailReason|string(string)|false|none||工作认证失败原因|
|nameAuthentication|string(string)|false|none||实名认证图片分号分隔|
|academicCertification|string(string)|false|none||学历图片，分号分隔|
|jobCertification|string(string)|false|none||工作图片，分号分隔|
|nameAuthType|integer(int32)|false|none||实名认证方式，1-居民身份证，2-护照，3-社会保障卡|
|nameAuthName|string(string)|false|none||实名认证名字|
|nameAuthCertNo|string(string)|false|none||实名认证证件号|
|academicAuthType|integer(int32)|false|none||学历认证方式，1-学位证书，2-毕业证书，3-学信网截图|
|academicAuthName|string(string)|false|none||学历认证学校名称|
|academicAuthSit|string(string)|false|none||学历认证学位|
|jobAuthType|integer(int32)|false|none||工作认证方式，1-劳动合同，2-公司名片/工卡，3-社保缴费记录，4-自由职业证明|
|jobAuthCompanyAllName|string(string)|false|none||工作认证公司全称|
|jobAuthCompanyName|string(string)|false|none||工作认证公司简称|

<h2 id="tocS_AppSettingBo">AppSettingBo</h2>

<a id="schemaappsettingbo"></a>
<a id="schema_AppSettingBo"></a>
<a id="tocSappsettingbo"></a>
<a id="tocsappsettingbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "settingId": 0,
  "serviceFace": "string",
  "serviceQrCode": "string",
  "serviceWechatCode": "string",
  "groupQrCode": "string",
  "freeSingleUrl": "string",
  "paySingleUrl": "string",
  "publicPoolTitle": "string",
  "privatePoolTitle": "string",
  "freeSingleTitle": "string",
  "paySingleTitle": "string",
  "blindBoxTitle": "string",
  "noBlindBoxTitle": "string",
  "addPrivatePoolTitle": "string",
  "addPublicPoolTitle": "string",
  "visitorTitle": "string",
  "remark": "string",
  "isDeleted": "string"
}

```

app设置业务对象 t_app_setting

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|settingId|integer(int64)|true|none||自增id|
|serviceFace|string(string)|true|none||管理员账号头像|
|serviceQrCode|string(string)|true|none||客服微信二维码|
|serviceWechatCode|string(string)|true|none||客服微信号|
|groupQrCode|string(string)|true|none||群微信二维码|
|freeSingleUrl|string(string)|true|none||免费脱单url|
|paySingleUrl|string(string)|true|none||付费脱单url|
|publicPoolTitle|string(string)|true|none||公域互选池标题|
|privatePoolTitle|string(string)|true|none||私域互选池标题|
|freeSingleTitle|string(string)|true|none||免费脱单标题|
|paySingleTitle|string(string)|true|none||付费脱单标题|
|blindBoxTitle|string(string)|true|none||盲盒标题|
|noBlindBoxTitle|string(string)|true|none||非盲盒标题|
|addPrivatePoolTitle|string(string)|true|none||增加私域标题|
|addPublicPoolTitle|string(string)|true|none||增加公域标题|
|visitorTitle|string(string)|true|none||访问标题|
|remark|string(string)|false|none||备注|
|isDeleted|string(string)|false|none||已删除(0:否 1:是)|

<h2 id="tocS_ActivityBo">ActivityBo</h2>

<a id="schemaactivitybo"></a>
<a id="schema_ActivityBo"></a>
<a id="tocSactivitybo"></a>
<a id="tocsactivitybo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "title": "string",
  "typeId": 0,
  "grade": 0,
  "titleImg": "string",
  "link": "string",
  "subTitle": "string",
  "maxNum": 0,
  "maxMaleNum": 0,
  "maxFemaleNum": 0,
  "address": "string",
  "detail": "string",
  "detailImg": "string",
  "beginTime": "2019-08-24T14:15:22Z",
  "endTime": "2019-08-24T14:15:22Z",
  "status": "string",
  "isSelect": "string",
  "nowNum": 0,
  "nowMaleNum": 0,
  "nowFemaleNum": 0,
  "maxChooseNum": 0,
  "briefIntroduction": "string",
  "activityCost": "string",
  "activityPrice": 0,
  "isOnline": "string",
  "activityType": "string",
  "preEnrollNum": 0,
  "activityPlatform": "string",
  "isDeleted": "string",
  "remark": "string"
}

```

活动列表业务对象 t_activity

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||自增id|
|title|string(string)|true|none||活动名称|
|typeId|integer(int64)|true|none||活动类型id|
|grade|integer(int32)|true|none||活动等级，数字越大优先级越高，普通活动为0|
|titleImg|string(string)|true|none||活动封面图片|
|link|string(string)|false|none||对应公众号链接|
|subTitle|string(string)|false|none||副标题|
|maxNum|integer(int64)|false|none||活动最大人数,如果为0则无限大|
|maxMaleNum|integer(int64)|false|none||男生最大人数（不设置则不限制 ）|
|maxFemaleNum|integer(int64)|false|none||女生最大人数（不设置则不限制 ）|
|address|string(string)|false|none||活动地址|
|detail|string(string)|false|none||活动详情|
|detailImg|string(string)|false|none||活动详情图片url|
|beginTime|string(date-time)|false|none||活动开始时间-年月日时分秒|
|endTime|string(date-time)|false|none||活动开始时间-年月日时分秒|
|status|string(string)|true|none||活动状态：0-未开始|1-报名中|2-报名结束，活动进行中|3-活动结束|
|isSelect|string(string)|true|none||是否开启互选 0-未开启|1-开启|2-互选结束|
|nowNum|integer(int64)|true|none||目前报名活动人数|
|nowMaleNum|integer(int64)|true|none||目前报名男生人数|
|nowFemaleNum|integer(int64)|true|none||目前报名女生人数|
|maxChooseNum|integer(int64)|true|none||个人互选上限|
|briefIntroduction|string(string)|true|none||活动简介|
|activityCost|string(string)|true|none||活动费用介绍|
|activityPrice|number(number)|true|none||活动费用|
|isOnline|string(string)|true|none||0:上线 1 下线|
|activityType|string(string)|true|none||0 非公益 1公益|
|preEnrollNum|integer(int64)|true|none||预报名人数|
|activityPlatform|string(string)|true|none||0 所有平台 1 h5 2 小程序|
|isDeleted|string(string)|false|none||是否刪除(0:否 1:是)|
|remark|string(string)|false|none||备注|

<h2 id="tocS_ActivityTypeBo">ActivityTypeBo</h2>

<a id="schemaactivitytypebo"></a>
<a id="schema_ActivityTypeBo"></a>
<a id="tocSactivitytypebo"></a>
<a id="tocsactivitytypebo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "title": "string",
  "sort": 0,
  "isDeleted": "string",
  "remark": "string"
}

```

活动类型业务对象 t_activity_type

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||活动类型标题|
|title|string(string)|true|none||none|
|sort|integer(int64)|true|none||活动类型排序|
|isDeleted|string(string)|true|none||是否删除(0:否1:是)|
|remark|string(string)|true|none||备注|

<h2 id="tocS_ActivityTemplateBo">ActivityTemplateBo</h2>

<a id="schemaactivitytemplatebo"></a>
<a id="schema_ActivityTemplateBo"></a>
<a id="tocSactivitytemplatebo"></a>
<a id="tocsactivitytemplatebo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "title": "string",
  "typeId": 0,
  "grade": "string",
  "titleImg": "string",
  "link": "string",
  "subTitle": "string",
  "maxNum": 0,
  "maxMaleNum": 0,
  "maxFemaleNum": 0,
  "address": "string",
  "detail": "string",
  "detailImg": "string",
  "beginTime": "2019-08-24T14:15:22Z",
  "endTime": "2019-08-24T14:15:22Z",
  "status": "string",
  "isSelect": "string",
  "nowNum": 0,
  "nowMaleNum": 0,
  "nowFemaleNum": 0,
  "maxChooseNum": 0,
  "briefIntroduction": "string",
  "activityCost": "string",
  "activityPrice": 0,
  "isOnline": "string",
  "activityType": "string",
  "preEnrollNum": 0,
  "activityPlatform": "string",
  "isDeleted": "string",
  "remark": "string"
}

```

活动模板业务对象 t_activity_template

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||模板id|
|title|string(string)|true|none||活动名称|
|typeId|integer(int64)|true|none||活动类型id|
|grade|string(string)|true|none||活动等级，数字越大优先级越高，普通活动为0|
|titleImg|string(string)|true|none||活动封面图片|
|link|string(string)|true|none||对应公众号链接|
|subTitle|string(string)|true|none||副标题|
|maxNum|integer(int64)|true|none||活动最大人数,如果为0则无限大|
|maxMaleNum|integer(int64)|true|none||男生最大人数（不设置则不限制 ）|
|maxFemaleNum|integer(int64)|true|none||女生最大人数（不设置则不限制 ）|
|address|string(string)|true|none||活动地址|
|detail|string(string)|true|none||活动详情|
|detailImg|string(string)|true|none||活动详情图片url|
|beginTime|string(date-time)|true|none||活动开始时间-年月日时分秒|
|endTime|string(date-time)|true|none||活动开始时间-年月日时分秒|
|status|string(string)|true|none||活动状态：0-未开始|1-报名中|2-报名结束，活动进行中|3-活动结束|
|isSelect|string(string)|true|none||是否开启互选 0-未开启|1-开启|2-互选结束|
|nowNum|integer(int64)|true|none||目前报名活动人数|
|nowMaleNum|integer(int64)|true|none||目前报名男生人数|
|nowFemaleNum|integer(int64)|true|none||目前报名女生人数|
|maxChooseNum|integer(int64)|true|none||个人互选上限|
|briefIntroduction|string(string)|true|none||活动简介|
|activityCost|string(string)|true|none||活动费用介绍|
|activityPrice|number(number)|true|none||活动费用|
|isOnline|string(string)|true|none||0:上线 1 下线|
|activityType|string(string)|true|none||0 非公益 1公益|
|preEnrollNum|integer(int64)|true|none||预报名人数|
|activityPlatform|string(string)|true|none||0 所有平台 1 h5 2 小程序|
|isDeleted|string(string)|false|none||是否刪除(0:否 1:是)|
|remark|string(string)|false|none||备注|

<h2 id="tocS_ActivityCustomBo">ActivityCustomBo</h2>

<a id="schemaactivitycustombo"></a>
<a id="schema_ActivityCustomBo"></a>
<a id="tocSactivitycustombo"></a>
<a id="tocsactivitycustombo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "activityId": 0,
  "customId": 0,
  "status": "string",
  "register": "string",
  "introducesId": 0,
  "activityPrice": 0,
  "timePrice": 0,
  "signStatus": "string",
  "signTime": "2019-08-24T14:15:22Z",
  "orderNo": "string",
  "isDeleted": "string",
  "remark": "string",
  "sexType": 0
}

```

报名用户业务对象 t_activity_custom

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|false|none||自增id|
|activityId|integer(int64)|true|none||活动id|
|customId|integer(int64)|true|none||参加活动用户id|
|status|string(string)|true|none||审核状态，0-未审核|1-审核中|2-审核通过|3-审核不通过|
|register|string(string)|true|none||0-未报名|1-报名中 |2- 取消报名|3- 报名成功|
|introducesId|integer(int64)|false|none||活动推荐人id|
|activityPrice|number(number)|true|none||活动价格|
|timePrice|number(number)|true|none||守时价格|
|signStatus|string(string)|true|none||是否签到（0未签到，1已签到）|
|signTime|string(date-time)|true|none||签到时间|
|orderNo|string(string)|true|none||报名订单号|
|isDeleted|string(string)|true|none||是否刪除(0:否 1:是)|
|remark|string(string)|true|none||备注|
|sexType|integer(int32)|false|none||性别 0-男 1-女 2-未知|

<h2 id="tocS_SysDept">SysDept</h2>

<a id="schemasysdept"></a>
<a id="schema_SysDept"></a>
<a id="tocSsysdept"></a>
<a id="tocssysdept"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "parentName": "string",
  "parentId": 0,
  "children": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "parentName": "string",
      "parentId": 0,
      "children": [
        {
          "createBy": "string",
          "createTime": "2019-08-24T14:15:22Z",
          "updateBy": "string",
          "updateTime": "2019-08-24T14:15:22Z",
          "params": {
            "property1": {},
            "property2": {}
          },
          "parentName": "string",
          "parentId": 0,
          "children": [
            {}
          ],
          "deptId": 0,
          "deptName": "string",
          "orderNum": 0,
          "leader": "string",
          "phone": "string",
          "email": "string",
          "status": "string",
          "delFlag": "string",
          "ancestors": "string"
        }
      ],
      "deptId": 0,
      "deptName": "string",
      "orderNum": 0,
      "leader": "string",
      "phone": "string",
      "email": "string",
      "status": "string",
      "delFlag": "string",
      "ancestors": "string"
    }
  ],
  "deptId": 0,
  "deptName": "string",
  "orderNum": 0,
  "leader": "string",
  "phone": "string",
  "email": "string",
  "status": "string",
  "delFlag": "string",
  "ancestors": "string"
}

```

部门表 sys_dept

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|parentName|string(string)|false|none||父菜单名称|
|parentId|integer(int64)|false|none||父菜单ID|
|children|[[SysDept](#schemasysdept)]|false|none||子部门|
|deptId|integer(int64)|false|none||部门ID|
|deptName|string(string)|true|none||部门名称|
|orderNum|integer(int32)|true|none||显示顺序|
|leader|string(string)|false|none||负责人|
|phone|string(string)|false|none||联系电话|
|email|string(string)|false|none||邮箱|
|status|string(string)|false|none||部门状态:0正常,1停用|
|delFlag|string(string)|false|none||删除标志（0代表存在 2代表删除）|
|ancestors|string(string)|false|none||祖级列表|

<h2 id="tocS_SysRole">SysRole</h2>

<a id="schemasysrole"></a>
<a id="schema_SysRole"></a>
<a id="tocSsysrole"></a>
<a id="tocssysrole"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "roleId": 0,
  "roleName": "string",
  "roleKey": "string",
  "roleSort": 0,
  "dataScope": "string",
  "menuCheckStrictly": true,
  "deptCheckStrictly": true,
  "status": "string",
  "delFlag": "string",
  "remark": "string",
  "flag": true,
  "menuIds": [
    0
  ],
  "deptIds": [
    0
  ],
  "admin": true
}

```

角色表 sys_role

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|roleId|integer(int64)|false|none||角色ID|
|roleName|string(string)|true|none||角色名称|
|roleKey|string(string)|true|none||角色权限|
|roleSort|integer(int32)|true|none||角色排序|
|dataScope|string(string)|false|none||数据范围（1：所有数据权限；2：自定义数据权限；3：本部门数据权限；4：本部门及以下数据权限；5：仅本人数据权限）|
|menuCheckStrictly|boolean(boolean)|false|none||菜单树选择项是否关联显示（ 0：父子不互相关联显示 1：父子互相关联显示）|
|deptCheckStrictly|boolean(boolean)|false|none||部门树选择项是否关联显示（0：父子不互相关联显示 1：父子互相关联显示 ）|
|status|string(string)|false|none||角色状态（0正常 1停用）|
|delFlag|string(string)|false|none||删除标志（0代表存在 2代表删除）|
|remark|string(string)|false|none||备注|
|flag|boolean(boolean)|false|none||用户是否存在此角色标识 默认不存在|
|menuIds|[integer]|false|none||菜单组|
|deptIds|[integer]|false|none||部门组（数据权限）|
|admin|boolean(boolean)|false|none||none|

<h2 id="tocS_SysUser">SysUser</h2>

<a id="schemasysuser"></a>
<a id="schema_SysUser"></a>
<a id="tocSsysuser"></a>
<a id="tocssysuser"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "userId": 0,
  "deptId": 0,
  "userName": "string",
  "nickName": "string",
  "userType": "string",
  "email": "string",
  "phonenumber": "string",
  "sex": "string",
  "avatar": "string",
  "password": "string",
  "status": "string",
  "delFlag": "string",
  "loginIp": "string",
  "loginDate": "2019-08-24T14:15:22Z",
  "remark": "string",
  "dept": {
    "createBy": "string",
    "createTime": "2019-08-24T14:15:22Z",
    "updateBy": "string",
    "updateTime": "2019-08-24T14:15:22Z",
    "params": {
      "property1": {},
      "property2": {}
    },
    "parentName": "string",
    "parentId": 0,
    "children": [
      {
        "createBy": "string",
        "createTime": "2019-08-24T14:15:22Z",
        "updateBy": "string",
        "updateTime": "2019-08-24T14:15:22Z",
        "params": {
          "property1": {},
          "property2": {}
        },
        "parentName": "string",
        "parentId": 0,
        "children": [
          {
            "createBy": null,
            "createTime": null,
            "updateBy": null,
            "updateTime": null,
            "params": null,
            "parentName": null,
            "parentId": null,
            "children": null,
            "deptId": null,
            "deptName": null,
            "orderNum": null,
            "leader": null,
            "phone": null,
            "email": null,
            "status": null,
            "delFlag": null,
            "ancestors": null
          }
        ],
        "deptId": 0,
        "deptName": "string",
        "orderNum": 0,
        "leader": "string",
        "phone": "string",
        "email": "string",
        "status": "string",
        "delFlag": "string",
        "ancestors": "string"
      }
    ],
    "deptId": 0,
    "deptName": "string",
    "orderNum": 0,
    "leader": "string",
    "phone": "string",
    "email": "string",
    "status": "string",
    "delFlag": "string",
    "ancestors": "string"
  },
  "roles": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "roleId": 0,
      "roleName": "string",
      "roleKey": "string",
      "roleSort": 0,
      "dataScope": "string",
      "menuCheckStrictly": true,
      "deptCheckStrictly": true,
      "status": "string",
      "delFlag": "string",
      "remark": "string",
      "flag": true,
      "menuIds": [
        0
      ],
      "deptIds": [
        0
      ],
      "admin": true
    }
  ],
  "roleIds": [
    0
  ],
  "postIds": [
    0
  ],
  "roleId": 0,
  "admin": true
}

```

用户对象 sys_user

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|userId|integer(int64)|false|none||用户ID|
|deptId|integer(int64)|false|none||部门ID|
|userName|string(string)|true|none||用户账号|
|nickName|string(string)|true|none||用户昵称|
|userType|string(string)|false|none||用户类型（sys_user系统用户）|
|email|string(string)|false|none||用户邮箱|
|phonenumber|string(string)|false|none||手机号码|
|sex|string(string)|false|none||用户性别|
|avatar|string(string)|false|none||用户头像|
|password|string(string)|false|write-only||密码|
|status|string(string)|false|none||帐号状态（0正常 1停用）|
|delFlag|string(string)|false|none||删除标志（0代表存在 2代表删除）|
|loginIp|string(string)|false|none||最后登录IP|
|loginDate|string(date-time)|false|none||最后登录时间|
|remark|string(string)|false|none||备注|
|dept|[SysDept](#schemasysdept)|false|none||部门表 sys_dept|
|roles|[[SysRole](#schemasysrole)]|false|none||角色对象|
|roleIds|[integer]|false|none||角色组|
|postIds|[integer]|false|none||岗位组|
|roleId|integer(int64)|false|none||数据权限 当前角色ID|
|admin|boolean(boolean)|false|none||none|

<h2 id="tocS_SysUserRole">SysUserRole</h2>

<a id="schemasysuserrole"></a>
<a id="schema_SysUserRole"></a>
<a id="tocSsysuserrole"></a>
<a id="tocssysuserrole"></a>

```json
{
  "userId": 0,
  "roleId": 0
}

```

用户和角色关联 sys_user_role

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|userId|integer(int64)|false|none||用户ID|
|roleId|integer(int64)|false|none||角色ID|

<h2 id="tocS_SysPost">SysPost</h2>

<a id="schemasyspost"></a>
<a id="schema_SysPost"></a>
<a id="tocSsyspost"></a>
<a id="tocssyspost"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "postId": 0,
  "postCode": "string",
  "postName": "string",
  "postSort": 0,
  "status": "string",
  "remark": "string",
  "flag": true
}

```

岗位表 sys_post

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|postId|integer(int64)|false|none||岗位序号|
|postCode|string(string)|true|none||岗位编码|
|postName|string(string)|true|none||岗位名称|
|postSort|integer(int32)|true|none||岗位排序|
|status|string(string)|false|none||状态（0正常 1停用）|
|remark|string(string)|false|none||备注|
|flag|boolean(boolean)|false|none||用户是否存在此岗位标识 默认不存在|

<h2 id="tocS_SysOssConfigBo">SysOssConfigBo</h2>

<a id="schemasysossconfigbo"></a>
<a id="schema_SysOssConfigBo"></a>
<a id="tocSsysossconfigbo"></a>
<a id="tocssysossconfigbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "ossConfigId": 0,
  "configKey": "string",
  "accessKey": "string",
  "secretKey": "string",
  "bucketName": "string",
  "prefix": "string",
  "endpoint": "string",
  "domain": "string",
  "isHttps": "string",
  "status": "string",
  "region": "string",
  "ext1": "string",
  "remark": "string",
  "accessPolicy": "string"
}

```

对象存储配置业务对象 sys_oss_config

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|ossConfigId|integer(int64)|true|none||主建|
|configKey|string(string)|true|none||配置key|
|accessKey|string(string)|true|none||accessKey|
|secretKey|string(string)|true|none||秘钥|
|bucketName|string(string)|true|none||桶名称|
|prefix|string(string)|false|none||前缀|
|endpoint|string(string)|true|none||访问站点|
|domain|string(string)|false|none||自定义域名|
|isHttps|string(string)|false|none||是否https（Y=是,N=否）|
|status|string(string)|false|none||是否默认（0=是,1=否）|
|region|string(string)|false|none||域|
|ext1|string(string)|false|none||扩展字段|
|remark|string(string)|false|none||备注|
|accessPolicy|string(string)|true|none||桶权限类型(0private 1public 2custom)|

<h2 id="tocS_SysNotice">SysNotice</h2>

<a id="schemasysnotice"></a>
<a id="schema_SysNotice"></a>
<a id="tocSsysnotice"></a>
<a id="tocssysnotice"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "noticeId": 0,
  "noticeTitle": "string",
  "noticeType": "string",
  "noticeContent": "string",
  "status": "string",
  "remark": "string"
}

```

通知公告表 sys_notice

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|noticeId|integer(int64)|false|none||公告ID|
|noticeTitle|string(string)|true|none||公告标题|
|noticeType|string(string)|false|none||公告类型（1通知 2公告）|
|noticeContent|string(string)|false|none||公告内容|
|status|string(string)|false|none||公告状态（0正常 1关闭）|
|remark|string(string)|false|none||备注|

<h2 id="tocS_SysMenu">SysMenu</h2>

<a id="schemasysmenu"></a>
<a id="schema_SysMenu"></a>
<a id="tocSsysmenu"></a>
<a id="tocssysmenu"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "parentName": "string",
  "parentId": 0,
  "children": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "parentName": "string",
      "parentId": 0,
      "children": [
        {
          "createBy": "string",
          "createTime": "2019-08-24T14:15:22Z",
          "updateBy": "string",
          "updateTime": "2019-08-24T14:15:22Z",
          "params": {
            "property1": {},
            "property2": {}
          },
          "parentName": "string",
          "parentId": 0,
          "children": [
            {}
          ],
          "menuId": 0,
          "menuName": "string",
          "orderNum": 0,
          "path": "string",
          "component": "string",
          "queryParam": "string",
          "isFrame": "string",
          "isCache": "string",
          "menuType": "string",
          "visible": "string",
          "status": "string",
          "perms": "string",
          "icon": "string",
          "remark": "string"
        }
      ],
      "menuId": 0,
      "menuName": "string",
      "orderNum": 0,
      "path": "string",
      "component": "string",
      "queryParam": "string",
      "isFrame": "string",
      "isCache": "string",
      "menuType": "string",
      "visible": "string",
      "status": "string",
      "perms": "string",
      "icon": "string",
      "remark": "string"
    }
  ],
  "menuId": 0,
  "menuName": "string",
  "orderNum": 0,
  "path": "string",
  "component": "string",
  "queryParam": "string",
  "isFrame": "string",
  "isCache": "string",
  "menuType": "string",
  "visible": "string",
  "status": "string",
  "perms": "string",
  "icon": "string",
  "remark": "string"
}

```

菜单权限表 sys_menu

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|parentName|string(string)|false|none||父菜单名称|
|parentId|integer(int64)|false|none||父菜单ID|
|children|[[SysMenu](#schemasysmenu)]|false|none||子部门|
|menuId|integer(int64)|false|none||菜单ID|
|menuName|string(string)|true|none||菜单名称|
|orderNum|integer(int32)|true|none||显示顺序|
|path|string(string)|false|none||路由地址|
|component|string(string)|false|none||组件路径|
|queryParam|string(string)|false|none||路由参数|
|isFrame|string(string)|false|none||是否为外链（0是 1否）|
|isCache|string(string)|false|none||是否缓存（0缓存 1不缓存）|
|menuType|string(string)|true|none||类型（M目录 C菜单 F按钮）|
|visible|string(string)|false|none||显示状态（0显示 1隐藏）|
|status|string(string)|false|none||菜单状态（0正常 1停用）|
|perms|string(string)|false|none||权限字符串|
|icon|string(string)|false|none||菜单图标|
|remark|string(string)|false|none||备注|

<h2 id="tocS_SysDictType">SysDictType</h2>

<a id="schemasysdicttype"></a>
<a id="schema_SysDictType"></a>
<a id="tocSsysdicttype"></a>
<a id="tocssysdicttype"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "dictId": 0,
  "dictName": "string",
  "dictType": "string",
  "status": "string",
  "remark": "string"
}

```

字典类型表 sys_dict_type

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|dictId|integer(int64)|false|none||字典主键|
|dictName|string(string)|true|none||字典名称|
|dictType|string(string)|true|none||字典类型|
|status|string(string)|false|none||状态（0正常 1停用）|
|remark|string(string)|false|none||备注|

<h2 id="tocS_SysDictData">SysDictData</h2>

<a id="schemasysdictdata"></a>
<a id="schema_SysDictData"></a>
<a id="tocSsysdictdata"></a>
<a id="tocssysdictdata"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "dictCode": 0,
  "dictSort": 0,
  "dictLabel": "string",
  "dictValue": "string",
  "dictType": "string",
  "cssClass": "string",
  "listClass": "string",
  "isDefault": "string",
  "status": "string",
  "remark": "string",
  "default": true
}

```

字典数据表 sys_dict_data

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|dictCode|integer(int64)|false|none||字典编码|
|dictSort|integer(int32)|false|none||字典排序|
|dictLabel|string(string)|true|none||字典标签|
|dictValue|string(string)|true|none||字典键值|
|dictType|string(string)|true|none||字典类型|
|cssClass|string(string)|false|none||样式属性（其他样式扩展）|
|listClass|string(string)|false|none||表格字典样式|
|isDefault|string(string)|false|none||是否默认（Y是 N否）|
|status|string(string)|false|none||状态（0正常 1停用）|
|remark|string(string)|false|none||备注|
|default|boolean(boolean)|false|none||none|

<h2 id="tocS_SysConfig">SysConfig</h2>

<a id="schemasysconfig"></a>
<a id="schema_SysConfig"></a>
<a id="tocSsysconfig"></a>
<a id="tocssysconfig"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "configId": 0,
  "configName": "string",
  "configKey": "string",
  "configValue": "string",
  "configType": "string",
  "remark": "string"
}

```

参数配置表 sys_config

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|configId|integer(int64)|false|none||参数主键|
|configName|string(string)|true|none||参数名称|
|configKey|string(string)|true|none||参数键名|
|configValue|string(string)|true|none||参数键值|
|configType|string(string)|false|none||系统内置（Y是 N否）|
|remark|string(string)|false|none||备注|

<h2 id="tocS_TestTreeBo">TestTreeBo</h2>

<a id="schematesttreebo"></a>
<a id="schema_TestTreeBo"></a>
<a id="tocStesttreebo"></a>
<a id="tocstesttreebo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "parentName": "string",
  "parentId": 0,
  "children": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "parentName": "string",
      "parentId": 0,
      "children": [
        {
          "createBy": "string",
          "createTime": "2019-08-24T14:15:22Z",
          "updateBy": "string",
          "updateTime": "2019-08-24T14:15:22Z",
          "params": {
            "property1": {},
            "property2": {}
          },
          "parentName": "string",
          "parentId": 0,
          "children": [
            {}
          ],
          "id": 0,
          "deptId": 0,
          "userId": 0,
          "treeName": "string"
        }
      ],
      "id": 0,
      "deptId": 0,
      "userId": 0,
      "treeName": "string"
    }
  ],
  "id": 0,
  "deptId": 0,
  "userId": 0,
  "treeName": "string"
}

```

测试树表业务对象 test_tree

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|parentName|string(string)|false|none||父菜单名称|
|parentId|integer(int64)|false|none||父菜单ID|
|children|[[TestTreeBo](#schematesttreebo)]|false|none||子部门|
|id|integer(int64)|true|none||主键|
|deptId|integer(int64)|true|none||部门id|
|userId|integer(int64)|true|none||用户id|
|treeName|string(string)|true|none||树节点名|

<h2 id="tocS_TestDemoBo">TestDemoBo</h2>

<a id="schematestdemobo"></a>
<a id="schema_TestDemoBo"></a>
<a id="tocStestdemobo"></a>
<a id="tocstestdemobo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "deptId": 0,
  "userId": 0,
  "orderNum": 0,
  "testKey": "string",
  "value": "string"
}

```

测试单表业务对象 test_demo

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||主键|
|deptId|integer(int64)|true|none||部门id|
|userId|integer(int64)|true|none||用户id|
|orderNum|integer(int32)|true|none||排序号|
|testKey|string(string)|true|none||key键|
|value|string(string)|true|none||值|

<h2 id="tocS_RMapStringObject">RMapStringObject</h2>

<a id="schemarmapstringobject"></a>
<a id="schema_RMapStringObject"></a>
<a id="tocSrmapstringobject"></a>
<a id="tocsrmapstringobject"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "property1": {},
    "property2": {}
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|object|false|none||none|
|» **additionalProperties**|object|false|none||none|

<h2 id="tocS_PayDto">PayDto</h2>

<a id="schemapaydto"></a>
<a id="schema_PayDto"></a>
<a id="tocSpaydto"></a>
<a id="tocspaydto"></a>

```json
{
  "payCode": 0,
  "payMethod": "string",
  "clientIp": "string",
  "payAmount": 0,
  "orderNo": "string",
  "goodsDetail": "string",
  "goodsDescription": "string",
  "payScene": "string",
  "termNo": "string",
  "openId": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|payCode|integer(int32)|true|none||payCode 1=微信支付，2=支付宝支付|
|payMethod|string|false|none||支付类型|
|clientIp|string|false|none||clientIp|
|payAmount|number|true|none||支付金额不能为空|
|orderNo|string|true|none||订单号不能为空|
|goodsDetail|string|true|none||商品详情不能为空|
|goodsDescription|string|false|none||none|
|payScene|string|true|none||支付场景，1-小程序端，2-h5端,3-PC端，|
|termNo|string|false|none||设备号|
|openId|string|false|none||openid(jsapi支付不能为空)|

<h2 id="tocS_R">R</h2>

<a id="schemar"></a>
<a id="schema_R"></a>
<a id="tocSr"></a>
<a id="tocsr"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {}
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|object|false|none||none|

<h2 id="tocS_RMapStringString">RMapStringString</h2>

<a id="schemarmapstringstring"></a>
<a id="schema_RMapStringString"></a>
<a id="tocSrmapstringstring"></a>
<a id="tocsrmapstringstring"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "property1": "string",
    "property2": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|object|false|none||none|
|» **additionalProperties**|string|false|none||none|

<h2 id="tocS_RString">RString</h2>

<a id="schemarstring"></a>
<a id="schema_RString"></a>
<a id="tocSrstring"></a>
<a id="tocsrstring"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": "string"
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|string|false|none||none|

<h2 id="tocS_SmsLoginBody">SmsLoginBody</h2>

<a id="schemasmsloginbody"></a>
<a id="schema_SmsLoginBody"></a>
<a id="tocSsmsloginbody"></a>
<a id="tocssmsloginbody"></a>

```json
{
  "phonenumber": "string",
  "smsCode": "string"
}

```

短信登录对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|phonenumber|string|true|none||手机号|
|smsCode|string|true|none||短信code|

<h2 id="tocS_RegisterBody">RegisterBody</h2>

<a id="schemaregisterbody"></a>
<a id="schema_RegisterBody"></a>
<a id="tocSregisterbody"></a>
<a id="tocsregisterbody"></a>

```json
{
  "username": "string",
  "password": "string",
  "code": "string",
  "uuid": "string",
  "userType": "string"
}

```

用户注册对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|username|string|true|none||用户名|
|password|string|true|none||用户密码|
|code|string|false|none||验证码|
|uuid|string|false|none||唯一标识|
|userType|string|false|none||none|

<h2 id="tocS_SysOperLog">SysOperLog</h2>

<a id="schemasysoperlog"></a>
<a id="schema_SysOperLog"></a>
<a id="tocSsysoperlog"></a>
<a id="tocssysoperlog"></a>

```json
{
  "operId": 0,
  "title": "string",
  "businessType": 0,
  "businessTypes": [
    0
  ],
  "method": "string",
  "requestMethod": "string",
  "operatorType": 0,
  "operName": "string",
  "deptName": "string",
  "operUrl": "string",
  "operIp": "string",
  "operLocation": "string",
  "operParam": "string",
  "jsonResult": "string",
  "status": 0,
  "errorMsg": "string",
  "operTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  }
}

```

操作日志记录表 oper_log

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|operId|integer(int64)|false|none||日志主键|
|title|string(string)|false|none||操作模块|
|businessType|integer(int32)|false|none||业务类型（0其它 1新增 2修改 3删除）|
|businessTypes|[integer]|false|none||业务类型数组|
|method|string(string)|false|none||请求方法|
|requestMethod|string(string)|false|none||请求方式|
|operatorType|integer(int32)|false|none||操作类别（0其它 1后台用户 2手机端用户）|
|operName|string(string)|false|none||操作人员|
|deptName|string(string)|false|none||部门名称|
|operUrl|string(string)|false|none||请求url|
|operIp|string(string)|false|none||操作地址|
|operLocation|string(string)|false|none||操作地点|
|operParam|string(string)|false|none||请求参数|
|jsonResult|string(string)|false|none||返回参数|
|status|integer(int32)|false|none||操作状态（0正常 1异常）|
|errorMsg|string(string)|false|none||错误消息|
|operTime|string(date-time)|false|none||操作时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|

<h2 id="tocS_SysLogininfor">SysLogininfor</h2>

<a id="schemasyslogininfor"></a>
<a id="schema_SysLogininfor"></a>
<a id="tocSsyslogininfor"></a>
<a id="tocssyslogininfor"></a>

```json
{
  "infoId": 0,
  "userName": "string",
  "status": "string",
  "ipaddr": "string",
  "loginLocation": "string",
  "browser": "string",
  "os": "string",
  "msg": "string",
  "loginTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  }
}

```

系统访问记录表 sys_logininfor

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|infoId|integer(int64)|false|none||ID|
|userName|string(string)|false|none||用户账号|
|status|string(string)|false|none||登录状态 0成功 1失败|
|ipaddr|string(string)|false|none||登录IP地址|
|loginLocation|string(string)|false|none||登录地点|
|browser|string(string)|false|none||浏览器类型|
|os|string(string)|false|none||操作系统|
|msg|string(string)|false|none||提示消息|
|loginTime|string(date-time)|false|none||访问时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|

<h2 id="tocS_LoginBody">LoginBody</h2>

<a id="schemaloginbody"></a>
<a id="schema_LoginBody"></a>
<a id="tocSloginbody"></a>
<a id="tocsloginbody"></a>

```json
{
  "username": "string",
  "password": "string",
  "code": "string",
  "uuid": "string"
}

```

用户登录对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|username|string|true|none||用户名|
|password|string|true|none||用户密码|
|code|string|false|none||验证码|
|uuid|string|false|none||唯一标识|

<h2 id="tocS_EmailLoginBody">EmailLoginBody</h2>

<a id="schemaemailloginbody"></a>
<a id="schema_EmailLoginBody"></a>
<a id="tocSemailloginbody"></a>
<a id="tocsemailloginbody"></a>

```json
{
  "email": "string",
  "emailCode": "string"
}

```

邮箱登录对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|email|string|true|none||邮箱|
|emailCode|string|true|none||邮箱code|

<h2 id="tocS_ExportDemoVo">ExportDemoVo</h2>

<a id="schemaexportdemovo"></a>
<a id="schema_ExportDemoVo"></a>
<a id="tocSexportdemovo"></a>
<a id="tocsexportdemovo"></a>

```json
{
  "nickName": "string",
  "userStatus": "string",
  "gender": "string",
  "phoneNumber": "string",
  "email": "string",
  "province": "string",
  "provinceId": 0,
  "city": "string",
  "cityId": 0,
  "area": "string",
  "areaId": 0
}

```

带有下拉选的Excel导出

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|nickName|string|true|none||用户昵称|
|userStatus|string|true|none||用户类型<br /> </p><br /> 使用ExcelEnumFormat注解需要进行下拉选的部分|
|gender|string|true|none||性别<br /> <p><br /> 使用ExcelDictFormat注解需要进行下拉选的部分|
|phoneNumber|string|true|none||手机号|
|email|string|true|none||Email|
|province|string|true|none||省<br /> <p><br /> 级联下拉，仅判断是否选了|
|provinceId|integer(int32)|true|none||数据库中的省ID<br /> </p><br /> 处理完毕后再判断是否市正确的值|
|city|string|true|none||市<br /> <p><br /> 级联下拉|
|cityId|integer(int32)|true|none||数据库中的市ID|
|area|string|true|none||县<br /> <p><br /> 级联下拉|
|areaId|integer(int32)|true|none||数据库中的县ID|

<h2 id="tocS_WxLoginDto">WxLoginDto</h2>

<a id="schemawxlogindto"></a>
<a id="schema_WxLoginDto"></a>
<a id="tocSwxlogindto"></a>
<a id="tocswxlogindto"></a>

```json
{
  "jsCode": "string",
  "brandType": 0,
  "referrer": "string",
  "phone": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|jsCode|string|true|none||none|
|brandType|integer(int32)|false|none||品牌类型 1=yxr 2=jxh 3=mbti|
|referrer|string|false|none||推荐人|
|phone|string|false|none||手机号|

<h2 id="tocS_PageQuery">PageQuery</h2>

<a id="schemapagequery"></a>
<a id="schema_PageQuery"></a>
<a id="tocSpagequery"></a>
<a id="tocspagequery"></a>

```json
{
  "pageSize": 0,
  "pageNum": 0,
  "orderByColumn": "string",
  "isAsc": "string"
}

```

分页查询实体类

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|pageSize|integer(int32)|false|none||分页大小|
|pageNum|integer(int32)|false|none||当前页数|
|orderByColumn|string(string)|false|none||排序列|
|isAsc|string(string)|false|none||排序的方向desc或者asc|

<h2 id="tocS_TableDataInfoGenTable">TableDataInfoGenTable</h2>

<a id="schematabledatainfogentable"></a>
<a id="schema_TableDataInfoGenTable"></a>
<a id="tocStabledatainfogentable"></a>
<a id="tocstabledatainfogentable"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "tableId": 0,
      "tableName": "string",
      "tableComment": "string",
      "subTableName": "string",
      "subTableFkName": "string",
      "className": "string",
      "tplCategory": "string",
      "packageName": "string",
      "moduleName": "string",
      "businessName": "string",
      "functionName": "string",
      "functionAuthor": "string",
      "genType": "string",
      "genPath": "string",
      "pkColumn": {
        "createBy": "string",
        "createTime": "2019-08-24T14:15:22Z",
        "updateBy": "string",
        "updateTime": "2019-08-24T14:15:22Z",
        "params": {
          "property1": {},
          "property2": {}
        },
        "columnId": 0,
        "tableId": 0,
        "columnName": "string",
        "columnComment": "string",
        "columnType": "string",
        "javaType": "string",
        "javaField": "string",
        "isPk": "string",
        "isIncrement": "string",
        "isRequired": "string",
        "isInsert": "string",
        "isEdit": "string",
        "isList": "string",
        "isQuery": "string",
        "queryType": "string",
        "htmlType": "string",
        "dictType": "string",
        "sort": 0,
        "list": true,
        "pk": true,
        "insert": true,
        "edit": true,
        "usableColumn": true,
        "superColumn": true,
        "required": true,
        "capJavaField": "string",
        "increment": true,
        "query": true
      },
      "subTable": {
        "createBy": "string",
        "createTime": "2019-08-24T14:15:22Z",
        "updateBy": "string",
        "updateTime": "2019-08-24T14:15:22Z",
        "params": {
          "property1": {},
          "property2": {}
        },
        "tableId": 0,
        "tableName": "string",
        "tableComment": "string",
        "subTableName": "string",
        "subTableFkName": "string",
        "className": "string",
        "tplCategory": "string",
        "packageName": "string",
        "moduleName": "string",
        "businessName": "string",
        "functionName": "string",
        "functionAuthor": "string",
        "genType": "string",
        "genPath": "string",
        "pkColumn": {
          "createBy": "string",
          "createTime": "2019-08-24T14:15:22Z",
          "updateBy": "string",
          "updateTime": "2019-08-24T14:15:22Z",
          "params": {},
          "columnId": 0,
          "tableId": 0,
          "columnName": "string",
          "columnComment": "string",
          "columnType": "string",
          "javaType": "string",
          "javaField": "string",
          "isPk": "string",
          "isIncrement": "string",
          "isRequired": "string",
          "isInsert": "string",
          "isEdit": "string",
          "isList": "string",
          "isQuery": "string",
          "queryType": "string",
          "htmlType": "string",
          "dictType": "string",
          "sort": 0,
          "list": true,
          "pk": true,
          "insert": true,
          "edit": true,
          "usableColumn": true,
          "superColumn": true,
          "required": true,
          "capJavaField": "string",
          "increment": true,
          "query": true
        },
        "subTable": {
          "createBy": "string",
          "createTime": "2019-08-24T14:15:22Z",
          "updateBy": "string",
          "updateTime": "2019-08-24T14:15:22Z",
          "params": {},
          "tableId": 0,
          "tableName": "string",
          "tableComment": "string",
          "subTableName": "string",
          "subTableFkName": "string",
          "className": "string",
          "tplCategory": "string",
          "packageName": "string",
          "moduleName": "string",
          "businessName": "string",
          "functionName": "string",
          "functionAuthor": "string",
          "genType": "string",
          "genPath": "string",
          "pkColumn": {},
          "subTable": {},
          "columns": [
            null
          ],
          "options": "string",
          "remark": "string",
          "treeCode": "string",
          "treeParentCode": "string",
          "treeName": "string",
          "menuIds": [
            null
          ],
          "parentMenuId": "string",
          "parentMenuName": "string",
          "sub": true,
          "tree": true,
          "crud": true
        },
        "columns": [
          {
            "createBy": null,
            "createTime": null,
            "updateBy": null,
            "updateTime": null,
            "params": null,
            "columnId": null,
            "tableId": null,
            "columnName": null,
            "columnComment": null,
            "columnType": null,
            "javaType": null,
            "javaField": null,
            "isPk": null,
            "isIncrement": null,
            "isRequired": null,
            "isInsert": null,
            "isEdit": null,
            "isList": null,
            "isQuery": null,
            "queryType": null,
            "htmlType": null,
            "dictType": null,
            "sort": null,
            "list": null,
            "pk": null,
            "insert": null,
            "edit": null,
            "usableColumn": null,
            "superColumn": null,
            "required": null,
            "capJavaField": null,
            "increment": null,
            "query": null
          }
        ],
        "options": "string",
        "remark": "string",
        "treeCode": "string",
        "treeParentCode": "string",
        "treeName": "string",
        "menuIds": [
          0
        ],
        "parentMenuId": "string",
        "parentMenuName": "string",
        "sub": true,
        "tree": true,
        "crud": true
      },
      "columns": [
        {
          "createBy": "string",
          "createTime": "2019-08-24T14:15:22Z",
          "updateBy": "string",
          "updateTime": "2019-08-24T14:15:22Z",
          "params": {
            "property1": {},
            "property2": {}
          },
          "columnId": 0,
          "tableId": 0,
          "columnName": "string",
          "columnComment": "string",
          "columnType": "string",
          "javaType": "string",
          "javaField": "string",
          "isPk": "string",
          "isIncrement": "string",
          "isRequired": "string",
          "isInsert": "string",
          "isEdit": "string",
          "isList": "string",
          "isQuery": "string",
          "queryType": "string",
          "htmlType": "string",
          "dictType": "string",
          "sort": 0,
          "list": true,
          "pk": true,
          "insert": true,
          "edit": true,
          "usableColumn": true,
          "superColumn": true,
          "required": true,
          "capJavaField": "string",
          "increment": true,
          "query": true
        }
      ],
      "options": "string",
      "remark": "string",
      "treeCode": "string",
      "treeParentCode": "string",
      "treeName": "string",
      "menuIds": [
        0
      ],
      "parentMenuId": "string",
      "parentMenuName": "string",
      "sub": true,
      "tree": true,
      "crud": true
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[GenTable](#schemagentable)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_TableDataInfoGenTableColumn">TableDataInfoGenTableColumn</h2>

<a id="schematabledatainfogentablecolumn"></a>
<a id="schema_TableDataInfoGenTableColumn"></a>
<a id="tocStabledatainfogentablecolumn"></a>
<a id="tocstabledatainfogentablecolumn"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "columnId": 0,
      "tableId": 0,
      "columnName": "string",
      "columnComment": "string",
      "columnType": "string",
      "javaType": "string",
      "javaField": "string",
      "isPk": "string",
      "isIncrement": "string",
      "isRequired": "string",
      "isInsert": "string",
      "isEdit": "string",
      "isList": "string",
      "isQuery": "string",
      "queryType": "string",
      "htmlType": "string",
      "dictType": "string",
      "sort": 0,
      "list": true,
      "pk": true,
      "insert": true,
      "edit": true,
      "usableColumn": true,
      "superColumn": true,
      "required": true,
      "capJavaField": "string",
      "increment": true,
      "query": true
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[GenTableColumn](#schemagentablecolumn)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_PayWxConfigVo">PayWxConfigVo</h2>

<a id="schemapaywxconfigvo"></a>
<a id="schema_PayWxConfigVo"></a>
<a id="tocSpaywxconfigvo"></a>
<a id="tocspaywxconfigvo"></a>

```json
{
  "id": "string",
  "appId": "string",
  "mchId": "string",
  "mchKey": "string",
  "privateKeyPath": "string",
  "privateCertPath": "string",
  "serialNo": "string",
  "notifyHostUrl": "string",
  "status": 0,
  "remark": "string",
  "isDelete": 0
}

```

微信支付配置视图对象 t_pay_wx_config

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|string|false|none||自增id|
|appId|string|false|none||应用编号|
|mchId|string|false|none||商户号|
|mchKey|string|false|none||密钥|
|privateKeyPath|string|false|none||商户私钥路径|
|privateCertPath|string|false|none||公钥路径|
|serialNo|string|false|none||商户证书序列号|
|notifyHostUrl|string|false|none||退款通知回调|
|status|integer(int32)|false|none||启用状态，0:禁用 1:启用|
|remark|string|false|none||备注|
|isDelete|integer(int64)|false|none||逻辑删除：1 正常，1 删除|

<h2 id="tocS_RPayWxConfigVo">RPayWxConfigVo</h2>

<a id="schemarpaywxconfigvo"></a>
<a id="schema_RPayWxConfigVo"></a>
<a id="tocSrpaywxconfigvo"></a>
<a id="tocsrpaywxconfigvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": "string",
    "appId": "string",
    "mchId": "string",
    "mchKey": "string",
    "privateKeyPath": "string",
    "privateCertPath": "string",
    "serialNo": "string",
    "notifyHostUrl": "string",
    "status": 0,
    "remark": "string",
    "isDelete": 0
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[PayWxConfigVo](#schemapaywxconfigvo)|false|none||微信支付配置视图对象 t_pay_wx_config|

<h2 id="tocS_TableDataInfoPayWxConfigVo">TableDataInfoPayWxConfigVo</h2>

<a id="schematabledatainfopaywxconfigvo"></a>
<a id="schema_TableDataInfoPayWxConfigVo"></a>
<a id="tocStabledatainfopaywxconfigvo"></a>
<a id="tocstabledatainfopaywxconfigvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": "string",
      "appId": "string",
      "mchId": "string",
      "mchKey": "string",
      "privateKeyPath": "string",
      "privateCertPath": "string",
      "serialNo": "string",
      "notifyHostUrl": "string",
      "status": 0,
      "remark": "string",
      "isDelete": 0
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[PayWxConfigVo](#schemapaywxconfigvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_CustomImageVo">CustomImageVo</h2>

<a id="schemacustomimagevo"></a>
<a id="schema_CustomImageVo"></a>
<a id="tocScustomimagevo"></a>
<a id="tocscustomimagevo"></a>

```json
{
  "imageId": 0,
  "customId": 0,
  "personalImageUrl": "string",
  "blindImageUrl": "string",
  "imageUrl": "string",
  "remark": "string"
}

```

照片管理视图对象 t_custom_image

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|imageId|integer(int64)|false|none||自增id|
|customId|integer(int64)|false|none||关联客户id|
|personalImageUrl|string|false|none||个人资料照片|
|blindImageUrl|string|false|none||盲盒照片|
|imageUrl|string|false|none||非盲盒照片|
|remark|string|false|none||备注|

<h2 id="tocS_RCustomImageVo">RCustomImageVo</h2>

<a id="schemarcustomimagevo"></a>
<a id="schema_RCustomImageVo"></a>
<a id="tocSrcustomimagevo"></a>
<a id="tocsrcustomimagevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "imageId": 0,
    "customId": 0,
    "personalImageUrl": "string",
    "blindImageUrl": "string",
    "imageUrl": "string",
    "remark": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[CustomImageVo](#schemacustomimagevo)|false|none||照片管理视图对象 t_custom_image|

<h2 id="tocS_TableDataInfoCustomImageVo">TableDataInfoCustomImageVo</h2>

<a id="schematabledatainfocustomimagevo"></a>
<a id="schema_TableDataInfoCustomImageVo"></a>
<a id="tocStabledatainfocustomimagevo"></a>
<a id="tocstabledatainfocustomimagevo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "imageId": 0,
      "customId": 0,
      "personalImageUrl": "string",
      "blindImageUrl": "string",
      "imageUrl": "string",
      "remark": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[CustomImageVo](#schemacustomimagevo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_CustomAuthencationVo">CustomAuthencationVo</h2>

<a id="schemacustomauthencationvo"></a>
<a id="schema_CustomAuthencationVo"></a>
<a id="tocScustomauthencationvo"></a>
<a id="tocscustomauthencationvo"></a>

```json
{
  "id": 0,
  "customId": 0,
  "nameAuthenticationSta": 0,
  "academicCertificationSta": 0,
  "jobCertificationSta": 0,
  "nameAuthentication": "string",
  "academicCertification": "string",
  "jobCertification": "string",
  "nameAuthenticationFailReason": "string",
  "academicCertificationFailReason": "string",
  "jobCertificationFailReason": "string",
  "nameAuthType": 0,
  "nameAuthName": "string",
  "nameAuthCertNo": "string",
  "academicAuthType": 0,
  "academicAuthName": "string",
  "academicAuthSit": "string",
  "jobAuthType": 0,
  "jobAuthCompanyAllName": "string",
  "jobAuthCompanyName": "string"
}

```

客户认证资料视图对象 t_custom_authencation

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||none|
|customId|integer(int64)|false|none||客户id|
|nameAuthenticationSta|integer(int32)|false|none||实名认证状态 0-认证中|1-认证成功|2-认证失败|
|academicCertificationSta|integer(int32)|false|none||学历认证状态 0-认证中|1-认证成功|2-认证失败|
|jobCertificationSta|integer(int32)|false|none||工作认证状态|
|nameAuthentication|string|false|none||实名认证图片分号分隔|
|academicCertification|string|false|none||学历图片，分号分隔|
|jobCertification|string|false|none||工作图片，分号分隔|
|nameAuthenticationFailReason|string|false|none||实名认证失败原因|
|academicCertificationFailReason|string|false|none||学历认证失败原因|
|jobCertificationFailReason|string|false|none||工作认证失败原因|
|nameAuthType|integer(int32)|false|none||实名认证方式，1-居民身份证，2-护照，3-社会保障卡|
|nameAuthName|string|false|none||实名认证名字|
|nameAuthCertNo|string|false|none||实名认证证件号|
|academicAuthType|integer(int32)|false|none||学历认证方式，1-学位证书，2-毕业证书，3-学信网截图|
|academicAuthName|string|false|none||学历认证学校名称|
|academicAuthSit|string|false|none||学历认证学位|
|jobAuthType|integer(int32)|false|none||工作认证方式，1-劳动合同，2-公司名片/工卡，3-社保缴费记录，4-自由职业证明|
|jobAuthCompanyAllName|string|false|none||工作认证公司全称|
|jobAuthCompanyName|string|false|none||工作认证公司简称|

<h2 id="tocS_RCustomAuthencationVo">RCustomAuthencationVo</h2>

<a id="schemarcustomauthencationvo"></a>
<a id="schema_RCustomAuthencationVo"></a>
<a id="tocSrcustomauthencationvo"></a>
<a id="tocsrcustomauthencationvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "customId": 0,
    "nameAuthenticationSta": 0,
    "academicCertificationSta": 0,
    "jobCertificationSta": 0,
    "nameAuthentication": "string",
    "academicCertification": "string",
    "jobCertification": "string",
    "nameAuthenticationFailReason": "string",
    "academicCertificationFailReason": "string",
    "jobCertificationFailReason": "string",
    "nameAuthType": 0,
    "nameAuthName": "string",
    "nameAuthCertNo": "string",
    "academicAuthType": 0,
    "academicAuthName": "string",
    "academicAuthSit": "string",
    "jobAuthType": 0,
    "jobAuthCompanyAllName": "string",
    "jobAuthCompanyName": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[CustomAuthencationVo](#schemacustomauthencationvo)|false|none||客户认证资料视图对象 t_custom_authencation|

<h2 id="tocS_TableDataInfoCustomAuthencationVo">TableDataInfoCustomAuthencationVo</h2>

<a id="schematabledatainfocustomauthencationvo"></a>
<a id="schema_TableDataInfoCustomAuthencationVo"></a>
<a id="tocStabledatainfocustomauthencationvo"></a>
<a id="tocstabledatainfocustomauthencationvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "customId": 0,
      "nameAuthenticationSta": 0,
      "academicCertificationSta": 0,
      "jobCertificationSta": 0,
      "nameAuthentication": "string",
      "academicCertification": "string",
      "jobCertification": "string",
      "nameAuthenticationFailReason": "string",
      "academicCertificationFailReason": "string",
      "jobCertificationFailReason": "string",
      "nameAuthType": 0,
      "nameAuthName": "string",
      "nameAuthCertNo": "string",
      "academicAuthType": 0,
      "academicAuthName": "string",
      "academicAuthSit": "string",
      "jobAuthType": 0,
      "jobAuthCompanyAllName": "string",
      "jobAuthCompanyName": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[CustomAuthencationVo](#schemacustomauthencationvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RCustomVo">RCustomVo</h2>

<a id="schemarcustomvo"></a>
<a id="schema_RCustomVo"></a>
<a id="tocSrcustomvo"></a>
<a id="tocsrcustomvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "customId": 0,
    "realName": "string",
    "phoneNumber": "string",
    "wxNumber": "string",
    "sexType": "string",
    "birthDate": "2019-08-24T14:15:22Z",
    "pureHeight": "string",
    "homeTown": "string",
    "eduBackground": "string",
    "finalSchool": "string",
    "familySituation": "string",
    "emotionalState": "string",
    "loveExperience": "string",
    "workCity": "string",
    "workJob": "string",
    "workCompany": "string",
    "yearIncome": "string",
    "houseState": "string",
    "futureCity": "string",
    "futurePlan": "string",
    "personalIntro": "string",
    "familyIntro": "string",
    "loveIntro": "string",
    "imageUrl": "string",
    "openid": "string",
    "verifyStatus": 0,
    "extension": "string",
    "eduImageUrl": "string",
    "referrer": "string",
    "nickName": "string",
    "constellation": "string",
    "marryTime": "string",
    "idealRemark": "string",
    "carState": "string",
    "publicSchedule": "string",
    "shareCode": "string",
    "residencePlace": "string",
    "permanentPlace": "string",
    "userType": "string",
    "weight": "string",
    "nation": "string",
    "hobby": "string",
    "memberType": "string",
    "verifyPhoneStatus": "string",
    "friendName": "string",
    "isDeleted": "string",
    "nameCertifiedStatus": 0,
    "eduCertifiedStatus": 0,
    "jobCertifiedStatus": 0,
    "loveStatus": 0,
    "avatarUrl": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[CustomVo](#schemacustomvo)|false|none||客户信息视图对象 t_custom|

<h2 id="tocS_TableDataInfoCustomVo">TableDataInfoCustomVo</h2>

<a id="schematabledatainfocustomvo"></a>
<a id="schema_TableDataInfoCustomVo"></a>
<a id="tocStabledatainfocustomvo"></a>
<a id="tocstabledatainfocustomvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "customId": 0,
      "realName": "string",
      "phoneNumber": "string",
      "wxNumber": "string",
      "sexType": "string",
      "birthDate": "2019-08-24T14:15:22Z",
      "pureHeight": "string",
      "homeTown": "string",
      "eduBackground": "string",
      "finalSchool": "string",
      "familySituation": "string",
      "emotionalState": "string",
      "loveExperience": "string",
      "workCity": "string",
      "workJob": "string",
      "workCompany": "string",
      "yearIncome": "string",
      "houseState": "string",
      "futureCity": "string",
      "futurePlan": "string",
      "personalIntro": "string",
      "familyIntro": "string",
      "loveIntro": "string",
      "imageUrl": "string",
      "openid": "string",
      "verifyStatus": 0,
      "extension": "string",
      "eduImageUrl": "string",
      "referrer": "string",
      "nickName": "string",
      "constellation": "string",
      "marryTime": "string",
      "idealRemark": "string",
      "carState": "string",
      "publicSchedule": "string",
      "shareCode": "string",
      "residencePlace": "string",
      "permanentPlace": "string",
      "userType": "string",
      "weight": "string",
      "nation": "string",
      "hobby": "string",
      "memberType": "string",
      "verifyPhoneStatus": "string",
      "friendName": "string",
      "isDeleted": "string",
      "nameCertifiedStatus": 0,
      "eduCertifiedStatus": 0,
      "jobCertifiedStatus": 0,
      "loveStatus": 0,
      "avatarUrl": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[CustomVo](#schemacustomvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_AppSettingVo">AppSettingVo</h2>

<a id="schemaappsettingvo"></a>
<a id="schema_AppSettingVo"></a>
<a id="tocSappsettingvo"></a>
<a id="tocsappsettingvo"></a>

```json
{
  "settingId": 0,
  "serviceFace": "string",
  "serviceQrCode": "string",
  "serviceWechatCode": "string",
  "groupQrCode": "string",
  "freeSingleUrl": "string",
  "paySingleUrl": "string",
  "publicPoolTitle": "string",
  "privatePoolTitle": "string",
  "freeSingleTitle": "string",
  "paySingleTitle": "string",
  "blindBoxTitle": "string",
  "noBlindBoxTitle": "string",
  "addPrivatePoolTitle": "string",
  "addPublicPoolTitle": "string",
  "visitorTitle": "string",
  "remark": "string",
  "isDeleted": "string"
}

```

app设置视图对象 t_app_setting

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|settingId|integer(int64)|false|none||自增id|
|serviceFace|string|false|none||管理员账号头像|
|serviceQrCode|string|false|none||客服微信二维码|
|serviceWechatCode|string|false|none||客服微信号|
|groupQrCode|string|false|none||群微信二维码|
|freeSingleUrl|string|false|none||免费脱单url|
|paySingleUrl|string|false|none||付费脱单url|
|publicPoolTitle|string|false|none||公域互选池标题|
|privatePoolTitle|string|false|none||私域互选池标题|
|freeSingleTitle|string|false|none||免费脱单标题|
|paySingleTitle|string|false|none||付费脱单标题|
|blindBoxTitle|string|false|none||盲盒标题|
|noBlindBoxTitle|string|false|none||非盲盒标题|
|addPrivatePoolTitle|string|false|none||增加私域标题|
|addPublicPoolTitle|string|false|none||增加公域标题|
|visitorTitle|string|false|none||访问标题|
|remark|string|false|none||备注|
|isDeleted|string|false|none||已删除(0:否 1:是)|

<h2 id="tocS_RAppSettingVo">RAppSettingVo</h2>

<a id="schemarappsettingvo"></a>
<a id="schema_RAppSettingVo"></a>
<a id="tocSrappsettingvo"></a>
<a id="tocsrappsettingvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "settingId": 0,
    "serviceFace": "string",
    "serviceQrCode": "string",
    "serviceWechatCode": "string",
    "groupQrCode": "string",
    "freeSingleUrl": "string",
    "paySingleUrl": "string",
    "publicPoolTitle": "string",
    "privatePoolTitle": "string",
    "freeSingleTitle": "string",
    "paySingleTitle": "string",
    "blindBoxTitle": "string",
    "noBlindBoxTitle": "string",
    "addPrivatePoolTitle": "string",
    "addPublicPoolTitle": "string",
    "visitorTitle": "string",
    "remark": "string",
    "isDeleted": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[AppSettingVo](#schemaappsettingvo)|false|none||app设置视图对象 t_app_setting|

<h2 id="tocS_TableDataInfoAppSettingVo">TableDataInfoAppSettingVo</h2>

<a id="schematabledatainfoappsettingvo"></a>
<a id="schema_TableDataInfoAppSettingVo"></a>
<a id="tocStabledatainfoappsettingvo"></a>
<a id="tocstabledatainfoappsettingvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "settingId": 0,
      "serviceFace": "string",
      "serviceQrCode": "string",
      "serviceWechatCode": "string",
      "groupQrCode": "string",
      "freeSingleUrl": "string",
      "paySingleUrl": "string",
      "publicPoolTitle": "string",
      "privatePoolTitle": "string",
      "freeSingleTitle": "string",
      "paySingleTitle": "string",
      "blindBoxTitle": "string",
      "noBlindBoxTitle": "string",
      "addPrivatePoolTitle": "string",
      "addPublicPoolTitle": "string",
      "visitorTitle": "string",
      "remark": "string",
      "isDeleted": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[AppSettingVo](#schemaappsettingvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_ActivityTypeVo">ActivityTypeVo</h2>

<a id="schemaactivitytypevo"></a>
<a id="schema_ActivityTypeVo"></a>
<a id="tocSactivitytypevo"></a>
<a id="tocsactivitytypevo"></a>

```json
{
  "id": 0,
  "title": "string",
  "sort": 0,
  "payModel": 0,
  "isDeleted": "string",
  "remark": "string"
}

```

活动类型视图对象 t_activity_type

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||活动类型标题|
|title|string|false|none||活动类型名|
|sort|integer(int64)|false|none||活动类型排序|
|payModel|integer(int32)|false|none||是否需要支付|
|isDeleted|string|false|none||是否删除(0:否1:是)|
|remark|string|false|none||备注|

<h2 id="tocS_RActivityTypeVo">RActivityTypeVo</h2>

<a id="schemaractivitytypevo"></a>
<a id="schema_RActivityTypeVo"></a>
<a id="tocSractivitytypevo"></a>
<a id="tocsractivitytypevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "title": "string",
    "sort": 0,
    "payModel": 0,
    "isDeleted": "string",
    "remark": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[ActivityTypeVo](#schemaactivitytypevo)|false|none||活动类型视图对象 t_activity_type|

<h2 id="tocS_TableDataInfoActivityTypeVo">TableDataInfoActivityTypeVo</h2>

<a id="schematabledatainfoactivitytypevo"></a>
<a id="schema_TableDataInfoActivityTypeVo"></a>
<a id="tocStabledatainfoactivitytypevo"></a>
<a id="tocstabledatainfoactivitytypevo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "title": "string",
      "sort": 0,
      "payModel": 0,
      "isDeleted": "string",
      "remark": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[ActivityTypeVo](#schemaactivitytypevo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_ActivityTemplateVo">ActivityTemplateVo</h2>

<a id="schemaactivitytemplatevo"></a>
<a id="schema_ActivityTemplateVo"></a>
<a id="tocSactivitytemplatevo"></a>
<a id="tocsactivitytemplatevo"></a>

```json
{
  "id": 0,
  "title": "string",
  "typeId": 0,
  "typeTitle": "string",
  "grade": "string",
  "titleImg": "string",
  "link": "string",
  "subTitle": "string",
  "maxNum": 0,
  "maxMaleNum": 0,
  "maxFemaleNum": 0,
  "address": "string",
  "detail": "string",
  "detailImg": "string",
  "beginTime": "2019-08-24T14:15:22Z",
  "endTime": "2019-08-24T14:15:22Z",
  "status": "string",
  "isSelect": "string",
  "nowNum": 0,
  "nowMaleNum": 0,
  "nowFemaleNum": 0,
  "maxChooseNum": 0,
  "briefIntroduction": "string",
  "activityCost": "string",
  "activityPrice": 0,
  "isOnline": "string",
  "activityType": "string",
  "preEnrollNum": 0,
  "activityPlatform": "string",
  "isDeleted": "string",
  "remark": "string"
}

```

活动模板视图对象 t_activity_template

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||模板id|
|title|string|false|none||活动名称|
|typeId|integer(int64)|false|none||活动类型id|
|typeTitle|string|false|none||活动类型名|
|grade|string|false|none||活动等级，数字越大优先级越高，普通活动为0|
|titleImg|string|false|none||活动封面图片|
|link|string|false|none||对应公众号链接|
|subTitle|string|false|none||副标题|
|maxNum|integer(int64)|false|none||活动最大人数,如果为0则无限大|
|maxMaleNum|integer(int64)|false|none||男生最大人数（不设置则不限制 ）|
|maxFemaleNum|integer(int64)|false|none||女生最大人数（不设置则不限制 ）|
|address|string|false|none||活动地址|
|detail|string|false|none||活动详情|
|detailImg|string|false|none||活动详情图片url|
|beginTime|string(date-time)|false|none||活动开始时间-年月日时分秒|
|endTime|string(date-time)|false|none||活动开始时间-年月日时分秒|
|status|string|false|none||活动状态：0-未开始|1-报名中|2-报名结束，活动进行中|3-活动结束|
|isSelect|string|false|none||是否开启互选 0-未开启|1-开启|2-互选结束|
|nowNum|integer(int64)|false|none||目前报名活动人数|
|nowMaleNum|integer(int64)|false|none||目前报名男生人数|
|nowFemaleNum|integer(int64)|false|none||目前报名女生人数|
|maxChooseNum|integer(int64)|false|none||个人互选上限|
|briefIntroduction|string|false|none||活动简介|
|activityCost|string|false|none||活动费用介绍|
|activityPrice|number|false|none||活动费用|
|isOnline|string|false|none||0:上线 1 下线|
|activityType|string|false|none||0 非公益 1公益|
|preEnrollNum|integer(int64)|false|none||预报名人数|
|activityPlatform|string|false|none||0 所有平台 1 h5 2 小程序|
|isDeleted|string|false|none||是否刪除(0:否 1:是)|
|remark|string|false|none||备注|

<h2 id="tocS_TableDataInfoActivityTemplateVo">TableDataInfoActivityTemplateVo</h2>

<a id="schematabledatainfoactivitytemplatevo"></a>
<a id="schema_TableDataInfoActivityTemplateVo"></a>
<a id="tocStabledatainfoactivitytemplatevo"></a>
<a id="tocstabledatainfoactivitytemplatevo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "title": "string",
      "typeId": 0,
      "typeTitle": "string",
      "grade": "string",
      "titleImg": "string",
      "link": "string",
      "subTitle": "string",
      "maxNum": 0,
      "maxMaleNum": 0,
      "maxFemaleNum": 0,
      "address": "string",
      "detail": "string",
      "detailImg": "string",
      "beginTime": "2019-08-24T14:15:22Z",
      "endTime": "2019-08-24T14:15:22Z",
      "status": "string",
      "isSelect": "string",
      "nowNum": 0,
      "nowMaleNum": 0,
      "nowFemaleNum": 0,
      "maxChooseNum": 0,
      "briefIntroduction": "string",
      "activityCost": "string",
      "activityPrice": 0,
      "isOnline": "string",
      "activityType": "string",
      "preEnrollNum": 0,
      "activityPlatform": "string",
      "isDeleted": "string",
      "remark": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[ActivityTemplateVo](#schemaactivitytemplatevo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_ActivityCustomVo">ActivityCustomVo</h2>

<a id="schemaactivitycustomvo"></a>
<a id="schema_ActivityCustomVo"></a>
<a id="tocSactivitycustomvo"></a>
<a id="tocsactivitycustomvo"></a>

```json
{
  "id": 0,
  "activityId": 0,
  "customId": 0,
  "nickName": "string",
  "status": "string",
  "enrollStatus": 0,
  "introducesId": 0,
  "activityPrice": 0,
  "timePrice": 0,
  "signStatus": "string",
  "signTime": "2019-08-24T14:15:22Z",
  "orderNo": "string",
  "remark": "string"
}

```

报名用户视图对象 t_activity_custom

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|activityId|integer(int64)|false|none||活动id|
|customId|integer(int64)|false|none||参加活动用户id|
|nickName|string|false|none||参加活动用户id|
|status|string|false|none||审核状态，0-未审核|1-审核中|2-审核通过|3-审核不通过|
|enrollStatus|integer(int32)|false|none||报名状态 0 未报名 1 已报名 2 取消报名 3 报名成功|
|introducesId|integer(int64)|false|none||活动推荐人id|
|activityPrice|number|false|none||活动价格|
|timePrice|number|false|none||守时价格|
|signStatus|string|false|none||是否签到（0未签到，1已签到）|
|signTime|string(date-time)|false|none||签到时间|
|orderNo|string|false|none||报名订单号|
|remark|string|false|none||备注|

<h2 id="tocS_RActivityCustomVo">RActivityCustomVo</h2>

<a id="schemaractivitycustomvo"></a>
<a id="schema_RActivityCustomVo"></a>
<a id="tocSractivitycustomvo"></a>
<a id="tocsractivitycustomvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "activityId": 0,
    "customId": 0,
    "nickName": "string",
    "status": "string",
    "enrollStatus": 0,
    "introducesId": 0,
    "activityPrice": 0,
    "timePrice": 0,
    "signStatus": "string",
    "signTime": "2019-08-24T14:15:22Z",
    "orderNo": "string",
    "remark": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[ActivityCustomVo](#schemaactivitycustomvo)|false|none||报名用户视图对象 t_activity_custom|

<h2 id="tocS_TableDataInfoActivityCustomVo">TableDataInfoActivityCustomVo</h2>

<a id="schematabledatainfoactivitycustomvo"></a>
<a id="schema_TableDataInfoActivityCustomVo"></a>
<a id="tocStabledatainfoactivitycustomvo"></a>
<a id="tocstabledatainfoactivitycustomvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "activityId": 0,
      "customId": 0,
      "nickName": "string",
      "status": "string",
      "enrollStatus": 0,
      "introducesId": 0,
      "activityPrice": 0,
      "timePrice": 0,
      "signStatus": "string",
      "signTime": "2019-08-24T14:15:22Z",
      "orderNo": "string",
      "remark": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[ActivityCustomVo](#schemaactivitycustomvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_ActivityVo">ActivityVo</h2>

<a id="schemaactivityvo"></a>
<a id="schema_ActivityVo"></a>
<a id="tocSactivityvo"></a>
<a id="tocsactivityvo"></a>

```json
{
  "id": 0,
  "title": "string",
  "typeId": 0,
  "grade": 0,
  "titleImg": "string",
  "link": "string",
  "subTitle": "string",
  "maxNum": 0,
  "maxMaleNum": 0,
  "maxFemaleNum": 0,
  "address": "string",
  "detail": "string",
  "detailImg": "string",
  "beginTime": "2019-08-24T14:15:22Z",
  "endTime": "2019-08-24T14:15:22Z",
  "status": "string",
  "isSelect": 0,
  "nowNum": 0,
  "nowMaleNum": 0,
  "nowFemaleNum": 0,
  "maxChooseNum": 0,
  "briefIntroduction": "string",
  "activityCost": "string",
  "activityPrice": 0,
  "isOnline": "string",
  "activityType": 0,
  "preEnrollNum": 0,
  "activityPlatform": "string",
  "typeTitle": "string",
  "enrollStatus": 0,
  "enrollStatusName": "string",
  "payStatus": 0,
  "payStatusName": "string"
}

```

活动列表视图对象 t_activity

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|title|string|false|none||活动名称|
|typeId|integer(int64)|false|none||活动类型id|
|grade|integer(int32)|false|none||活动等级，数字越大优先级越高，普通活动为0|
|titleImg|string|false|none||活动封面图片|
|link|string|false|none||对应公众号链接|
|subTitle|string|false|none||副标题|
|maxNum|integer(int64)|false|none||活动最大人数,如果为0则无限大|
|maxMaleNum|integer(int64)|false|none||男生最大人数（不设置则不限制 ）|
|maxFemaleNum|integer(int64)|false|none||女生最大人数（不设置则不限制 ）|
|address|string|false|none||活动地址|
|detail|string|false|none||活动详情|
|detailImg|string|false|none||活动详情图片url|
|beginTime|string(date-time)|false|none||活动开始时间-年月日时分秒|
|endTime|string(date-time)|false|none||活动开始时间-年月日时分秒|
|status|string|false|none||活动状态：0-未开始|1-报名中|2-报名结束，活动进行中|3-活动结束|
|isSelect|integer(int32)|false|none||是否开启互选 0-未开启|1-开启|2-互选结束|
|nowNum|integer(int64)|false|none||目前报名活动人数|
|nowMaleNum|integer(int64)|false|none||目前报名男生人数|
|nowFemaleNum|integer(int64)|false|none||目前报名女生人数|
|maxChooseNum|integer(int64)|false|none||个人互选上限|
|briefIntroduction|string|false|none||活动简介|
|activityCost|string|false|none||活动费用介绍|
|activityPrice|number|false|none||活动费用|
|isOnline|string|false|none||0:上线 1 下线|
|activityType|integer(int32)|false|none||0 非公益 1 公益|
|preEnrollNum|integer(int64)|false|none||预报名人数|
|activityPlatform|string|false|none||0 所有平台 1 h5 2 小程序|
|typeTitle|string|false|none||活动类型名|
|enrollStatus|integer(int32)|false|none||报名状态 0 未报名 1 未支付,报名中 2 已支付,报名成功  3 报名失败，全额退款|
|enrollStatusName|string|false|none||报名状态 0 未报名 1 未支付,报名中 2 已支付,报名成功  3 报名失败，全额退款|
|payStatus|integer(int32)|false|none||支付状态 0 未支付  1 已支付 2 退款|
|payStatusName|string|false|none||支付状态 0 未支付  1 已支付 2 退款|

<h2 id="tocS_TableDataInfoActivityVo">TableDataInfoActivityVo</h2>

<a id="schematabledatainfoactivityvo"></a>
<a id="schema_TableDataInfoActivityVo"></a>
<a id="tocStabledatainfoactivityvo"></a>
<a id="tocstabledatainfoactivityvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "title": "string",
      "typeId": 0,
      "grade": 0,
      "titleImg": "string",
      "link": "string",
      "subTitle": "string",
      "maxNum": 0,
      "maxMaleNum": 0,
      "maxFemaleNum": 0,
      "address": "string",
      "detail": "string",
      "detailImg": "string",
      "beginTime": "2019-08-24T14:15:22Z",
      "endTime": "2019-08-24T14:15:22Z",
      "status": "string",
      "isSelect": 0,
      "nowNum": 0,
      "nowMaleNum": 0,
      "nowFemaleNum": 0,
      "maxChooseNum": 0,
      "briefIntroduction": "string",
      "activityCost": "string",
      "activityPrice": 0,
      "isOnline": "string",
      "activityType": 0,
      "preEnrollNum": 0,
      "activityPlatform": "string",
      "typeTitle": "string",
      "enrollStatus": 0,
      "enrollStatusName": "string",
      "payStatus": 0,
      "payStatusName": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[ActivityVo](#schemaactivityvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_TableDataInfoSysUser">TableDataInfoSysUser</h2>

<a id="schematabledatainfosysuser"></a>
<a id="schema_TableDataInfoSysUser"></a>
<a id="tocStabledatainfosysuser"></a>
<a id="tocstabledatainfosysuser"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "userId": 0,
      "deptId": 0,
      "userName": "string",
      "nickName": "string",
      "userType": "string",
      "email": "string",
      "phonenumber": "string",
      "sex": "string",
      "avatar": "string",
      "password": "string",
      "status": "string",
      "delFlag": "string",
      "loginIp": "string",
      "loginDate": "2019-08-24T14:15:22Z",
      "remark": "string",
      "dept": {
        "createBy": "string",
        "createTime": "2019-08-24T14:15:22Z",
        "updateBy": "string",
        "updateTime": "2019-08-24T14:15:22Z",
        "params": {
          "property1": {},
          "property2": {}
        },
        "parentName": "string",
        "parentId": 0,
        "children": [
          {
            "createBy": null,
            "createTime": null,
            "updateBy": null,
            "updateTime": null,
            "params": null,
            "parentName": null,
            "parentId": null,
            "children": null,
            "deptId": null,
            "deptName": null,
            "orderNum": null,
            "leader": null,
            "phone": null,
            "email": null,
            "status": null,
            "delFlag": null,
            "ancestors": null
          }
        ],
        "deptId": 0,
        "deptName": "string",
        "orderNum": 0,
        "leader": "string",
        "phone": "string",
        "email": "string",
        "status": "string",
        "delFlag": "string",
        "ancestors": "string"
      },
      "roles": [
        {
          "createBy": "string",
          "createTime": "2019-08-24T14:15:22Z",
          "updateBy": "string",
          "updateTime": "2019-08-24T14:15:22Z",
          "params": {
            "property1": {},
            "property2": {}
          },
          "roleId": 0,
          "roleName": "string",
          "roleKey": "string",
          "roleSort": 0,
          "dataScope": "string",
          "menuCheckStrictly": true,
          "deptCheckStrictly": true,
          "status": "string",
          "delFlag": "string",
          "remark": "string",
          "flag": true,
          "menuIds": [
            0
          ],
          "deptIds": [
            0
          ],
          "admin": true
        }
      ],
      "roleIds": [
        0
      ],
      "postIds": [
        0
      ],
      "roleId": 0,
      "admin": true
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[SysUser](#schemasysuser)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RListTreeLong">RListTreeLong</h2>

<a id="schemarlisttreelong"></a>
<a id="schema_RListTreeLong"></a>
<a id="tocSrlisttreelong"></a>
<a id="tocsrlisttreelong"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "config": {
        "idKey": "string",
        "parentIdKey": "string",
        "weightKey": "string",
        "nameKey": "string",
        "childrenKey": "string",
        "deep": 0
      },
      "parentId": 0,
      "id": 0,
      "weight": {},
      "name": {},
      "empty": true,
      "property1": {},
      "property2": {}
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[TreeLong](#schematreelong)]|false|none||none|

<h2 id="tocS_TreeLong">TreeLong</h2>

<a id="schematreelong"></a>
<a id="schema_TreeLong"></a>
<a id="tocStreelong"></a>
<a id="tocstreelong"></a>

```json
{
  "config": {
    "idKey": "string",
    "parentIdKey": "string",
    "weightKey": "string",
    "nameKey": "string",
    "childrenKey": "string",
    "deep": 0
  },
  "parentId": 0,
  "id": 0,
  "weight": {},
  "name": {},
  "empty": true,
  "property1": {},
  "property2": {}
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|**additionalProperties**|object|false|none||none|
|config|[TreeNodeConfig](#schematreenodeconfig)|false|none||none|
|parentId|integer(int64)|false|none||none|
|id|integer(int64)|false|none||none|
|weight|object|false|none||none|
|name|object|false|none||none|
|empty|boolean|false|none||none|

<h2 id="tocS_TreeNodeConfig">TreeNodeConfig</h2>

<a id="schematreenodeconfig"></a>
<a id="schema_TreeNodeConfig"></a>
<a id="tocStreenodeconfig"></a>
<a id="tocstreenodeconfig"></a>

```json
{
  "idKey": "string",
  "parentIdKey": "string",
  "weightKey": "string",
  "nameKey": "string",
  "childrenKey": "string",
  "deep": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|idKey|string|false|none||none|
|parentIdKey|string|false|none||none|
|weightKey|string|false|none||none|
|nameKey|string|false|none||none|
|childrenKey|string|false|none||none|
|deep|integer(int32)|false|none||none|

<h2 id="tocS_RSysRole">RSysRole</h2>

<a id="schemarsysrole"></a>
<a id="schema_RSysRole"></a>
<a id="tocSrsysrole"></a>
<a id="tocsrsysrole"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "createBy": "string",
    "createTime": "2019-08-24T14:15:22Z",
    "updateBy": "string",
    "updateTime": "2019-08-24T14:15:22Z",
    "params": {
      "property1": {},
      "property2": {}
    },
    "roleId": 0,
    "roleName": "string",
    "roleKey": "string",
    "roleSort": 0,
    "dataScope": "string",
    "menuCheckStrictly": true,
    "deptCheckStrictly": true,
    "status": "string",
    "delFlag": "string",
    "remark": "string",
    "flag": true,
    "menuIds": [
      0
    ],
    "deptIds": [
      0
    ],
    "admin": true
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[SysRole](#schemasysrole)|false|none||角色表 sys_role|

<h2 id="tocS_RListSysRole">RListSysRole</h2>

<a id="schemarlistsysrole"></a>
<a id="schema_RListSysRole"></a>
<a id="tocSrlistsysrole"></a>
<a id="tocsrlistsysrole"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "roleId": 0,
      "roleName": "string",
      "roleKey": "string",
      "roleSort": 0,
      "dataScope": "string",
      "menuCheckStrictly": true,
      "deptCheckStrictly": true,
      "status": "string",
      "delFlag": "string",
      "remark": "string",
      "flag": true,
      "menuIds": [
        0
      ],
      "deptIds": [
        0
      ],
      "admin": true
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[SysRole](#schemasysrole)]|false|none||[角色表 sys_role]|

<h2 id="tocS_TableDataInfoSysRole">TableDataInfoSysRole</h2>

<a id="schematabledatainfosysrole"></a>
<a id="schema_TableDataInfoSysRole"></a>
<a id="tocStabledatainfosysrole"></a>
<a id="tocstabledatainfosysrole"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "roleId": 0,
      "roleName": "string",
      "roleKey": "string",
      "roleSort": 0,
      "dataScope": "string",
      "menuCheckStrictly": true,
      "deptCheckStrictly": true,
      "status": "string",
      "delFlag": "string",
      "remark": "string",
      "flag": true,
      "menuIds": [
        0
      ],
      "deptIds": [
        0
      ],
      "admin": true
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[SysRole](#schemasysrole)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RSysPost">RSysPost</h2>

<a id="schemarsyspost"></a>
<a id="schema_RSysPost"></a>
<a id="tocSrsyspost"></a>
<a id="tocsrsyspost"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "createBy": "string",
    "createTime": "2019-08-24T14:15:22Z",
    "updateBy": "string",
    "updateTime": "2019-08-24T14:15:22Z",
    "params": {
      "property1": {},
      "property2": {}
    },
    "postId": 0,
    "postCode": "string",
    "postName": "string",
    "postSort": 0,
    "status": "string",
    "remark": "string",
    "flag": true
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[SysPost](#schemasyspost)|false|none||岗位表 sys_post|

<h2 id="tocS_RListSysPost">RListSysPost</h2>

<a id="schemarlistsyspost"></a>
<a id="schema_RListSysPost"></a>
<a id="tocSrlistsyspost"></a>
<a id="tocsrlistsyspost"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "postId": 0,
      "postCode": "string",
      "postName": "string",
      "postSort": 0,
      "status": "string",
      "remark": "string",
      "flag": true
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[SysPost](#schemasyspost)]|false|none||[岗位表 sys_post]|

<h2 id="tocS_TableDataInfoSysPost">TableDataInfoSysPost</h2>

<a id="schematabledatainfosyspost"></a>
<a id="schema_TableDataInfoSysPost"></a>
<a id="tocStabledatainfosyspost"></a>
<a id="tocstabledatainfosyspost"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "postId": 0,
      "postCode": "string",
      "postName": "string",
      "postSort": 0,
      "status": "string",
      "remark": "string",
      "flag": true
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[SysPost](#schemasyspost)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_SysOssBo">SysOssBo</h2>

<a id="schemasysossbo"></a>
<a id="schema_SysOssBo"></a>
<a id="tocSsysossbo"></a>
<a id="tocssysossbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "ossId": 0,
  "fileName": "string",
  "originalName": "string",
  "fileSuffix": "string",
  "url": "string",
  "service": "string"
}

```

OSS对象存储分页查询对象 sys_oss

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|ossId|integer(int64)|false|none||ossId|
|fileName|string(string)|false|none||文件名|
|originalName|string(string)|false|none||原名|
|fileSuffix|string(string)|false|none||文件后缀名|
|url|string(string)|false|none||URL地址|
|service|string(string)|false|none||服务商|

<h2 id="tocS_SysOssVo">SysOssVo</h2>

<a id="schemasysossvo"></a>
<a id="schema_SysOssVo"></a>
<a id="tocSsysossvo"></a>
<a id="tocssysossvo"></a>

```json
{
  "ossId": 0,
  "fileName": "string",
  "originalName": "string",
  "fileSuffix": "string",
  "url": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "createBy": "string",
  "service": "string"
}

```

OSS对象存储视图对象 sys_oss

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|ossId|integer(int64)|false|none||对象存储主键|
|fileName|string|false|none||文件名|
|originalName|string|false|none||原名|
|fileSuffix|string|false|none||文件后缀名|
|url|string|false|none||URL地址|
|createTime|string(date-time)|false|none||创建时间|
|createBy|string|false|none||上传人|
|service|string|false|none||服务商|

<h2 id="tocS_TableDataInfoSysOssVo">TableDataInfoSysOssVo</h2>

<a id="schematabledatainfosysossvo"></a>
<a id="schema_TableDataInfoSysOssVo"></a>
<a id="tocStabledatainfosysossvo"></a>
<a id="tocstabledatainfosysossvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "ossId": 0,
      "fileName": "string",
      "originalName": "string",
      "fileSuffix": "string",
      "url": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "createBy": "string",
      "service": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[SysOssVo](#schemasysossvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RListSysOssVo">RListSysOssVo</h2>

<a id="schemarlistsysossvo"></a>
<a id="schema_RListSysOssVo"></a>
<a id="tocSrlistsysossvo"></a>
<a id="tocsrlistsysossvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "ossId": 0,
      "fileName": "string",
      "originalName": "string",
      "fileSuffix": "string",
      "url": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "createBy": "string",
      "service": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[SysOssVo](#schemasysossvo)]|false|none||[OSS对象存储视图对象 sys_oss]|

<h2 id="tocS_RSysOssConfigVo">RSysOssConfigVo</h2>

<a id="schemarsysossconfigvo"></a>
<a id="schema_RSysOssConfigVo"></a>
<a id="tocSrsysossconfigvo"></a>
<a id="tocsrsysossconfigvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "ossConfigId": 0,
    "configKey": "string",
    "accessKey": "string",
    "secretKey": "string",
    "bucketName": "string",
    "prefix": "string",
    "endpoint": "string",
    "domain": "string",
    "isHttps": "string",
    "region": "string",
    "status": "string",
    "ext1": "string",
    "remark": "string",
    "accessPolicy": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[SysOssConfigVo](#schemasysossconfigvo)|false|none||对象存储配置视图对象 sys_oss_config|

<h2 id="tocS_SysOssConfigVo">SysOssConfigVo</h2>

<a id="schemasysossconfigvo"></a>
<a id="schema_SysOssConfigVo"></a>
<a id="tocSsysossconfigvo"></a>
<a id="tocssysossconfigvo"></a>

```json
{
  "ossConfigId": 0,
  "configKey": "string",
  "accessKey": "string",
  "secretKey": "string",
  "bucketName": "string",
  "prefix": "string",
  "endpoint": "string",
  "domain": "string",
  "isHttps": "string",
  "region": "string",
  "status": "string",
  "ext1": "string",
  "remark": "string",
  "accessPolicy": "string"
}

```

对象存储配置视图对象 sys_oss_config

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|ossConfigId|integer(int64)|false|none||主建|
|configKey|string|false|none||配置key|
|accessKey|string|false|none||accessKey|
|secretKey|string|false|none||秘钥|
|bucketName|string|false|none||桶名称|
|prefix|string|false|none||前缀|
|endpoint|string|false|none||访问站点|
|domain|string|false|none||自定义域名|
|isHttps|string|false|none||是否https（Y=是,N=否）|
|region|string|false|none||域|
|status|string|false|none||是否默认（0=是,1=否）|
|ext1|string|false|none||扩展字段|
|remark|string|false|none||备注|
|accessPolicy|string|false|none||桶权限类型(0private 1public 2custom)|

<h2 id="tocS_TableDataInfoSysOssConfigVo">TableDataInfoSysOssConfigVo</h2>

<a id="schematabledatainfosysossconfigvo"></a>
<a id="schema_TableDataInfoSysOssConfigVo"></a>
<a id="tocStabledatainfosysossconfigvo"></a>
<a id="tocstabledatainfosysossconfigvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "ossConfigId": 0,
      "configKey": "string",
      "accessKey": "string",
      "secretKey": "string",
      "bucketName": "string",
      "prefix": "string",
      "endpoint": "string",
      "domain": "string",
      "isHttps": "string",
      "region": "string",
      "status": "string",
      "ext1": "string",
      "remark": "string",
      "accessPolicy": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[SysOssConfigVo](#schemasysossconfigvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RSysNotice">RSysNotice</h2>

<a id="schemarsysnotice"></a>
<a id="schema_RSysNotice"></a>
<a id="tocSrsysnotice"></a>
<a id="tocsrsysnotice"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "createBy": "string",
    "createTime": "2019-08-24T14:15:22Z",
    "updateBy": "string",
    "updateTime": "2019-08-24T14:15:22Z",
    "params": {
      "property1": {},
      "property2": {}
    },
    "noticeId": 0,
    "noticeTitle": "string",
    "noticeType": "string",
    "noticeContent": "string",
    "status": "string",
    "remark": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[SysNotice](#schemasysnotice)|false|none||通知公告表 sys_notice|

<h2 id="tocS_TableDataInfoSysNotice">TableDataInfoSysNotice</h2>

<a id="schematabledatainfosysnotice"></a>
<a id="schema_TableDataInfoSysNotice"></a>
<a id="tocStabledatainfosysnotice"></a>
<a id="tocstabledatainfosysnotice"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "noticeId": 0,
      "noticeTitle": "string",
      "noticeType": "string",
      "noticeContent": "string",
      "status": "string",
      "remark": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[SysNotice](#schemasysnotice)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RSysMenu">RSysMenu</h2>

<a id="schemarsysmenu"></a>
<a id="schema_RSysMenu"></a>
<a id="tocSrsysmenu"></a>
<a id="tocsrsysmenu"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "createBy": "string",
    "createTime": "2019-08-24T14:15:22Z",
    "updateBy": "string",
    "updateTime": "2019-08-24T14:15:22Z",
    "params": {
      "property1": {},
      "property2": {}
    },
    "parentName": "string",
    "parentId": 0,
    "children": [
      {
        "createBy": "string",
        "createTime": "2019-08-24T14:15:22Z",
        "updateBy": "string",
        "updateTime": "2019-08-24T14:15:22Z",
        "params": {
          "property1": {},
          "property2": {}
        },
        "parentName": "string",
        "parentId": 0,
        "children": [
          {
            "createBy": null,
            "createTime": null,
            "updateBy": null,
            "updateTime": null,
            "params": null,
            "parentName": null,
            "parentId": null,
            "children": null,
            "menuId": null,
            "menuName": null,
            "orderNum": null,
            "path": null,
            "component": null,
            "queryParam": null,
            "isFrame": null,
            "isCache": null,
            "menuType": null,
            "visible": null,
            "status": null,
            "perms": null,
            "icon": null,
            "remark": null
          }
        ],
        "menuId": 0,
        "menuName": "string",
        "orderNum": 0,
        "path": "string",
        "component": "string",
        "queryParam": "string",
        "isFrame": "string",
        "isCache": "string",
        "menuType": "string",
        "visible": "string",
        "status": "string",
        "perms": "string",
        "icon": "string",
        "remark": "string"
      }
    ],
    "menuId": 0,
    "menuName": "string",
    "orderNum": 0,
    "path": "string",
    "component": "string",
    "queryParam": "string",
    "isFrame": "string",
    "isCache": "string",
    "menuType": "string",
    "visible": "string",
    "status": "string",
    "perms": "string",
    "icon": "string",
    "remark": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[SysMenu](#schemasysmenu)|false|none||菜单权限表 sys_menu|

<h2 id="tocS_RListSysMenu">RListSysMenu</h2>

<a id="schemarlistsysmenu"></a>
<a id="schema_RListSysMenu"></a>
<a id="tocSrlistsysmenu"></a>
<a id="tocsrlistsysmenu"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "parentName": "string",
      "parentId": 0,
      "children": [
        {
          "createBy": "string",
          "createTime": "2019-08-24T14:15:22Z",
          "updateBy": "string",
          "updateTime": "2019-08-24T14:15:22Z",
          "params": {
            "property1": {},
            "property2": {}
          },
          "parentName": "string",
          "parentId": 0,
          "children": [
            {}
          ],
          "menuId": 0,
          "menuName": "string",
          "orderNum": 0,
          "path": "string",
          "component": "string",
          "queryParam": "string",
          "isFrame": "string",
          "isCache": "string",
          "menuType": "string",
          "visible": "string",
          "status": "string",
          "perms": "string",
          "icon": "string",
          "remark": "string"
        }
      ],
      "menuId": 0,
      "menuName": "string",
      "orderNum": 0,
      "path": "string",
      "component": "string",
      "queryParam": "string",
      "isFrame": "string",
      "isCache": "string",
      "menuType": "string",
      "visible": "string",
      "status": "string",
      "perms": "string",
      "icon": "string",
      "remark": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[SysMenu](#schemasysmenu)]|false|none||[菜单权限表 sys_menu]|

<h2 id="tocS_RSysDictType">RSysDictType</h2>

<a id="schemarsysdicttype"></a>
<a id="schema_RSysDictType"></a>
<a id="tocSrsysdicttype"></a>
<a id="tocsrsysdicttype"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "createBy": "string",
    "createTime": "2019-08-24T14:15:22Z",
    "updateBy": "string",
    "updateTime": "2019-08-24T14:15:22Z",
    "params": {
      "property1": {},
      "property2": {}
    },
    "dictId": 0,
    "dictName": "string",
    "dictType": "string",
    "status": "string",
    "remark": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[SysDictType](#schemasysdicttype)|false|none||字典类型表 sys_dict_type|

<h2 id="tocS_RListSysDictType">RListSysDictType</h2>

<a id="schemarlistsysdicttype"></a>
<a id="schema_RListSysDictType"></a>
<a id="tocSrlistsysdicttype"></a>
<a id="tocsrlistsysdicttype"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "dictId": 0,
      "dictName": "string",
      "dictType": "string",
      "status": "string",
      "remark": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[SysDictType](#schemasysdicttype)]|false|none||[字典类型表 sys_dict_type]|

<h2 id="tocS_TableDataInfoSysDictType">TableDataInfoSysDictType</h2>

<a id="schematabledatainfosysdicttype"></a>
<a id="schema_TableDataInfoSysDictType"></a>
<a id="tocStabledatainfosysdicttype"></a>
<a id="tocstabledatainfosysdicttype"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "dictId": 0,
      "dictName": "string",
      "dictType": "string",
      "status": "string",
      "remark": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[SysDictType](#schemasysdicttype)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RSysDictData">RSysDictData</h2>

<a id="schemarsysdictdata"></a>
<a id="schema_RSysDictData"></a>
<a id="tocSrsysdictdata"></a>
<a id="tocsrsysdictdata"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "createBy": "string",
    "createTime": "2019-08-24T14:15:22Z",
    "updateBy": "string",
    "updateTime": "2019-08-24T14:15:22Z",
    "params": {
      "property1": {},
      "property2": {}
    },
    "dictCode": 0,
    "dictSort": 0,
    "dictLabel": "string",
    "dictValue": "string",
    "dictType": "string",
    "cssClass": "string",
    "listClass": "string",
    "isDefault": "string",
    "status": "string",
    "remark": "string",
    "default": true
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[SysDictData](#schemasysdictdata)|false|none||字典数据表 sys_dict_data|

<h2 id="tocS_RListSysDictData">RListSysDictData</h2>

<a id="schemarlistsysdictdata"></a>
<a id="schema_RListSysDictData"></a>
<a id="tocSrlistsysdictdata"></a>
<a id="tocsrlistsysdictdata"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "dictCode": 0,
      "dictSort": 0,
      "dictLabel": "string",
      "dictValue": "string",
      "dictType": "string",
      "cssClass": "string",
      "listClass": "string",
      "isDefault": "string",
      "status": "string",
      "remark": "string",
      "default": true
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[SysDictData](#schemasysdictdata)]|false|none||[字典数据表 sys_dict_data]|

<h2 id="tocS_TableDataInfoSysDictData">TableDataInfoSysDictData</h2>

<a id="schematabledatainfosysdictdata"></a>
<a id="schema_TableDataInfoSysDictData"></a>
<a id="tocStabledatainfosysdictdata"></a>
<a id="tocstabledatainfosysdictdata"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "dictCode": 0,
      "dictSort": 0,
      "dictLabel": "string",
      "dictValue": "string",
      "dictType": "string",
      "cssClass": "string",
      "listClass": "string",
      "isDefault": "string",
      "status": "string",
      "remark": "string",
      "default": true
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[SysDictData](#schemasysdictdata)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RSysDept">RSysDept</h2>

<a id="schemarsysdept"></a>
<a id="schema_RSysDept"></a>
<a id="tocSrsysdept"></a>
<a id="tocsrsysdept"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "createBy": "string",
    "createTime": "2019-08-24T14:15:22Z",
    "updateBy": "string",
    "updateTime": "2019-08-24T14:15:22Z",
    "params": {
      "property1": {},
      "property2": {}
    },
    "parentName": "string",
    "parentId": 0,
    "children": [
      {
        "createBy": "string",
        "createTime": "2019-08-24T14:15:22Z",
        "updateBy": "string",
        "updateTime": "2019-08-24T14:15:22Z",
        "params": {
          "property1": {},
          "property2": {}
        },
        "parentName": "string",
        "parentId": 0,
        "children": [
          {
            "createBy": null,
            "createTime": null,
            "updateBy": null,
            "updateTime": null,
            "params": null,
            "parentName": null,
            "parentId": null,
            "children": null,
            "deptId": null,
            "deptName": null,
            "orderNum": null,
            "leader": null,
            "phone": null,
            "email": null,
            "status": null,
            "delFlag": null,
            "ancestors": null
          }
        ],
        "deptId": 0,
        "deptName": "string",
        "orderNum": 0,
        "leader": "string",
        "phone": "string",
        "email": "string",
        "status": "string",
        "delFlag": "string",
        "ancestors": "string"
      }
    ],
    "deptId": 0,
    "deptName": "string",
    "orderNum": 0,
    "leader": "string",
    "phone": "string",
    "email": "string",
    "status": "string",
    "delFlag": "string",
    "ancestors": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[SysDept](#schemasysdept)|false|none||部门表 sys_dept|

<h2 id="tocS_RListSysDept">RListSysDept</h2>

<a id="schemarlistsysdept"></a>
<a id="schema_RListSysDept"></a>
<a id="tocSrlistsysdept"></a>
<a id="tocsrlistsysdept"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "parentName": "string",
      "parentId": 0,
      "children": [
        {
          "createBy": "string",
          "createTime": "2019-08-24T14:15:22Z",
          "updateBy": "string",
          "updateTime": "2019-08-24T14:15:22Z",
          "params": {
            "property1": {},
            "property2": {}
          },
          "parentName": "string",
          "parentId": 0,
          "children": [
            {}
          ],
          "deptId": 0,
          "deptName": "string",
          "orderNum": 0,
          "leader": "string",
          "phone": "string",
          "email": "string",
          "status": "string",
          "delFlag": "string",
          "ancestors": "string"
        }
      ],
      "deptId": 0,
      "deptName": "string",
      "orderNum": 0,
      "leader": "string",
      "phone": "string",
      "email": "string",
      "status": "string",
      "delFlag": "string",
      "ancestors": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[SysDept](#schemasysdept)]|false|none||[部门表 sys_dept]|

<h2 id="tocS_RSysConfig">RSysConfig</h2>

<a id="schemarsysconfig"></a>
<a id="schema_RSysConfig"></a>
<a id="tocSrsysconfig"></a>
<a id="tocsrsysconfig"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "createBy": "string",
    "createTime": "2019-08-24T14:15:22Z",
    "updateBy": "string",
    "updateTime": "2019-08-24T14:15:22Z",
    "params": {
      "property1": {},
      "property2": {}
    },
    "configId": 0,
    "configName": "string",
    "configKey": "string",
    "configValue": "string",
    "configType": "string",
    "remark": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[SysConfig](#schemasysconfig)|false|none||参数配置表 sys_config|

<h2 id="tocS_TableDataInfoSysConfig">TableDataInfoSysConfig</h2>

<a id="schematabledatainfosysconfig"></a>
<a id="schema_TableDataInfoSysConfig"></a>
<a id="tocStabledatainfosysconfig"></a>
<a id="tocstabledatainfosysconfig"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "configId": 0,
      "configName": "string",
      "configKey": "string",
      "configValue": "string",
      "configType": "string",
      "remark": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[SysConfig](#schemasysconfig)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_TableDataInfoSysOperLog">TableDataInfoSysOperLog</h2>

<a id="schematabledatainfosysoperlog"></a>
<a id="schema_TableDataInfoSysOperLog"></a>
<a id="tocStabledatainfosysoperlog"></a>
<a id="tocstabledatainfosysoperlog"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "operId": 0,
      "title": "string",
      "businessType": 0,
      "businessTypes": [
        0
      ],
      "method": "string",
      "requestMethod": "string",
      "operatorType": 0,
      "operName": "string",
      "deptName": "string",
      "operUrl": "string",
      "operIp": "string",
      "operLocation": "string",
      "operParam": "string",
      "jsonResult": "string",
      "status": 0,
      "errorMsg": "string",
      "operTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      }
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[SysOperLog](#schemasysoperlog)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_SysUserOnline">SysUserOnline</h2>

<a id="schemasysuseronline"></a>
<a id="schema_SysUserOnline"></a>
<a id="tocSsysuseronline"></a>
<a id="tocssysuseronline"></a>

```json
{
  "tokenId": "string",
  "deptName": "string",
  "userName": "string",
  "ipaddr": "string",
  "loginLocation": "string",
  "browser": "string",
  "os": "string",
  "loginTime": 0
}

```

当前在线会话

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|tokenId|string|false|none||会话编号|
|deptName|string|false|none||部门名称|
|userName|string|false|none||用户名称|
|ipaddr|string|false|none||登录IP地址|
|loginLocation|string|false|none||登录地址|
|browser|string|false|none||浏览器类型|
|os|string|false|none||操作系统|
|loginTime|integer(int64)|false|none||登录时间|

<h2 id="tocS_TableDataInfoSysUserOnline">TableDataInfoSysUserOnline</h2>

<a id="schematabledatainfosysuseronline"></a>
<a id="schema_TableDataInfoSysUserOnline"></a>
<a id="tocStabledatainfosysuseronline"></a>
<a id="tocstabledatainfosysuseronline"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "tokenId": "string",
      "deptName": "string",
      "userName": "string",
      "ipaddr": "string",
      "loginLocation": "string",
      "browser": "string",
      "os": "string",
      "loginTime": 0
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[SysUserOnline](#schemasysuseronline)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_TableDataInfoSysLogininfor">TableDataInfoSysLogininfor</h2>

<a id="schematabledatainfosyslogininfor"></a>
<a id="schema_TableDataInfoSysLogininfor"></a>
<a id="tocStabledatainfosyslogininfor"></a>
<a id="tocstabledatainfosyslogininfor"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "infoId": 0,
      "userName": "string",
      "status": "string",
      "ipaddr": "string",
      "loginLocation": "string",
      "browser": "string",
      "os": "string",
      "msg": "string",
      "loginTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      }
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[SysLogininfor](#schemasyslogininfor)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RSysCache">RSysCache</h2>

<a id="schemarsyscache"></a>
<a id="schema_RSysCache"></a>
<a id="tocSrsyscache"></a>
<a id="tocsrsyscache"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "cacheName": "string",
    "cacheKey": "string",
    "cacheValue": "string",
    "remark": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[SysCache](#schemasyscache)|false|none||缓存信息|

<h2 id="tocS_SysCache">SysCache</h2>

<a id="schemasyscache"></a>
<a id="schema_SysCache"></a>
<a id="tocSsyscache"></a>
<a id="tocssyscache"></a>

```json
{
  "cacheName": "string",
  "cacheKey": "string",
  "cacheValue": "string",
  "remark": "string"
}

```

缓存信息

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|cacheName|string|false|none||缓存名称|
|cacheKey|string|false|none||缓存键名|
|cacheValue|string|false|none||缓存内容|
|remark|string|false|none||备注|

<h2 id="tocS_RListSysCache">RListSysCache</h2>

<a id="schemarlistsyscache"></a>
<a id="schema_RListSysCache"></a>
<a id="tocSrlistsyscache"></a>
<a id="tocsrlistsyscache"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "cacheName": "string",
      "cacheKey": "string",
      "cacheValue": "string",
      "remark": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[SysCache](#schemasyscache)]|false|none||[缓存信息]|

<h2 id="tocS_RCollectionString">RCollectionString</h2>

<a id="schemarcollectionstring"></a>
<a id="schema_RCollectionString"></a>
<a id="tocSrcollectionstring"></a>
<a id="tocsrcollectionstring"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    "string"
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[string]|false|none||none|

<h2 id="tocS_MetaVo">MetaVo</h2>

<a id="schemametavo"></a>
<a id="schema_MetaVo"></a>
<a id="tocSmetavo"></a>
<a id="tocsmetavo"></a>

```json
{
  "title": "string",
  "icon": "string",
  "noCache": true,
  "link": "string"
}

```

路由显示信息

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|title|string|false|none||设置该路由在侧边栏和面包屑中展示的名字|
|icon|string|false|none||设置该路由的图标，对应路径src/assets/icons/svg|
|noCache|boolean|false|none||设置为true，则不会被 <keep-alive>缓存|
|link|string|false|none||内链地址（http(s)://开头）|

<h2 id="tocS_RListRouterVo">RListRouterVo</h2>

<a id="schemarlistroutervo"></a>
<a id="schema_RListRouterVo"></a>
<a id="tocSrlistroutervo"></a>
<a id="tocsrlistroutervo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "name": "string",
      "path": "string",
      "hidden": true,
      "redirect": "string",
      "component": "string",
      "query": "string",
      "alwaysShow": true,
      "meta": {
        "title": "string",
        "icon": "string",
        "noCache": true,
        "link": "string"
      }
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[RouterVo](#schemaroutervo)]|false|none||[路由配置信息]|

<h2 id="tocS_RouterVo">RouterVo</h2>

<a id="schemaroutervo"></a>
<a id="schema_RouterVo"></a>
<a id="tocSroutervo"></a>
<a id="tocsroutervo"></a>

```json
{
  "name": "string",
  "path": "string",
  "hidden": true,
  "redirect": "string",
  "component": "string",
  "query": "string",
  "alwaysShow": true,
  "meta": {
    "title": "string",
    "icon": "string",
    "noCache": true,
    "link": "string"
  }
}

```

路由配置信息

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|name|string|false|none||路由名字|
|path|string|false|none||路由地址|
|hidden|boolean|false|none||是否隐藏路由，当设置 true 的时候该路由不会再侧边栏出现|
|redirect|string|false|none||重定向地址，当设置 noRedirect 的时候该路由在面包屑导航中不可被点击|
|component|string|false|none||组件地址|
|query|string|false|none||路由参数：如 {"id": 1, "name": "ry"}|
|alwaysShow|boolean|false|none||当你一个路由下面的 children 声明的路由大于1个时，自动会变成嵌套的模式--如组件页面|
|meta|[MetaVo](#schemametavo)|false|none||路由显示信息|

<h2 id="tocS_RTestTreeVo">RTestTreeVo</h2>

<a id="schemartesttreevo"></a>
<a id="schema_RTestTreeVo"></a>
<a id="tocSrtesttreevo"></a>
<a id="tocsrtesttreevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "parentId": 0,
    "deptId": 0,
    "userId": 0,
    "treeName": "string",
    "createTime": "2019-08-24T14:15:22Z"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[TestTreeVo](#schematesttreevo)|false|none||测试树表视图对象 test_tree|

<h2 id="tocS_TestTreeVo">TestTreeVo</h2>

<a id="schematesttreevo"></a>
<a id="schema_TestTreeVo"></a>
<a id="tocStesttreevo"></a>
<a id="tocstesttreevo"></a>

```json
{
  "id": 0,
  "parentId": 0,
  "deptId": 0,
  "userId": 0,
  "treeName": "string",
  "createTime": "2019-08-24T14:15:22Z"
}

```

测试树表视图对象 test_tree

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||主键|
|parentId|integer(int64)|false|none||父id|
|deptId|integer(int64)|false|none||部门id|
|userId|integer(int64)|false|none||用户id|
|treeName|string|false|none||树节点名|
|createTime|string(date-time)|false|none||创建时间|

<h2 id="tocS_RListTestTreeVo">RListTestTreeVo</h2>

<a id="schemarlisttesttreevo"></a>
<a id="schema_RListTestTreeVo"></a>
<a id="tocSrlisttesttreevo"></a>
<a id="tocsrlisttesttreevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "id": 0,
      "parentId": 0,
      "deptId": 0,
      "userId": 0,
      "treeName": "string",
      "createTime": "2019-08-24T14:15:22Z"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[TestTreeVo](#schematesttreevo)]|false|none||[测试树表视图对象 test_tree]|

<h2 id="tocS_RObject">RObject</h2>

<a id="schemarobject"></a>
<a id="schema_RObject"></a>
<a id="tocSrobject"></a>
<a id="tocsrobject"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {}
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|object|false|none||none|

<h2 id="tocS_RTestSensitive">RTestSensitive</h2>

<a id="schemartestsensitive"></a>
<a id="schema_RTestSensitive"></a>
<a id="tocSrtestsensitive"></a>
<a id="tocsrtestsensitive"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "idCard": "string",
    "phone": "string",
    "address": "string",
    "email": "string",
    "bankCard": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[TestSensitive](#schematestsensitive)|false|none||none|

<h2 id="tocS_TestSensitive">TestSensitive</h2>

<a id="schematestsensitive"></a>
<a id="schema_TestSensitive"></a>
<a id="tocStestsensitive"></a>
<a id="tocstestsensitive"></a>

```json
{
  "idCard": "string",
  "phone": "string",
  "address": "string",
  "email": "string",
  "bankCard": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|idCard|string|false|none||身份证|
|phone|string|false|none||电话|
|address|string|false|none||地址|
|email|string|false|none||邮箱|
|bankCard|string|false|none||银行卡|

<h2 id="tocS_TestI18nBo">TestI18nBo</h2>

<a id="schematesti18nbo"></a>
<a id="schema_TestI18nBo"></a>
<a id="tocStesti18nbo"></a>
<a id="tocstesti18nbo"></a>

```json
{
  "name": "string",
  "age": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|name|string(string)|true|none||none|
|age|integer(int32)|true|none||none|

<h2 id="tocS_RTestI18nBo">RTestI18nBo</h2>

<a id="schemartesti18nbo"></a>
<a id="schema_RTestI18nBo"></a>
<a id="tocSrtesti18nbo"></a>
<a id="tocsrtesti18nbo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "name": "string",
    "age": 0
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[TestI18nBo](#schematesti18nbo)|false|none||none|

<h2 id="tocS_RMapStringTestDemoEncrypt">RMapStringTestDemoEncrypt</h2>

<a id="schemarmapstringtestdemoencrypt"></a>
<a id="schema_RMapStringTestDemoEncrypt"></a>
<a id="tocSrmapstringtestdemoencrypt"></a>
<a id="tocsrmapstringtestdemoencrypt"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "property1": {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "id": 0,
      "deptId": 0,
      "userId": 0,
      "orderNum": 0,
      "testKey": "string",
      "value": "string",
      "version": 0,
      "delFlag": 0
    },
    "property2": {
      "createBy": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "updateBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "params": {
        "property1": {},
        "property2": {}
      },
      "id": 0,
      "deptId": 0,
      "userId": 0,
      "orderNum": 0,
      "testKey": "string",
      "value": "string",
      "version": 0,
      "delFlag": 0
    }
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|object|false|none||none|
|» **additionalProperties**|[TestDemoEncrypt](#schematestdemoencrypt)|false|none||none|

<h2 id="tocS_TestDemoEncrypt">TestDemoEncrypt</h2>

<a id="schematestdemoencrypt"></a>
<a id="schema_TestDemoEncrypt"></a>
<a id="tocStestdemoencrypt"></a>
<a id="tocstestdemoencrypt"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "deptId": 0,
  "userId": 0,
  "orderNum": 0,
  "testKey": "string",
  "value": "string",
  "version": 0,
  "delFlag": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|false|none||主键|
|deptId|integer(int64)|false|none||部门id|
|userId|integer(int64)|false|none||用户id|
|orderNum|integer(int32)|false|none||排序号|
|testKey|string|false|none||key键|
|value|string|false|none||值|
|version|integer(int64)|false|none||版本|
|delFlag|integer(int64)|false|none||删除标志|

<h2 id="tocS_RTestDemoVo">RTestDemoVo</h2>

<a id="schemartestdemovo"></a>
<a id="schema_RTestDemoVo"></a>
<a id="tocSrtestdemovo"></a>
<a id="tocsrtestdemovo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "deptId": 0,
    "userId": 0,
    "orderNum": 0,
    "testKey": "string",
    "value": "string",
    "createTime": "2019-08-24T14:15:22Z",
    "createBy": "string",
    "updateTime": "2019-08-24T14:15:22Z",
    "updateBy": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[TestDemoVo](#schematestdemovo)|false|none||测试单表视图对象 test_demo|

<h2 id="tocS_TestDemoVo">TestDemoVo</h2>

<a id="schematestdemovo"></a>
<a id="schema_TestDemoVo"></a>
<a id="tocStestdemovo"></a>
<a id="tocstestdemovo"></a>

```json
{
  "id": 0,
  "deptId": 0,
  "userId": 0,
  "orderNum": 0,
  "testKey": "string",
  "value": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "createBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "updateBy": "string"
}

```

测试单表视图对象 test_demo

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||主键|
|deptId|integer(int64)|false|none||部门id|
|userId|integer(int64)|false|none||用户id|
|orderNum|integer(int32)|false|none||排序号|
|testKey|string|false|none||key键|
|value|string|false|none||值|
|createTime|string(date-time)|false|none||创建时间|
|createBy|string|false|none||创建人|
|updateTime|string(date-time)|false|none||更新时间|
|updateBy|string|false|none||更新人|

<h2 id="tocS_TableDataInfoTestDemoVo">TableDataInfoTestDemoVo</h2>

<a id="schematabledatainfotestdemovo"></a>
<a id="schema_TableDataInfoTestDemoVo"></a>
<a id="tocStabledatainfotestdemovo"></a>
<a id="tocstabledatainfotestdemovo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "deptId": 0,
      "userId": 0,
      "orderNum": 0,
      "testKey": "string",
      "value": "string",
      "createTime": "2019-08-24T14:15:22Z",
      "createBy": "string",
      "updateTime": "2019-08-24T14:15:22Z",
      "updateBy": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[TestDemoVo](#schematestdemovo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RBoolean">RBoolean</h2>

<a id="schemarboolean"></a>
<a id="schema_RBoolean"></a>
<a id="tocSrboolean"></a>
<a id="tocsrboolean"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": true
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|boolean|false|none||none|

<h2 id="tocS_VerifyPhoneReqDto">VerifyPhoneReqDto</h2>

<a id="schemaverifyphonereqdto"></a>
<a id="schema_VerifyPhoneReqDto"></a>
<a id="tocSverifyphonereqdto"></a>
<a id="tocsverifyphonereqdto"></a>

```json
{
  "phoneNumber": "string",
  "verificationCode": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|phoneNumber|string|true|none||none|
|verificationCode|string|true|none||none|

<h2 id="tocS_ConsultDto">ConsultDto</h2>

<a id="schemaconsultdto"></a>
<a id="schema_ConsultDto"></a>
<a id="tocSconsultdto"></a>
<a id="tocsconsultdto"></a>

```json
{
  "id": 0,
  "question": "string",
  "customId": 0,
  "status": 0
}

```

用户咨询信息to

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int32)|false|none||问题编号,首次咨询不用携带|
|question|string|false|none||咨询内容|
|customId|integer(int32)|false|none||咨询人|
|status|integer(int32)|false|none||咨询状态: 0 未解决 1 解决|

<h2 id="tocS_AnswerDto">AnswerDto</h2>

<a id="schemaanswerdto"></a>
<a id="schema_AnswerDto"></a>
<a id="tocSanswerdto"></a>
<a id="tocsanswerdto"></a>

```json
{
  "consultId": 0,
  "question": "string",
  "answer": "string",
  "customId": 0,
  "status": 0
}

```

咨询dto

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|consultId|integer(int32)|false|none||问题编号|
|question|string|false|none||咨询问题|
|answer|string|false|none||咨询问题|
|customId|integer(int32)|false|none||咨询人|
|status|integer(int32)|false|none||咨询状态: 0 未解决 1 解决|

<h2 id="tocS_PublicRecommendQueryDto">PublicRecommendQueryDto</h2>

<a id="schemapublicrecommendquerydto"></a>
<a id="schema_PublicRecommendQueryDto"></a>
<a id="tocSpublicrecommendquerydto"></a>
<a id="tocspublicrecommendquerydto"></a>

```json
{
  "sexType": 0,
  "blindBox": 0,
  "amount": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|sexType|integer(int32)|false|none||要查询的性别0-女性，1-男性|
|blindBox|integer(int32)|false|none||是否拆盲盒：1-打码照片展示 2-正常照片展示 3-无照片展示|
|amount|integer(int32)|true|none||每日推荐数量|

<h2 id="tocS_WxCheckDto">WxCheckDto</h2>

<a id="schemawxcheckdto"></a>
<a id="schema_WxCheckDto"></a>
<a id="tocSwxcheckdto"></a>
<a id="tocswxcheckdto"></a>

```json
{
  "signature": "string",
  "timestamp": "string",
  "nonce": "string",
  "echostr": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|signature|string(string)|true|none||openid|
|timestamp|string(string)|false|none||none|
|nonce|string(string)|false|none||none|
|echostr|string(string)|false|none||none|

<h2 id="tocS_ChooseQueryDto">ChooseQueryDto</h2>

<a id="schemachoosequerydto"></a>
<a id="schema_ChooseQueryDto"></a>
<a id="tocSchoosequerydto"></a>
<a id="tocschoosequerydto"></a>

```json
{
  "customId": 0,
  "realName": "string",
  "wxNumber": "string",
  "sexType": "string",
  "pureHeight": "string",
  "homeTown": "string",
  "eduBackground": "string",
  "finalSchool": "string",
  "familySituation": "string",
  "emotionalState": "string",
  "loveExperience": "string",
  "workCity": "string",
  "workJob": "string",
  "workCompany": "string",
  "yearIncome": "string",
  "houseState": "string",
  "futureCity": "string",
  "verifyStatus": "string",
  "nickName": "string",
  "constellation": "string",
  "marryTime": "string",
  "idealRemark": "string",
  "carState": "string",
  "residencePlace": "string",
  "permanentPlace": "string",
  "weight": "string",
  "nation": "string",
  "hobby": "string",
  "nameCertifiedStatus": 0,
  "eduCertifiedStatus": 0,
  "jobCertifiedStatus": 0,
  "isDeleted": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|customId|integer(int64)|false|none||用户id|
|realName|string(string)|false|none||真实姓名|
|wxNumber|string(string)|false|none||微信号|
|sexType|string(string)|false|none||性别 1男，0女,2 未知|
|pureHeight|string(string)|false|none||身高cm|
|homeTown|string(string)|false|none||家乡|
|eduBackground|string(string)|false|none||学历|
|finalSchool|string(string)|false|none||毕业学校|
|familySituation|string(string)|false|none||家庭情况|
|emotionalState|string(string)|false|none||感情状况|
|loveExperience|string(string)|false|none||情感经历|
|workCity|string(string)|false|none||工作地|
|workJob|string(string)|false|none||职业|
|workCompany|string(string)|false|none||工作单位|
|yearIncome|string(string)|false|none||年收入万元|
|houseState|string(string)|false|none||房产情况|
|futureCity|string(string)|false|none||未来发展城市|
|verifyStatus|string(string)|false|none||认证状态  0：未认证，1：认证|
|nickName|string(string)|false|none||微信昵称|
|constellation|string(string)|false|none||星座|
|marryTime|string(string)|false|none||希望多久结婚|
|idealRemark|string(string)|false|none||理想的他/她|
|carState|string(string)|false|none||车辆情况|
|residencePlace|string(string)|false|none||居住地|
|permanentPlace|string(string)|false|none||户口所在地|
|weight|string(string)|false|none||身高|
|nation|string(string)|false|none||名族|
|hobby|string(string)|false|none||兴趣爱好|
|nameCertifiedStatus|integer(int32)|false|none||实名认证状态 0-认证中|1-认证成功|2-认证失败|
|eduCertifiedStatus|integer(int32)|false|none||学历认证状态 0-认证中|1-认证成功|2-认证失败|
|jobCertifiedStatus|integer(int32)|false|none||工作认证状态|
|isDeleted|string(string)|false|none||已删除(0:否 1:是)|

<h2 id="tocS_WxRequestDto">WxRequestDto</h2>

<a id="schemawxrequestdto"></a>
<a id="schema_WxRequestDto"></a>
<a id="tocSwxrequestdto"></a>
<a id="tocswxrequestdto"></a>

```json
{
  "openid": "string",
  "platformType": 0,
  "brandType": 0,
  "phone": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|openid|string|true|none||openid|
|platformType|integer(int32)|true|none||0 h5用户 1 小程序用户|
|brandType|integer(int32)|false|none||品牌类型 1=yxr 2=jxh 3=mbti|
|phone|string|false|none||phone|

<h2 id="tocS_LikeDto">LikeDto</h2>

<a id="schemalikedto"></a>
<a id="schema_LikeDto"></a>
<a id="tocSlikedto"></a>
<a id="tocslikedto"></a>

```json
{
  "status": 0,
  "loverId": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|status|integer(int32)|true|none||2: 不喜欢 1:喜欢 0：取消|
|loverId|integer(int64)|true|none||传入被喜欢人的customId|

<h2 id="tocS_ActivityCustomDto">ActivityCustomDto</h2>

<a id="schemaactivitycustomdto"></a>
<a id="schema_ActivityCustomDto"></a>
<a id="tocSactivitycustomdto"></a>
<a id="tocsactivitycustomdto"></a>

```json
{
  "activityId": 0,
  "enrollStatus": 0,
  "introducesId": 0,
  "remark": "string"
}

```

报名用户业务对象Dto

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|activityId|integer(int64)|true|none||活动id|
|enrollStatus|integer(int32)|true|none||1-报名 |0- 取消报名|
|introducesId|integer(int64)|false|none||活动推荐人id|
|remark|string|false|none||报名备注|

<h2 id="tocS_CustomQueryDto">CustomQueryDto</h2>

<a id="schemacustomquerydto"></a>
<a id="schema_CustomQueryDto"></a>
<a id="tocScustomquerydto"></a>
<a id="tocscustomquerydto"></a>

```json
{
  "shareId": "string",
  "birthDates": [
    "string"
  ],
  "pureHeights": [
    "string"
  ],
  "eduBackgrounds": [
    "string"
  ],
  "emotionalStates": [
    "string"
  ],
  "homeTown": "string",
  "verifyStatus": "string",
  "weights": [
    "string"
  ],
  "constellations": [
    "string"
  ],
  "yearIncome": "string",
  "residencePlace": "string",
  "workCity": "string",
  "workJobs": [
    "string"
  ],
  "houseStates": [
    "string"
  ],
  "carStates": [
    "string"
  ],
  "key": "string",
  "sexType": "string"
}

```

客户匹配设置业务对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|shareId|string|false|none||分享编号|
|birthDates|[string]|false|none||出生年月范围|
|pureHeights|[string]|false|none||身高范围|
|eduBackgrounds|[string]|false|none||学历范围|
|emotionalStates|[string]|false|none||感情状况|
|homeTown|string|false|none||家乡，格式：广东省/深圳市|
|verifyStatus|string|false|none||认证情况, 1-未三重认证，2-已三重认证|
|weights|[string]|false|none||身高范围|
|constellations|[string]|false|none||星座|
|yearIncome|string|false|none||收入范围, 数据格式：30-40W|
|residencePlace|string|false|none||现居地，数据格式：广东省/深圳市/南山区|
|workCity|string|false|none||工作地，数据格式：广东省/深圳市/南山区|
|workJobs|[string]|false|none||职业（多选）|
|houseStates|[string]|false|none||深圳房产情况，1-深圳有房、2-深圳无房|
|carStates|[string]|false|none||深圳车辆情况，1-深圳有车，2-深圳无车|
|key|string|false|none||键|
|sexType|string|false|none||性别 1男，0女,2 未知|

<h2 id="tocS_ActivityQueryDto">ActivityQueryDto</h2>

<a id="schemaactivityquerydto"></a>
<a id="schema_ActivityQueryDto"></a>
<a id="tocSactivityquerydto"></a>
<a id="tocsactivityquerydto"></a>

```json
{
  "status": "string",
  "grade": 0,
  "typeId": 0
}

```

活动查询dto

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|status|string(string)|false|none||活动状态(0-未开始|1-报名中|2-报名结束，活动进行中|3-活动结束，以;分割)|
|grade|integer(int32)|false|none||活动等级:越大优先级越高|
|typeId|integer(int32)|false|none||活动类型(0代表所有活动类型,4:双保险活动)|

<h2 id="tocS_ImageUploadDto">ImageUploadDto</h2>

<a id="schemaimageuploaddto"></a>
<a id="schema_ImageUploadDto"></a>
<a id="tocSimageuploaddto"></a>
<a id="tocsimageuploaddto"></a>

```json
{
  "pageId": "string",
  "images": [
    {
      "imageType": 0,
      "imageUrl": "string"
    }
  ]
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|pageId|string|true|none||页面编号, 5001-个人形象照, 5002-打码照片|
|images|[[CustomImageItemVo](#schemacustomimageitemvo)]|false|none||[照片管理视图对象]|

<h2 id="tocS_ImageQueryDto">ImageQueryDto</h2>

<a id="schemaimagequerydto"></a>
<a id="schema_ImageQueryDto"></a>
<a id="tocSimagequerydto"></a>
<a id="tocsimagequerydto"></a>

```json
{
  "pageId": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|pageId|string|true|none||页面编号, 5001-个人形象照, 5002-打码照片|

<h2 id="tocS_CustomImageBaseVo">CustomImageBaseVo</h2>

<a id="schemacustomimagebasevo"></a>
<a id="schema_CustomImageBaseVo"></a>
<a id="tocScustomimagebasevo"></a>
<a id="tocscustomimagebasevo"></a>

```json
{
  "imageId": 0,
  "customId": 0,
  "imageUrl": [
    "string"
  ]
}

```

照片管理视图对象 t_custom_image

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|imageId|integer(int64)|false|none||自增id|
|customId|integer(int64)|false|none||关联客户id|
|imageUrl|[string]|false|none||照片|

<h2 id="tocS_RCustomImageBaseVo">RCustomImageBaseVo</h2>

<a id="schemarcustomimagebasevo"></a>
<a id="schema_RCustomImageBaseVo"></a>
<a id="tocSrcustomimagebasevo"></a>
<a id="tocsrcustomimagebasevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "imageId": 0,
    "customId": 0,
    "imageUrl": [
      "string"
    ]
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[CustomImageBaseVo](#schemacustomimagebasevo)|false|none||照片管理视图对象 t_custom_image|

<h2 id="tocS_ActivityCustomLoveDto">ActivityCustomLoveDto</h2>

<a id="schemaactivitycustomlovedto"></a>
<a id="schema_ActivityCustomLoveDto"></a>
<a id="tocSactivitycustomlovedto"></a>
<a id="tocsactivitycustomlovedto"></a>

```json
{
  "activityId": 0,
  "loveType": 0
}

```

报名用户业务对象Dto

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|activityId|integer(int64)|true|none||活动id|
|loveType|integer(int32)|true|none||none|

<h2 id="tocS_ActivityCustomDetailDto">ActivityCustomDetailDto</h2>

<a id="schemaactivitycustomdetaildto"></a>
<a id="schema_ActivityCustomDetailDto"></a>
<a id="tocSactivitycustomdetaildto"></a>
<a id="tocsactivitycustomdetaildto"></a>

```json
{
  "activityId": 0,
  "customId": 0
}

```

报名用户业务对象Dto

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|activityId|integer(int64)|true|none||活动id|
|customId|integer(int64)|true|none||参加活动用户id|

<h2 id="tocS_CustomChooseDto">CustomChooseDto</h2>

<a id="schemacustomchoosedto"></a>
<a id="schema_CustomChooseDto"></a>
<a id="tocScustomchoosedto"></a>
<a id="tocscustomchoosedto"></a>

```json
{
  "loverStatus": 0
}

```

报名用户业务对象Dto

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|loverStatus|integer(int32)|true|none||none|

<h2 id="tocS_CustomDto">CustomDto</h2>

<a id="schemacustomdto"></a>
<a id="schema_CustomDto"></a>
<a id="tocScustomdto"></a>
<a id="tocscustomdto"></a>

```json
{
  "platformType": 0,
  "openid": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|platformType|integer(int32)|true|none||0 h5用户 1 小程序用户|
|openid|string(string)|true|none||openid|

<h2 id="tocS_ActivityChooseBaseDto">ActivityChooseBaseDto</h2>

<a id="schemaactivitychoosebasedto"></a>
<a id="schema_ActivityChooseBaseDto"></a>
<a id="tocSactivitychoosebasedto"></a>
<a id="tocsactivitychoosebasedto"></a>

```json
{
  "activityId": 0,
  "customId": 0,
  "loveStatus": 0
}

```

报名用户业务对象Dto

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|activityId|integer(int64)|true|none||活动id|
|customId|integer(int64)|true|none||参加活动用户id|
|loveStatus|integer(int32)|true|none||none|

<h2 id="tocS_CustomShareDto">CustomShareDto</h2>

<a id="schemacustomsharedto"></a>
<a id="schema_CustomShareDto"></a>
<a id="tocScustomsharedto"></a>
<a id="tocscustomsharedto"></a>

```json
{
  "platformType": 0,
  "shareCode": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|platformType|integer(int32)|true|none||0 h5用户 1 小程序用户|
|shareCode|string(string)|true|none||shareCode|

<h2 id="tocS_CustomBaseVo">CustomBaseVo</h2>

<a id="schemacustombasevo"></a>
<a id="schema_CustomBaseVo"></a>
<a id="tocScustombasevo"></a>
<a id="tocscustombasevo"></a>

```json
{
  "customId": 0,
  "nickName": "string",
  "wxNumber": "string",
  "birthDate": "2019-08-24T14:15:22Z",
  "pureHeight": "string",
  "homeTown": "string",
  "eduBackground": "string",
  "workCity": "string",
  "workJob": "string",
  "houseState": "string",
  "futureCity": "string",
  "futurePlan": "string",
  "masterImageUrl": "string",
  "verifyStatus": 0,
  "verifyStatusName": "string",
  "residencePlace": "string",
  "permanentPlace": "string",
  "weight": "string",
  "nation": "string",
  "loveStatus": 0,
  "loveStatusName": "string",
  "chooseSource": 0,
  "chooseTime": "2019-08-24T14:15:22Z",
  "blindBox": 0,
  "sexType": "string",
  "sexTypeName": "string"
}

```

客户信息视图对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|customId|integer(int64)|false|none||用户id|
|nickName|string|false|none||昵称|
|wxNumber|string|false|none||微信号|
|birthDate|string(date-time)|false|none||出生年月|
|pureHeight|string|false|none||身高cm|
|homeTown|string|false|none||家乡|
|eduBackground|string|false|none||学历|
|workCity|string|false|none||工作地|
|workJob|string|false|none||职业|
|houseState|string|false|none||房产情况|
|futureCity|string|false|none||未来发展城市|
|futurePlan|string|false|none||未来发展规划|
|masterImageUrl|string|false|none||主图|
|verifyStatus|integer(int32)|false|none||认证状态  0：未认证，1：认证|
|verifyStatusName|string|false|none||认证状态  0：未认证，1：认证|
|residencePlace|string|false|none||居住地|
|permanentPlace|string|false|none||户口所在地|
|weight|string|false|none||身高|
|nation|string|false|none||民族|
|loveStatus|integer(int32)|false|none||选择状态值 0-默认 1-喜欢 2-不喜欢 3-互相喜欢|
|loveStatusName|string|false|none||选择状态值 0-默认 1-喜欢 2-不喜欢 3-互相喜欢|
|chooseSource|integer(int32)|false|none||互选来源 0-活动互选 1-互选池互选|
|chooseTime|string(date-time)|false|none||互选时间|
|blindBox|integer(int32)|false|none||1-打码照片展示 2-正常照片展示 3-无照片展示|
|sexType|string|false|none||性别 1男，0女,2 未知|
|sexTypeName|string|false|none||性别 1男，0女,2 未知|

<h2 id="tocS_TableDataInfoCustomBaseVo">TableDataInfoCustomBaseVo</h2>

<a id="schematabledatainfocustombasevo"></a>
<a id="schema_TableDataInfoCustomBaseVo"></a>
<a id="tocStabledatainfocustombasevo"></a>
<a id="tocstabledatainfocustombasevo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "customId": 0,
      "nickName": "string",
      "wxNumber": "string",
      "birthDate": "2019-08-24T14:15:22Z",
      "pureHeight": "string",
      "homeTown": "string",
      "eduBackground": "string",
      "workCity": "string",
      "workJob": "string",
      "houseState": "string",
      "futureCity": "string",
      "futurePlan": "string",
      "masterImageUrl": "string",
      "verifyStatus": 0,
      "verifyStatusName": "string",
      "residencePlace": "string",
      "permanentPlace": "string",
      "weight": "string",
      "nation": "string",
      "loveStatus": 0,
      "loveStatusName": "string",
      "chooseSource": 0,
      "chooseTime": "2019-08-24T14:15:22Z",
      "blindBox": 0,
      "sexType": "string",
      "sexTypeName": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[CustomBaseVo](#schemacustombasevo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_ActivityBaseVo">ActivityBaseVo</h2>

<a id="schemaactivitybasevo"></a>
<a id="schema_ActivityBaseVo"></a>
<a id="tocSactivitybasevo"></a>
<a id="tocsactivitybasevo"></a>

```json
{
  "id": 0,
  "title": "string",
  "typeId": 0,
  "grade": 0,
  "titleImg": "string",
  "link": "string",
  "subTitle": "string",
  "maxNum": 0,
  "maxMaleNum": 0,
  "maxFemaleNum": 0,
  "address": "string",
  "beginTime": "2019-08-24T14:15:22Z",
  "endTime": "2019-08-24T14:15:22Z",
  "status": 0,
  "activityStatus": "string",
  "isSelect": 0,
  "isSelectStatusName": "string",
  "nowNum": 0,
  "briefIntroduction": "string",
  "activityCost": "string",
  "activityPrice": 0,
  "activityType": 0,
  "publicTypeName": "string",
  "preEnrollNum": 0,
  "typeTitle": "string",
  "enrollStatus": 0,
  "enrollStatusName": "string",
  "payStatus": 0,
  "payStatusName": "string",
  "activityCountdown": 0,
  "payModel": 0
}

```

活动列表视图对象 t_activity

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|title|string|false|none||活动名称|
|typeId|integer(int64)|false|none||活动类型id|
|grade|integer(int32)|false|none||活动等级，数字越大优先级越高，普通活动为0|
|titleImg|string|false|none||活动封面图片|
|link|string|false|none||对应公众号链接|
|subTitle|string|false|none||副标题|
|maxNum|integer(int64)|false|none||活动最大人数,如果为0则无限大|
|maxMaleNum|integer(int64)|false|none||男生最大人数（不设置则不限制 ）|
|maxFemaleNum|integer(int64)|false|none||女生最大人数（不设置则不限制 ）|
|address|string|false|none||活动地址|
|beginTime|string(date-time)|false|none||活动开始时间-年月日时分秒|
|endTime|string(date-time)|false|none||活动开始时间-年月日时分秒|
|status|integer(int32)|false|none||活动状态：0-未开始|1-报名中|2-报名结束，活动进行中|3-活动结束|
|activityStatus|string|false|none||活动状态：0-未开始|1-报名中|2-报名结束，活动进行中|3-活动结束|
|isSelect|integer(int32)|false|none||是否开启互选 0-未开启|1-开启|2-互选结束|
|isSelectStatusName|string|false|none||none|
|nowNum|integer(int64)|false|none||目前报名活动人数|
|briefIntroduction|string|false|none||活动简介|
|activityCost|string|false|none||活动费用介绍|
|activityPrice|number|false|none||活动费用|
|activityType|integer(int32)|false|none||0 非公益 1 公益|
|publicTypeName|string|false|none||0 非公益 1 公益|
|preEnrollNum|integer(int64)|false|none||预报名人数|
|typeTitle|string|false|none||活动类型名|
|enrollStatus|integer(int32)|false|none||报名状态 0 未报名 1 已报名 2 取消报名 3 报名成功|
|enrollStatusName|string|false|none||报名状态 0 未报名 1 已报名 2 取消报名 3 报名成功|
|payStatus|integer(int32)|false|none||支付状态 0 未支付  1 已支付 2 退款|
|payStatusName|string|false|none||支付状态 0 未支付  1 已支付 2 退款|
|activityCountdown|integer(int32)|false|none||none|
|payModel|integer(int32)|false|none||是否需要支付, 0-需要支付, 1-不需要支付|

<h2 id="tocS_TableDataInfoActivityBaseVo">TableDataInfoActivityBaseVo</h2>

<a id="schematabledatainfoactivitybasevo"></a>
<a id="schema_TableDataInfoActivityBaseVo"></a>
<a id="tocStabledatainfoactivitybasevo"></a>
<a id="tocstabledatainfoactivitybasevo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "title": "string",
      "typeId": 0,
      "grade": 0,
      "titleImg": "string",
      "link": "string",
      "subTitle": "string",
      "maxNum": 0,
      "maxMaleNum": 0,
      "maxFemaleNum": 0,
      "address": "string",
      "beginTime": "2019-08-24T14:15:22Z",
      "endTime": "2019-08-24T14:15:22Z",
      "status": 0,
      "activityStatus": "string",
      "isSelect": 0,
      "isSelectStatusName": "string",
      "nowNum": 0,
      "briefIntroduction": "string",
      "activityCost": "string",
      "activityPrice": 0,
      "activityType": 0,
      "publicTypeName": "string",
      "preEnrollNum": 0,
      "typeTitle": "string",
      "enrollStatus": 0,
      "enrollStatusName": "string",
      "payStatus": 0,
      "payStatusName": "string",
      "activityCountdown": 0,
      "payModel": 0
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[ActivityBaseVo](#schemaactivitybasevo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RefundDto">RefundDto</h2>

<a id="schemarefunddto"></a>
<a id="schema_RefundDto"></a>
<a id="tocSrefunddto"></a>
<a id="tocsrefunddto"></a>

```json
{
  "payCode": 0,
  "orderNo": "string",
  "refund": 0,
  "amount": 0,
  "reason": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|payCode|integer(int32)|true|none||payCode 1=微信支付，2=支付宝支付|
|orderNo|string|true|none||订单号|
|refund|number|true|none||退款金额|
|amount|number|false|none||实际支付金额|
|reason|string|false|none||退款原因|

<h2 id="tocS_CloseOrderDto">CloseOrderDto</h2>

<a id="schemacloseorderdto"></a>
<a id="schema_CloseOrderDto"></a>
<a id="tocScloseorderdto"></a>
<a id="tocscloseorderdto"></a>

```json
{
  "payCode": 0,
  "orderNo": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|payCode|integer(int32)|true|none||payCode 1=微信支付，2=支付宝支付|
|orderNo|string|true|none||订单号|

<h2 id="tocS_CollectDto">CollectDto</h2>

<a id="schemacollectdto"></a>
<a id="schema_CollectDto"></a>
<a id="tocScollectdto"></a>
<a id="tocscollectdto"></a>

```json
{
  "status": 0,
  "customId": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|status|integer(int32)|true|none||1=收藏 0=取消收藏|
|customId|integer(int64)|true|none||传入被收藏人的customId|

<h2 id="tocS_RActivityVo">RActivityVo</h2>

<a id="schemaractivityvo"></a>
<a id="schema_RActivityVo"></a>
<a id="tocSractivityvo"></a>
<a id="tocsractivityvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "title": "string",
    "typeId": 0,
    "grade": 0,
    "titleImg": "string",
    "link": "string",
    "subTitle": "string",
    "maxNum": 0,
    "maxMaleNum": 0,
    "maxFemaleNum": 0,
    "address": "string",
    "detail": "string",
    "detailImg": "string",
    "beginTime": "2019-08-24T14:15:22Z",
    "endTime": "2019-08-24T14:15:22Z",
    "status": "string",
    "isSelect": 0,
    "nowNum": 0,
    "nowMaleNum": 0,
    "nowFemaleNum": 0,
    "maxChooseNum": 0,
    "briefIntroduction": "string",
    "activityCost": "string",
    "activityPrice": 0,
    "isOnline": "string",
    "activityType": 0,
    "preEnrollNum": 0,
    "activityPlatform": "string",
    "typeTitle": "string",
    "enrollStatus": 0,
    "enrollStatusName": "string",
    "payStatus": 0,
    "payStatusName": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[ActivityVo](#schemaactivityvo)|false|none||活动列表视图对象 t_activity|

<h2 id="tocS_CustomDetailVo">CustomDetailVo</h2>

<a id="schemacustomdetailvo"></a>
<a id="schema_CustomDetailVo"></a>
<a id="tocScustomdetailvo"></a>
<a id="tocscustomdetailvo"></a>

```json
{
  "customId": 0,
  "realName": "string",
  "phoneNumber": "string",
  "wxNumber": "string",
  "sexType": "string",
  "birthDate": "2019-08-24T14:15:22Z",
  "pureHeight": "string",
  "homeTown": "string",
  "eduBackground": "string",
  "finalSchool": "string",
  "familySituation": "string",
  "emotionalState": "string",
  "loveExperience": "string",
  "workCity": "string",
  "workJob": "string",
  "workCompany": "string",
  "yearIncome": "string",
  "houseState": "string",
  "futureCity": "string",
  "futurePlan": "string",
  "personalIntro": "string",
  "familyIntro": "string",
  "loveIntro": "string",
  "imageUrl": [
    "string"
  ],
  "verifyStatus": "string",
  "referrer": "string",
  "nickName": "string",
  "constellation": "string",
  "marryTime": "string",
  "idealRemark": "string",
  "carState": "string",
  "residencePlace": "string",
  "permanentPlace": "string",
  "weight": "string",
  "nation": "string",
  "hobby": "string",
  "memberType": "string",
  "verifyPhoneStatus": "string",
  "friendName": "string",
  "nameCertifiedStatus": 0,
  "nameCertifiedStatusName": "string",
  "eduCertifiedStatus": 0,
  "eduCertifiedStatusName": "string",
  "jobCertifiedStatus": 0,
  "jobCertifiedStatusName": "string",
  "loveStatus": 0,
  "loveStatusName": "string",
  "collectStatus": 0,
  "avatarUrl": "string",
  "brandId": 0,
  "customImageInfo": {
    "personalImageUrls": [
      "string"
    ],
    "blindImageUrls": [
      "string"
    ],
    "imageUrls": [
      "string"
    ]
  },
  "customSettingVo": {
    "id": 0,
    "customId": 0,
    "choose": 0,
    "blindBox": 0,
    "one2one": 0,
    "chooseIdentity": 0,
    "hideYearIncomeStatus": 0,
    "hideSchoolStatus": 0,
    "hidePersonalIntroStatus": 0,
    "hideLoveIntroStatus": 0,
    "hideHobbyStatus": 0,
    "hideIdealRemarkStatus": 0,
    "status": 0,
    "remark": "string",
    "testCode": "string"
  }
}

```

客户信息视图对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|customId|integer(int64)|false|none||用户id|
|realName|string|false|none||真实姓名|
|phoneNumber|string|false|none||手机号|
|wxNumber|string|false|none||微信号|
|sexType|string|false|none||性别 1男，0女,2 未知|
|birthDate|string(date-time)|false|none||出生年月|
|pureHeight|string|false|none||身高cm|
|homeTown|string|false|none||家乡|
|eduBackground|string|false|none||学历|
|finalSchool|string|false|none||毕业学校|
|familySituation|string|false|none||家庭情况|
|emotionalState|string|false|none||感情状况|
|loveExperience|string|false|none||情感经历|
|workCity|string|false|none||工作地|
|workJob|string|false|none||职业|
|workCompany|string|false|none||工作单位|
|yearIncome|string|false|none||年收入万元|
|houseState|string|false|none||房产情况|
|futureCity|string|false|none||未来发展城市|
|futurePlan|string|false|none||未来发展规划|
|personalIntro|string|false|none||个人介绍|
|familyIntro|string|false|none||家庭情况|
|loveIntro|string|false|none||感情观|
|imageUrl|[string]|false|none||照片|
|verifyStatus|string|false|none||认证状态  0：未认证，1：认证，2:认证不通过|
|referrer|string|false|none||推荐人|
|nickName|string|false|none||微信昵称|
|constellation|string|false|none||星座|
|marryTime|string|false|none||希望多久结婚|
|idealRemark|string|false|none||理想的他/她|
|carState|string|false|none||车辆情况|
|residencePlace|string|false|none||居住地|
|permanentPlace|string|false|none||户口所在地|
|weight|string|false|none||身高|
|nation|string|false|none||民族|
|hobby|string|false|none||兴趣爱好|
|memberType|string|false|none||0 非会员 1 VIP 2SVIP|
|verifyPhoneStatus|string|false|none||0未验证 1已验证|
|friendName|string|false|none||朋友姓名|
|nameCertifiedStatus|integer(int32)|false|none||实名认证状态 0-认证中|1-认证成功|2-认证失败|
|nameCertifiedStatusName|string|false|none||none|
|eduCertifiedStatus|integer(int32)|false|none||学历认证状态 0-认证中|1-认证成功|2-认证失败|
|eduCertifiedStatusName|string|false|none||none|
|jobCertifiedStatus|integer(int32)|false|none||工作认证状态|
|jobCertifiedStatusName|string|false|none||none|
|loveStatus|integer(int32)|false|none||选择状态值 0-默认 1-喜欢 2-不喜欢 3-互相喜欢|
|loveStatusName|string|false|none||选择状态值 0-默认 1-喜欢 2-不喜欢 3-互相喜欢|
|collectStatus|integer(int32)|false|none||选择状态值  0=取消收藏  1=收藏|
|avatarUrl|string|false|none||用户图像|
|brandId|integer(int32)|false|none||品牌id|
|customImageInfo|[CustomImageInfoVo](#schemacustomimageinfovo)|false|none||照片管理视图|
|customSettingVo|[CustomSettingVo](#schemacustomsettingvo)|false|none||用户个性设置视图对象 t_custom_setting|

<h2 id="tocS_RCustomDetailVo">RCustomDetailVo</h2>

<a id="schemarcustomdetailvo"></a>
<a id="schema_RCustomDetailVo"></a>
<a id="tocSrcustomdetailvo"></a>
<a id="tocsrcustomdetailvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "customId": 0,
    "realName": "string",
    "phoneNumber": "string",
    "wxNumber": "string",
    "sexType": "string",
    "birthDate": "2019-08-24T14:15:22Z",
    "pureHeight": "string",
    "homeTown": "string",
    "eduBackground": "string",
    "finalSchool": "string",
    "familySituation": "string",
    "emotionalState": "string",
    "loveExperience": "string",
    "workCity": "string",
    "workJob": "string",
    "workCompany": "string",
    "yearIncome": "string",
    "houseState": "string",
    "futureCity": "string",
    "futurePlan": "string",
    "personalIntro": "string",
    "familyIntro": "string",
    "loveIntro": "string",
    "imageUrl": [
      "string"
    ],
    "verifyStatus": "string",
    "referrer": "string",
    "nickName": "string",
    "constellation": "string",
    "marryTime": "string",
    "idealRemark": "string",
    "carState": "string",
    "residencePlace": "string",
    "permanentPlace": "string",
    "weight": "string",
    "nation": "string",
    "hobby": "string",
    "memberType": "string",
    "verifyPhoneStatus": "string",
    "friendName": "string",
    "nameCertifiedStatus": 0,
    "nameCertifiedStatusName": "string",
    "eduCertifiedStatus": 0,
    "eduCertifiedStatusName": "string",
    "jobCertifiedStatus": 0,
    "jobCertifiedStatusName": "string",
    "loveStatus": 0,
    "loveStatusName": "string",
    "collectStatus": 0,
    "avatarUrl": "string",
    "brandId": 0,
    "customImageInfo": {
      "personalImageUrls": [
        "string"
      ],
      "blindImageUrls": [
        "string"
      ],
      "imageUrls": [
        "string"
      ]
    },
    "customSettingVo": {
      "id": 0,
      "customId": 0,
      "choose": 0,
      "blindBox": 0,
      "one2one": 0,
      "chooseIdentity": 0,
      "hideYearIncomeStatus": 0,
      "hideSchoolStatus": 0,
      "hidePersonalIntroStatus": 0,
      "hideLoveIntroStatus": 0,
      "hideHobbyStatus": 0,
      "hideIdealRemarkStatus": 0,
      "status": 0,
      "remark": "string",
      "testCode": "string"
    }
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[CustomDetailVo](#schemacustomdetailvo)|false|none||客户信息视图对象|

<h2 id="tocS_RListCustomBaseVo">RListCustomBaseVo</h2>

<a id="schemarlistcustombasevo"></a>
<a id="schema_RListCustomBaseVo"></a>
<a id="tocSrlistcustombasevo"></a>
<a id="tocsrlistcustombasevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "customId": 0,
      "nickName": "string",
      "wxNumber": "string",
      "birthDate": "2019-08-24T14:15:22Z",
      "pureHeight": "string",
      "homeTown": "string",
      "eduBackground": "string",
      "workCity": "string",
      "workJob": "string",
      "houseState": "string",
      "futureCity": "string",
      "futurePlan": "string",
      "masterImageUrl": "string",
      "verifyStatus": 0,
      "verifyStatusName": "string",
      "residencePlace": "string",
      "permanentPlace": "string",
      "weight": "string",
      "nation": "string",
      "loveStatus": 0,
      "loveStatusName": "string",
      "chooseSource": 0,
      "chooseTime": "2019-08-24T14:15:22Z",
      "blindBox": 0,
      "sexType": "string",
      "sexTypeName": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[CustomBaseVo](#schemacustombasevo)]|false|none||[客户信息视图对象]|

<h2 id="tocS_RCustomVerifyRespVo">RCustomVerifyRespVo</h2>

<a id="schemarcustomverifyrespvo"></a>
<a id="schema_RCustomVerifyRespVo"></a>
<a id="tocSrcustomverifyrespvo"></a>
<a id="tocsrcustomverifyrespvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "customId": 0,
    "verifyStatus": 0,
    "verifyStatusName": "string",
    "verifyImageUrl": [
      "string"
    ],
    "verifyFailReason": "string",
    "nameAuthType": 0,
    "nameAuthName": "string",
    "nameAuthCertNo": "string",
    "academicAuthType": 0,
    "academicAuthName": "string",
    "academicAuthSit": "string",
    "jobAuthType": 0,
    "jobAuthCompanyAllName": "string",
    "jobAuthCompanyName": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[CustomVerifyRespVo](#schemacustomverifyrespvo)|false|none||none|

<h2 id="tocS_LoginCustomVo">LoginCustomVo</h2>

<a id="schemalogincustomvo"></a>
<a id="schema_LoginCustomVo"></a>
<a id="tocSlogincustomvo"></a>
<a id="tocslogincustomvo"></a>

```json
{
  "customId": 0,
  "realName": "string",
  "phoneNumber": "string",
  "wxNumber": "string",
  "sexType": "string",
  "birthDate": "2019-08-24T14:15:22Z",
  "pureHeight": "string",
  "homeTown": "string",
  "eduBackground": "string",
  "finalSchool": "string",
  "familySituation": "string",
  "emotionalState": "string",
  "loveExperience": "string",
  "workCity": "string",
  "workJob": "string",
  "workCompany": "string",
  "yearIncome": "string",
  "houseState": "string",
  "futureCity": "string",
  "futurePlan": "string",
  "personalIntro": "string",
  "familyIntro": "string",
  "loveIntro": "string",
  "imageUrl": [
    "string"
  ],
  "customImageInfo": {
    "personalImageUrls": [
      "string"
    ],
    "blindImageUrls": [
      "string"
    ],
    "imageUrls": [
      "string"
    ]
  },
  "verifyStatus": 0,
  "referrer": "string",
  "nickName": "string",
  "constellation": "string",
  "marryTime": "string",
  "idealRemark": "string",
  "carState": "string",
  "shareCode": "string",
  "residencePlace": "string",
  "permanentPlace": "string",
  "userType": "string",
  "weight": "string",
  "nation": "string",
  "hobby": "string",
  "memberType": "string",
  "memberTypeName": "string",
  "verifyPhoneStatus": 0,
  "friendName": "string",
  "nameCertifiedStatus": 0,
  "nameCertifiedStatusName": "string",
  "eduCertifiedStatus": 0,
  "jobCertifiedStatus": 0,
  "avatarUrl": "string",
  "customSettingVo": {
    "id": 0,
    "customId": 0,
    "choose": 0,
    "blindBox": 0,
    "one2one": 0,
    "chooseIdentity": 0,
    "hideYearIncomeStatus": 0,
    "hideSchoolStatus": 0,
    "hidePersonalIntroStatus": 0,
    "hideLoveIntroStatus": 0,
    "hideHobbyStatus": 0,
    "hideIdealRemarkStatus": 0,
    "status": 0,
    "remark": "string",
    "testCode": "string"
  },
  "memberTypeVo": {
    "vipId": 0,
    "vipName": "string",
    "bgColor": "string",
    "startTime": "2019-08-24T14:15:22Z",
    "endTime": "2019-08-24T14:15:22Z"
  },
  "brandType": 0,
  "platformType": 0,
  "isMember": 0
}

```

客户信息视图对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|customId|integer(int64)|false|none||用户id|
|realName|string|false|none||真实姓名|
|phoneNumber|string|false|none||手机号|
|wxNumber|string|false|none||微信号|
|sexType|string|false|none||性别 1男，0女,2 未知|
|birthDate|string(date-time)|false|none||出生年月|
|pureHeight|string|false|none||身高cm|
|homeTown|string|false|none||家乡|
|eduBackground|string|false|none||学历|
|finalSchool|string|false|none||毕业学校|
|familySituation|string|false|none||家庭情况|
|emotionalState|string|false|none||感情状况|
|loveExperience|string|false|none||情感经历|
|workCity|string|false|none||工作地|
|workJob|string|false|none||职业|
|workCompany|string|false|none||工作单位|
|yearIncome|string|false|none||年收入万元|
|houseState|string|false|none||房产情况|
|futureCity|string|false|none||未来发展城市|
|futurePlan|string|false|none||未来发展规划|
|personalIntro|string|false|none||个人介绍|
|familyIntro|string|false|none||家庭情况|
|loveIntro|string|false|none||感情观|
|imageUrl|[string]|false|none||照片|
|customImageInfo|[CustomImageInfoVo](#schemacustomimageinfovo)|false|none||照片管理视图|
|verifyStatus|integer(int32)|false|none||认证状态  0：未认证，1：认证|
|referrer|string|false|none||推荐人|
|nickName|string|false|none||微信昵称|
|constellation|string|false|none||星座|
|marryTime|string|false|none||希望多久结婚|
|idealRemark|string|false|none||理想的他/她|
|carState|string|false|none||车辆情况|
|shareCode|string|false|none||分享码|
|residencePlace|string|false|none||居住地|
|permanentPlace|string|false|none||户口所在地|
|userType|string|false|none||0 h5用户 1 小程序用户|
|weight|string|false|none||身高|
|nation|string|false|none||名族|
|hobby|string|false|none||兴趣爱好|
|memberType|string|false|none||0=非会员,1=VIP,2=SVIP,3=专属会员|
|memberTypeName|string|false|none||0=非会员,1=VIP,2=SVIP,3=专属会员|
|verifyPhoneStatus|integer(int32)|false|none||0未验证 1已验证|
|friendName|string|false|none||朋友姓名|
|nameCertifiedStatus|integer(int32)|false|none||实名认证状态 0-认证中|1-认证成功|2-认证失败|
|nameCertifiedStatusName|string|false|none||none|
|eduCertifiedStatus|integer(int32)|false|none||学历认证状态 0-认证中|1-认证成功|2-认证失败|
|jobCertifiedStatus|integer(int32)|false|none||工作认证状态|
|avatarUrl|string|false|none||用户图像|
|customSettingVo|[CustomSettingVo](#schemacustomsettingvo)|false|none||用户个性设置视图对象 t_custom_setting|
|memberTypeVo|[MemberTypeVo](#schemamembertypevo)|false|none||会员类型Vo|
|brandType|integer(int32)|false|none||none|
|platformType|integer(int32)|false|none||none|
|isMember|integer(int32)|false|none||0 非会员 1 会员|

<h2 id="tocS_RLoginCustomVo">RLoginCustomVo</h2>

<a id="schemarlogincustomvo"></a>
<a id="schema_RLoginCustomVo"></a>
<a id="tocSrlogincustomvo"></a>
<a id="tocsrlogincustomvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "customId": 0,
    "realName": "string",
    "phoneNumber": "string",
    "wxNumber": "string",
    "sexType": "string",
    "birthDate": "2019-08-24T14:15:22Z",
    "pureHeight": "string",
    "homeTown": "string",
    "eduBackground": "string",
    "finalSchool": "string",
    "familySituation": "string",
    "emotionalState": "string",
    "loveExperience": "string",
    "workCity": "string",
    "workJob": "string",
    "workCompany": "string",
    "yearIncome": "string",
    "houseState": "string",
    "futureCity": "string",
    "futurePlan": "string",
    "personalIntro": "string",
    "familyIntro": "string",
    "loveIntro": "string",
    "imageUrl": [
      "string"
    ],
    "customImageInfo": {
      "personalImageUrls": [
        "string"
      ],
      "blindImageUrls": [
        "string"
      ],
      "imageUrls": [
        "string"
      ]
    },
    "verifyStatus": 0,
    "referrer": "string",
    "nickName": "string",
    "constellation": "string",
    "marryTime": "string",
    "idealRemark": "string",
    "carState": "string",
    "shareCode": "string",
    "residencePlace": "string",
    "permanentPlace": "string",
    "userType": "string",
    "weight": "string",
    "nation": "string",
    "hobby": "string",
    "memberType": "string",
    "memberTypeName": "string",
    "verifyPhoneStatus": 0,
    "friendName": "string",
    "nameCertifiedStatus": 0,
    "nameCertifiedStatusName": "string",
    "eduCertifiedStatus": 0,
    "jobCertifiedStatus": 0,
    "avatarUrl": "string",
    "customSettingVo": {
      "id": 0,
      "customId": 0,
      "choose": 0,
      "blindBox": 0,
      "one2one": 0,
      "chooseIdentity": 0,
      "hideYearIncomeStatus": 0,
      "hideSchoolStatus": 0,
      "hidePersonalIntroStatus": 0,
      "hideLoveIntroStatus": 0,
      "hideHobbyStatus": 0,
      "hideIdealRemarkStatus": 0,
      "status": 0,
      "remark": "string",
      "testCode": "string"
    },
    "memberTypeVo": {
      "vipId": 0,
      "vipName": "string",
      "bgColor": "string",
      "startTime": "2019-08-24T14:15:22Z",
      "endTime": "2019-08-24T14:15:22Z"
    },
    "brandType": 0,
    "platformType": 0,
    "isMember": 0
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[LoginCustomVo](#schemalogincustomvo)|false|none||客户信息视图对象|

<h2 id="tocS_CustomAddressBo">CustomAddressBo</h2>

<a id="schemacustomaddressbo"></a>
<a id="schema_CustomAddressBo"></a>
<a id="tocScustomaddressbo"></a>
<a id="tocscustomaddressbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "customId": 0,
  "contactName": "string",
  "phone": "string",
  "contactArea": "string",
  "address": "string",
  "postCode": "string",
  "status": 0,
  "remark": "string",
  "isDefault": 0
}

```

用户联系地址业务对象 t_custom_address

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||客户id|
|customId|integer(int64)|true|none||主动方id|
|contactName|string(string)|true|none||联系人姓名|
|phone|string(string)|true|none||联系人|
|contactArea|string(string)|true|none||地区|
|address|string(string)|true|none||详细地址|
|postCode|string(string)|true|none||邮编|
|status|integer(int32)|true|none||状态（0正常 1停用）|
|remark|string(string)|true|none||备注|
|isDefault|integer(int32)|false|none||是否默认 0=非默认 1= 默认|

<h2 id="tocS_CustomAddressDto">CustomAddressDto</h2>

<a id="schemacustomaddressdto"></a>
<a id="schema_CustomAddressDto"></a>
<a id="tocScustomaddressdto"></a>
<a id="tocscustomaddressdto"></a>

```json
{
  "id": 0,
  "customId": 0,
  "contactName": "string",
  "phone": "string",
  "contactArea": "string",
  "address": "string",
  "postCode": "string",
  "isDefault": 0,
  "remark": "string"
}

```

用户联系地址业务对象 t_custom_address

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|customId|integer(int64)|true|none||客户id|
|contactName|string|true|none||联系人姓名|
|phone|string|true|none||联系人|
|contactArea|string|true|none||地区|
|address|string|true|none||详细地址|
|postCode|string|true|none||邮编|
|isDefault|integer(int32)|true|none||是否默认 0=非默认 1= 默认|
|remark|string|false|none||备注|

<h2 id="tocS_CustomAddressVo">CustomAddressVo</h2>

<a id="schemacustomaddressvo"></a>
<a id="schema_CustomAddressVo"></a>
<a id="tocScustomaddressvo"></a>
<a id="tocscustomaddressvo"></a>

```json
{
  "id": 0,
  "customId": 0,
  "contactName": "string",
  "phone": "string",
  "contactArea": "string",
  "address": "string",
  "postCode": "string",
  "status": 0,
  "isDefault": 0,
  "remark": "string"
}

```

用户联系地址视图对象 t_custom_address

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|customId|integer(int64)|false|none||客户id|
|contactName|string|false|none||联系人姓名|
|phone|string|false|none||联系电话|
|contactArea|string|false|none||地区|
|address|string|false|none||详细地址|
|postCode|string|false|none||邮编|
|status|integer(int32)|false|none||状态（0正常 1停用）|
|isDefault|integer(int32)|false|none||是否默认 0=非默认 1= 默认|
|remark|string|false|none||备注|

<h2 id="tocS_RCustomAddressVo">RCustomAddressVo</h2>

<a id="schemarcustomaddressvo"></a>
<a id="schema_RCustomAddressVo"></a>
<a id="tocSrcustomaddressvo"></a>
<a id="tocsrcustomaddressvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "customId": 0,
    "contactName": "string",
    "phone": "string",
    "contactArea": "string",
    "address": "string",
    "postCode": "string",
    "status": 0,
    "isDefault": 0,
    "remark": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[CustomAddressVo](#schemacustomaddressvo)|false|none||用户联系地址视图对象 t_custom_address|

<h2 id="tocS_TableDataInfoCustomAddressVo">TableDataInfoCustomAddressVo</h2>

<a id="schematabledatainfocustomaddressvo"></a>
<a id="schema_TableDataInfoCustomAddressVo"></a>
<a id="tocStabledatainfocustomaddressvo"></a>
<a id="tocstabledatainfocustomaddressvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "customId": 0,
      "contactName": "string",
      "phone": "string",
      "contactArea": "string",
      "address": "string",
      "postCode": "string",
      "status": 0,
      "isDefault": 0,
      "remark": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[CustomAddressVo](#schemacustomaddressvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RListCustomAddressVo">RListCustomAddressVo</h2>

<a id="schemarlistcustomaddressvo"></a>
<a id="schema_RListCustomAddressVo"></a>
<a id="tocSrlistcustomaddressvo"></a>
<a id="tocsrlistcustomaddressvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "id": 0,
      "customId": 0,
      "contactName": "string",
      "phone": "string",
      "contactArea": "string",
      "address": "string",
      "postCode": "string",
      "status": 0,
      "isDefault": 0,
      "remark": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[CustomAddressVo](#schemacustomaddressvo)]|false|none||[用户联系地址视图对象 t_custom_address]|

<h2 id="tocS_RTraitMbtiUserTestVo">RTraitMbtiUserTestVo</h2>

<a id="schemartraitmbtiusertestvo"></a>
<a id="schema_RTraitMbtiUserTestVo"></a>
<a id="tocSrtraitmbtiusertestvo"></a>
<a id="tocsrtraitmbtiusertestvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "traitTile": "string",
    "traitCode": "string",
    "traitName": "string",
    "traitImgUrl": "string",
    "traitDesc": "string",
    "traits": [
      {
        "traitTile": "string",
        "traitCode": "string",
        "traitName": "string",
        "traitReverseName": "string",
        "traitImgUrl": "string",
        "traitDesc": "string",
        "traitScore": 0
      }
    ]
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[TraitMbtiUserTestVo](#schematraitmbtiusertestvo)|false|none||MBTI性格特征|

<h2 id="tocS_TraitMbtiUserTestDetailVo">TraitMbtiUserTestDetailVo</h2>

<a id="schematraitmbtiusertestdetailvo"></a>
<a id="schema_TraitMbtiUserTestDetailVo"></a>
<a id="tocStraitmbtiusertestdetailvo"></a>
<a id="tocstraitmbtiusertestdetailvo"></a>

```json
{
  "traitTile": "string",
  "traitCode": "string",
  "traitName": "string",
  "traitReverseName": "string",
  "traitImgUrl": "string",
  "traitDesc": "string",
  "traitScore": 0
}

```

MBTI性格特征

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|traitTile|string|false|none||性格标题|
|traitCode|string|false|none||性格编号|
|traitName|string|false|none||性格名称|
|traitReverseName|string|false|none||性格反向名称|
|traitImgUrl|string|false|none||性格图片链接|
|traitDesc|string|false|none||性格描述|
|traitScore|number|false|none||性格分数|

<h2 id="tocS_TraitMbtiUserTestVo">TraitMbtiUserTestVo</h2>

<a id="schematraitmbtiusertestvo"></a>
<a id="schema_TraitMbtiUserTestVo"></a>
<a id="tocStraitmbtiusertestvo"></a>
<a id="tocstraitmbtiusertestvo"></a>

```json
{
  "traitTile": "string",
  "traitCode": "string",
  "traitName": "string",
  "traitImgUrl": "string",
  "traitDesc": "string",
  "traits": [
    {
      "traitTile": "string",
      "traitCode": "string",
      "traitName": "string",
      "traitReverseName": "string",
      "traitImgUrl": "string",
      "traitDesc": "string",
      "traitScore": 0
    }
  ]
}

```

MBTI性格特征

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|traitTile|string|false|none||性格标题|
|traitCode|string|false|none||性格编号|
|traitName|string|false|none||性格名称|
|traitImgUrl|string|false|none||性格图片链接|
|traitDesc|string|false|none||性格描述|
|traits|[[TraitMbtiUserTestDetailVo](#schematraitmbtiusertestdetailvo)]|false|none||性格明细|

<h2 id="tocS_RListTraitMbtiTestResultVo">RListTraitMbtiTestResultVo</h2>

<a id="schemarlisttraitmbtitestresultvo"></a>
<a id="schema_RListTraitMbtiTestResultVo"></a>
<a id="tocSrlisttraitmbtitestresultvo"></a>
<a id="tocsrlisttraitmbtitestresultvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "testCode": "string",
      "infoCode": "string",
      "infoTitle": "string",
      "traitCode": "string",
      "traitImgUrl": "string",
      "traitName": "string",
      "traitDesc": "string",
      "testTime": "2019-08-24T14:15:22Z"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[TraitMbtiTestResultVo](#schematraitmbtitestresultvo)]|false|none||[MBTI用户测评结果]|

<h2 id="tocS_TraitMbtiTestResultVo">TraitMbtiTestResultVo</h2>

<a id="schematraitmbtitestresultvo"></a>
<a id="schema_TraitMbtiTestResultVo"></a>
<a id="tocStraitmbtitestresultvo"></a>
<a id="tocstraitmbtitestresultvo"></a>

```json
{
  "testCode": "string",
  "infoCode": "string",
  "infoTitle": "string",
  "traitCode": "string",
  "traitImgUrl": "string",
  "traitName": "string",
  "traitDesc": "string",
  "testTime": "2019-08-24T14:15:22Z"
}

```

MBTI用户测评结果

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|testCode|string|false|none||性格测试结果编码|
|infoCode|string|false|none||性格信息编码|
|infoTitle|string|false|none||信息标题|
|traitCode|string|false|none||性格编号|
|traitImgUrl|string|false|none||性格图片链接|
|traitName|string|false|none||性格名称|
|traitDesc|string|false|none||性格描述|
|testTime|string(date-time)|false|none||性格测试时间|

<h2 id="tocS_RListTraitMbtiQuestionInfoVo">RListTraitMbtiQuestionInfoVo</h2>

<a id="schemarlisttraitmbtiquestioninfovo"></a>
<a id="schema_RListTraitMbtiQuestionInfoVo"></a>
<a id="tocSrlisttraitmbtiquestioninfovo"></a>
<a id="tocsrlisttraitmbtiquestioninfovo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "questionCode": "string",
      "questionTitle": "string",
      "questionType": "string",
      "orderNo": 0,
      "answers": [
        {
          "answerCode": "string",
          "answerName": "string",
          "showNo": "string"
        }
      ]
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[TraitMbtiQuestionInfoVo](#schematraitmbtiquestioninfovo)]|false|none||[MBTI性格特征]|

<h2 id="tocS_TraitMbtiQuestionAnswerInfoVo">TraitMbtiQuestionAnswerInfoVo</h2>

<a id="schematraitmbtiquestionanswerinfovo"></a>
<a id="schema_TraitMbtiQuestionAnswerInfoVo"></a>
<a id="tocStraitmbtiquestionanswerinfovo"></a>
<a id="tocstraitmbtiquestionanswerinfovo"></a>

```json
{
  "answerCode": "string",
  "answerName": "string",
  "showNo": "string"
}

```

MBTI性格特征

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|answerCode|string|false|none||问题答案编码|
|answerName|string|false|none||问题答案名称|
|showNo|string|false|none||问题答案显示顺序|

<h2 id="tocS_TraitMbtiQuestionInfoVo">TraitMbtiQuestionInfoVo</h2>

<a id="schematraitmbtiquestioninfovo"></a>
<a id="schema_TraitMbtiQuestionInfoVo"></a>
<a id="tocStraitmbtiquestioninfovo"></a>
<a id="tocstraitmbtiquestioninfovo"></a>

```json
{
  "questionCode": "string",
  "questionTitle": "string",
  "questionType": "string",
  "orderNo": 0,
  "answers": [
    {
      "answerCode": "string",
      "answerName": "string",
      "showNo": "string"
    }
  ]
}

```

MBTI性格特征

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|questionCode|string|false|none||问题编号|
|questionTitle|string|false|none||问题标题|
|questionType|string|false|none||none|
|orderNo|integer(int32)|false|none||none|
|answers|[[TraitMbtiQuestionAnswerInfoVo](#schematraitmbtiquestionanswerinfovo)]|false|none||问题答案|

<h2 id="tocS_CustomSettingVo">CustomSettingVo</h2>

<a id="schemacustomsettingvo"></a>
<a id="schema_CustomSettingVo"></a>
<a id="tocScustomsettingvo"></a>
<a id="tocscustomsettingvo"></a>

```json
{
  "id": 0,
  "customId": 0,
  "choose": 0,
  "blindBox": 0,
  "one2one": 0,
  "chooseIdentity": 0,
  "hideYearIncomeStatus": 0,
  "hideSchoolStatus": 0,
  "hidePersonalIntroStatus": 0,
  "hideLoveIntroStatus": 0,
  "hideHobbyStatus": 0,
  "hideIdealRemarkStatus": 0,
  "status": 0,
  "remark": "string",
  "testCode": "string"
}

```

用户个性设置视图对象 t_custom_setting

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|customId|integer(int64)|false|none||用户id|
|choose|integer(int32)|false|none||互选池：0-不加互选池，1-公域互选池，2-私域互选池|
|blindBox|integer(int32)|false|none||是否拆盲盒：1-打码照片展示 2-正常照片展示 3-无照片展示|
|one2one|integer(int32)|false|none||红娘1v1服务:0-不需要，1-需要|
|chooseIdentity|integer(int32)|false|none||身份：C1/C2/C3/C4/C5|
|hideYearIncomeStatus|integer(int32)|false|none||是否隐藏年收入：0 不隐藏 1 隐藏|
|hideSchoolStatus|integer(int32)|false|none||是否隐藏毕业学校 0 不隐藏 1 隐藏|
|hidePersonalIntroStatus|integer(int32)|false|none||none|
|hideLoveIntroStatus|integer(int32)|false|none||none|
|hideHobbyStatus|integer(int32)|false|none||none|
|hideIdealRemarkStatus|integer(int32)|false|none||none|
|status|integer(int32)|false|none||审核状态：0 待审核，1 审核通过|
|remark|string|false|none||备注|
|testCode|string|false|none||性格测试编码|

<h2 id="tocS_NoticeBo">NoticeBo</h2>

<a id="schemanoticebo"></a>
<a id="schema_NoticeBo"></a>
<a id="tocSnoticebo"></a>
<a id="tocsnoticebo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "typeId": 0,
  "content": "string",
  "status": 0,
  "remark": "string"
}

```

通知内容业务对象 t_notice

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||自增id|
|typeId|integer(int64)|true|none||类型id|
|content|string(string)|true|none||通知内容|
|status|integer(int64)|true|none||选择状态值 0=禁用 1=  启用|
|remark|string(string)|true|none||备注|

<h2 id="tocS_NoticeTypeBo">NoticeTypeBo</h2>

<a id="schemanoticetypebo"></a>
<a id="schema_NoticeTypeBo"></a>
<a id="tocSnoticetypebo"></a>
<a id="tocsnoticetypebo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "name": "string",
  "status": 0,
  "remark": "string"
}

```

通知类型业务对象 t_notice_type

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||客户id|
|name|string(string)|true|none||类型名|
|status|integer(int32)|false|none||选择状态值 0=禁用 1=  启用|
|remark|string(string)|true|none||备注|

<h2 id="tocS_NoticeTypeVo">NoticeTypeVo</h2>

<a id="schemanoticetypevo"></a>
<a id="schema_NoticeTypeVo"></a>
<a id="tocSnoticetypevo"></a>
<a id="tocsnoticetypevo"></a>

```json
{
  "id": 0,
  "name": "string",
  "status": 0,
  "remark": "string"
}

```

通知类型视图对象 t_notice_type

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||客户id|
|name|string|false|none||类型名|
|status|integer(int32)|false|none||选择状态值 0=禁用 1=  启用|
|remark|string|false|none||备注|

<h2 id="tocS_RNoticeTypeVo">RNoticeTypeVo</h2>

<a id="schemarnoticetypevo"></a>
<a id="schema_RNoticeTypeVo"></a>
<a id="tocSrnoticetypevo"></a>
<a id="tocsrnoticetypevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "name": "string",
    "status": 0,
    "remark": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[NoticeTypeVo](#schemanoticetypevo)|false|none||通知类型视图对象 t_notice_type|

<h2 id="tocS_TableDataInfoNoticeTypeVo">TableDataInfoNoticeTypeVo</h2>

<a id="schematabledatainfonoticetypevo"></a>
<a id="schema_TableDataInfoNoticeTypeVo"></a>
<a id="tocStabledatainfonoticetypevo"></a>
<a id="tocstabledatainfonoticetypevo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "name": "string",
      "status": 0,
      "remark": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[NoticeTypeVo](#schemanoticetypevo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RListNoticeTypeVo">RListNoticeTypeVo</h2>

<a id="schemarlistnoticetypevo"></a>
<a id="schema_RListNoticeTypeVo"></a>
<a id="tocSrlistnoticetypevo"></a>
<a id="tocsrlistnoticetypevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "id": 0,
      "name": "string",
      "status": 0,
      "remark": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[NoticeTypeVo](#schemanoticetypevo)]|false|none||[通知类型视图对象 t_notice_type]|

<h2 id="tocS_NoticeVo">NoticeVo</h2>

<a id="schemanoticevo"></a>
<a id="schema_NoticeVo"></a>
<a id="tocSnoticevo"></a>
<a id="tocsnoticevo"></a>

```json
{
  "id": 0,
  "typeId": 0,
  "typeName": "string",
  "content": "string",
  "status": 0,
  "remark": "string"
}

```

通知内容视图对象 t_notice

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|typeId|integer(int64)|false|none||类型id|
|typeName|string|false|none||类型名称|
|content|string|false|none||通知内容|
|status|integer(int64)|false|none||选择状态值 0=禁用 1=  启用|
|remark|string|false|none||备注|

<h2 id="tocS_RNoticeVo">RNoticeVo</h2>

<a id="schemarnoticevo"></a>
<a id="schema_RNoticeVo"></a>
<a id="tocSrnoticevo"></a>
<a id="tocsrnoticevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "typeId": 0,
    "typeName": "string",
    "content": "string",
    "status": 0,
    "remark": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[NoticeVo](#schemanoticevo)|false|none||通知内容视图对象 t_notice|

<h2 id="tocS_TableDataInfoNoticeVo">TableDataInfoNoticeVo</h2>

<a id="schematabledatainfonoticevo"></a>
<a id="schema_TableDataInfoNoticeVo"></a>
<a id="tocStabledatainfonoticevo"></a>
<a id="tocstabledatainfonoticevo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "typeId": 0,
      "typeName": "string",
      "content": "string",
      "status": 0,
      "remark": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[NoticeVo](#schemanoticevo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_PersonalInfo">PersonalInfo</h2>

<a id="schemapersonalinfo"></a>
<a id="schema_PersonalInfo"></a>
<a id="tocSpersonalinfo"></a>
<a id="tocspersonalinfo"></a>

```json
{
  "totalCollectCustom": 0,
  "numCollect": 0,
  "totalChooseCustom": 0,
  "numChoose": 0,
  "totalILikeCustom": 0,
  "numILike": 0,
  "totalLikeMeCustom": 0,
  "numLikeMe": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|totalCollectCustom|integer(int64)|false|none||总共收藏嘉宾|
|numCollect|integer(int64)|false|none||互选池收藏嘉宾|
|totalChooseCustom|integer(int64)|false|none||总共互选成功嘉宾|
|numChoose|integer(int64)|false|none||活动互选成功嘉宾|
|totalILikeCustom|integer(int64)|false|none||总共我喜欢的嘉宾|
|numILike|integer(int64)|false|none||今年我喜欢的嘉宾|
|totalLikeMeCustom|integer(int64)|false|none||总共喜欢我的嘉宾|
|numLikeMe|integer(int64)|false|none||今年喜欢的嘉宾|

<h2 id="tocS_RPersonalInfo">RPersonalInfo</h2>

<a id="schemarpersonalinfo"></a>
<a id="schema_RPersonalInfo"></a>
<a id="tocSrpersonalinfo"></a>
<a id="tocsrpersonalinfo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "totalCollectCustom": 0,
    "numCollect": 0,
    "totalChooseCustom": 0,
    "numChoose": 0,
    "totalILikeCustom": 0,
    "numILike": 0,
    "totalLikeMeCustom": 0,
    "numLikeMe": 0
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[PersonalInfo](#schemapersonalinfo)|false|none||none|

<h2 id="tocS_CustomChooseSuccessBo">CustomChooseSuccessBo</h2>

<a id="schemacustomchoosesuccessbo"></a>
<a id="schema_CustomChooseSuccessBo"></a>
<a id="tocScustomchoosesuccessbo"></a>
<a id="tocscustomchoosesuccessbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "customId": 0,
  "loverId": 0,
  "remark": "string",
  "type": 0
}

```

互选成功记录业务对象 t_custom_choose_success

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||自增id|
|customId|integer(int64)|true|none||主动方id|
|loverId|integer(int64)|true|none||被动方id|
|remark|string(string)|true|none||备注|
|type|integer(int32)|true|none||互选成功类型 0 活动互选 1 互选池互选|

<h2 id="tocS_CustomChooseSuccessVo">CustomChooseSuccessVo</h2>

<a id="schemacustomchoosesuccessvo"></a>
<a id="schema_CustomChooseSuccessVo"></a>
<a id="tocScustomchoosesuccessvo"></a>
<a id="tocscustomchoosesuccessvo"></a>

```json
{
  "id": 0,
  "customId": 0,
  "loverId": 0,
  "remark": "string",
  "type": 0,
  "updateTime": "2019-08-24T14:15:22Z"
}

```

互选成功记录视图对象 t_custom_choose_success

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|customId|integer(int64)|false|none||主动方id|
|loverId|integer(int64)|false|none||被动方id|
|remark|string|false|none||备注|
|type|integer(int32)|false|none||互选成功类型 0 活动互选 1 互选池互选|
|updateTime|string(date-time)|false|none||none|

<h2 id="tocS_RCustomChooseSuccessVo">RCustomChooseSuccessVo</h2>

<a id="schemarcustomchoosesuccessvo"></a>
<a id="schema_RCustomChooseSuccessVo"></a>
<a id="tocSrcustomchoosesuccessvo"></a>
<a id="tocsrcustomchoosesuccessvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "customId": 0,
    "loverId": 0,
    "remark": "string",
    "type": 0,
    "updateTime": "2019-08-24T14:15:22Z"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[CustomChooseSuccessVo](#schemacustomchoosesuccessvo)|false|none||互选成功记录视图对象 t_custom_choose_success|

<h2 id="tocS_TableDataInfoCustomChooseSuccessVo">TableDataInfoCustomChooseSuccessVo</h2>

<a id="schematabledatainfocustomchoosesuccessvo"></a>
<a id="schema_TableDataInfoCustomChooseSuccessVo"></a>
<a id="tocStabledatainfocustomchoosesuccessvo"></a>
<a id="tocstabledatainfocustomchoosesuccessvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "customId": 0,
      "loverId": 0,
      "remark": "string",
      "type": 0,
      "updateTime": "2019-08-24T14:15:22Z"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[CustomChooseSuccessVo](#schemacustomchoosesuccessvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_WxMsgConfigBo">WxMsgConfigBo</h2>

<a id="schemawxmsgconfigbo"></a>
<a id="schema_WxMsgConfigBo"></a>
<a id="tocSwxmsgconfigbo"></a>
<a id="tocswxmsgconfigbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "appId": "string",
  "msgType": 0,
  "subType": 0,
  "subTypeName": "string",
  "msgTemplateId": "string",
  "jumpUrl": "string",
  "remark": "string",
  "delFlag": "string",
  "enable": 0,
  "paramOne": "string",
  "paramTwo": "string",
  "paramThree": "string",
  "paramFour": "string",
  "paramFive": "string",
  "paramRemark": "string"
}

```

微信模板消息配置业务对象 t_wx_msg_config

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||自增id|
|appId|string(string)|true|none||应用编号|
|msgType|integer(int32)|true|none||消息类型|
|subType|integer(int32)|true|none||none|
|subTypeName|string(string)|true|none||none|
|msgTemplateId|string(string)|true|none||消息模板id|
|jumpUrl|string(string)|false|none||消息模板跳转url|
|remark|string(string)|false|none||备注|
|delFlag|string(string)|false|none||逻辑删除：0 正常，1 删除|
|enable|integer(int32)|true|none||启用状态 0 启用  1 禁用|
|paramOne|string(string)|false|none||none|
|paramTwo|string(string)|false|none||none|
|paramThree|string(string)|false|none||none|
|paramFour|string(string)|false|none||none|
|paramFive|string(string)|false|none||none|
|paramRemark|string(string)|false|none||none|

<h2 id="tocS_PayInfoBo">PayInfoBo</h2>

<a id="schemapayinfobo"></a>
<a id="schema_PayInfoBo"></a>
<a id="tocSpayinfobo"></a>
<a id="tocspayinfobo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "orderNo": "string",
  "outTradeNo": "string",
  "payPlatform": 0,
  "payClient": 0,
  "payScene": 0,
  "payStatus": 0,
  "payAmount": 0,
  "refundAmount": 0,
  "payType": 0,
  "remark": "string"
}

```

支付信息业务对象 t_pay_info

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||支付信息自增ID|
|orderNo|string(string)|true|none||订单号|
|outTradeNo|string(string)|true|none||交易单号|
|payPlatform|integer(int32)|true|none||支付平台，1-微信，2-支付宝，3-通联，4-聚合|
|payClient|integer(int32)|true|none||支付设备，1-手机，2-电脑，3-其它|
|payScene|integer(int32)|true|none||支付场景，1-小程序端，2-h5端，3-PC端|
|payStatus|integer(int32)|true|none||支付状态  0 未支付  1 已支付 2 退款|
|payAmount|number(number)|true|none||支付金额|
|refundAmount|number(number)|true|none||退款金额|
|payType|integer(int32)|true|none||支付类型，0-活动支付，1-互选池支付，2-其它|
|remark|string(string)|true|none||备注|

<h2 id="tocS_ActivityEnrollVo">ActivityEnrollVo</h2>

<a id="schemaactivityenrollvo"></a>
<a id="schema_ActivityEnrollVo"></a>
<a id="tocSactivityenrollvo"></a>
<a id="tocsactivityenrollvo"></a>

```json
{
  "ordersNo": "string",
  "enrollStatus": 0,
  "enrollStatusName": "string",
  "verifyStatusName": "string"
}

```

活动列表视图对象 t_activity

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|ordersNo|string|false|none||活动报名订单号|
|enrollStatus|integer(int32)|false|none||报名状态 0 未报名 1 未支付,报名中  2 已支付,报名成功  3 报名失败，全额退款|
|enrollStatusName|string|false|none||报名状态 0 未报名 1 未支付,报名中 2 已支付,报名成功  3 报名失败，全额退款|
|verifyStatusName|string|false|none||三重认证验证, Uncertified-未认证, Certified-已认证|

<h2 id="tocS_RActivityEnrollVo">RActivityEnrollVo</h2>

<a id="schemaractivityenrollvo"></a>
<a id="schema_RActivityEnrollVo"></a>
<a id="tocSractivityenrollvo"></a>
<a id="tocsractivityenrollvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "ordersNo": "string",
    "enrollStatus": 0,
    "enrollStatusName": "string",
    "verifyStatusName": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[ActivityEnrollVo](#schemaactivityenrollvo)|false|none||活动列表视图对象 t_activity|

<h2 id="tocS_RWxMsgConfigVo">RWxMsgConfigVo</h2>

<a id="schemarwxmsgconfigvo"></a>
<a id="schema_RWxMsgConfigVo"></a>
<a id="tocSrwxmsgconfigvo"></a>
<a id="tocsrwxmsgconfigvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "appId": "string",
    "msgType": 0,
    "subType": 0,
    "subTypeName": "string",
    "msgTemplateId": "string",
    "jumpUrl": "string",
    "enable": 0,
    "remark": "string",
    "delFlag": "string",
    "appName": "string",
    "msgTypeName": "string",
    "paramOne": "string",
    "paramTwo": "string",
    "paramThree": "string",
    "paramFour": "string",
    "paramFive": "string",
    "paramRemark": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[WxMsgConfigVo](#schemawxmsgconfigvo)|false|none||微信模板消息配置视图对象 t_wx_msg_config|

<h2 id="tocS_WxMsgConfigVo">WxMsgConfigVo</h2>

<a id="schemawxmsgconfigvo"></a>
<a id="schema_WxMsgConfigVo"></a>
<a id="tocSwxmsgconfigvo"></a>
<a id="tocswxmsgconfigvo"></a>

```json
{
  "id": 0,
  "appId": "string",
  "msgType": 0,
  "subType": 0,
  "subTypeName": "string",
  "msgTemplateId": "string",
  "jumpUrl": "string",
  "enable": 0,
  "remark": "string",
  "delFlag": "string",
  "appName": "string",
  "msgTypeName": "string",
  "paramOne": "string",
  "paramTwo": "string",
  "paramThree": "string",
  "paramFour": "string",
  "paramFive": "string",
  "paramRemark": "string"
}

```

微信模板消息配置视图对象 t_wx_msg_config

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|appId|string|false|none||应用编号|
|msgType|integer(int32)|false|none||消息类型|
|subType|integer(int32)|false|none||none|
|subTypeName|string|false|none||none|
|msgTemplateId|string|false|none||消息模板id|
|jumpUrl|string|false|none||消息模板跳转url|
|enable|integer(int32)|false|none||启用状态，0:禁用 1:启用|
|remark|string|false|none||备注|
|delFlag|string|false|none||逻辑删除：0 正常，1 删除|
|appName|string|false|none||none|
|msgTypeName|string|false|none||none|
|paramOne|string|false|none||none|
|paramTwo|string|false|none||none|
|paramThree|string|false|none||none|
|paramFour|string|false|none||none|
|paramFive|string|false|none||none|
|paramRemark|string|false|none||none|

<h2 id="tocS_TableDataInfoWxMsgConfigVo">TableDataInfoWxMsgConfigVo</h2>

<a id="schematabledatainfowxmsgconfigvo"></a>
<a id="schema_TableDataInfoWxMsgConfigVo"></a>
<a id="tocStabledatainfowxmsgconfigvo"></a>
<a id="tocstabledatainfowxmsgconfigvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "appId": "string",
      "msgType": 0,
      "subType": 0,
      "subTypeName": "string",
      "msgTemplateId": "string",
      "jumpUrl": "string",
      "enable": 0,
      "remark": "string",
      "delFlag": "string",
      "appName": "string",
      "msgTypeName": "string",
      "paramOne": "string",
      "paramTwo": "string",
      "paramThree": "string",
      "paramFour": "string",
      "paramFive": "string",
      "paramRemark": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[WxMsgConfigVo](#schemawxmsgconfigvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_PayInfoVo">PayInfoVo</h2>

<a id="schemapayinfovo"></a>
<a id="schema_PayInfoVo"></a>
<a id="tocSpayinfovo"></a>
<a id="tocspayinfovo"></a>

```json
{
  "id": 0,
  "orderNo": "string",
  "outTradeNo": "string",
  "payPlatform": 0,
  "payClient": 0,
  "payScene": 0,
  "payStatus": 0,
  "payAmount": 0,
  "refundAmount": 0,
  "payType": 0,
  "remark": "string"
}

```

支付信息视图对象 t_pay_info

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||支付信息自增ID|
|orderNo|string|false|none||订单号|
|outTradeNo|string|false|none||交易单号|
|payPlatform|integer(int32)|false|none||支付平台，1-支付宝，2-微信，3-通联，4-聚合|
|payClient|integer(int32)|false|none||支付设备，1-手机，2-电脑，3-其它|
|payScene|integer(int32)|false|none||支付场景，1-小程序端，2-h5端，3-PC端|
|payStatus|integer(int32)|false|none||支付状态  0 未支付  1 已支付 2 退款|
|payAmount|number|false|none||支付金额|
|refundAmount|number|false|none||退款金额|
|payType|integer(int32)|false|none||支付类型，0-活动支付，1-互选池支付，2-其它|
|remark|string|false|none||备注|

<h2 id="tocS_RPayInfoVo">RPayInfoVo</h2>

<a id="schemarpayinfovo"></a>
<a id="schema_RPayInfoVo"></a>
<a id="tocSrpayinfovo"></a>
<a id="tocsrpayinfovo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "orderNo": "string",
    "outTradeNo": "string",
    "payPlatform": 0,
    "payClient": 0,
    "payScene": 0,
    "payStatus": 0,
    "payAmount": 0,
    "refundAmount": 0,
    "payType": 0,
    "remark": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[PayInfoVo](#schemapayinfovo)|false|none||支付信息视图对象 t_pay_info|

<h2 id="tocS_TableDataInfoPayInfoVo">TableDataInfoPayInfoVo</h2>

<a id="schematabledatainfopayinfovo"></a>
<a id="schema_TableDataInfoPayInfoVo"></a>
<a id="tocStabledatainfopayinfovo"></a>
<a id="tocstabledatainfopayinfovo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "orderNo": "string",
      "outTradeNo": "string",
      "payPlatform": 0,
      "payClient": 0,
      "payScene": 0,
      "payStatus": 0,
      "payAmount": 0,
      "refundAmount": 0,
      "payType": 0,
      "remark": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[PayInfoVo](#schemapayinfovo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_WxCodeLoginDto">WxCodeLoginDto</h2>

<a id="schemawxcodelogindto"></a>
<a id="schema_WxCodeLoginDto"></a>
<a id="tocSwxcodelogindto"></a>
<a id="tocswxcodelogindto"></a>

```json
{
  "code": "string",
  "openid": "string",
  "brandType": 0,
  "referrer": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|string|true|none||none|
|openid|string|true|none||openid|
|brandType|integer(int32)|false|none||品牌类型 1=yxr 2=jxh 3=mbti|
|referrer|string|false|none||推荐人|

<h2 id="tocS_SocialGroupBo">SocialGroupBo</h2>

<a id="schemasocialgroupbo"></a>
<a id="schema_SocialGroupBo"></a>
<a id="tocSsocialgroupbo"></a>
<a id="tocssocialgroupbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "typeId": 0,
  "groupName": "string",
  "groupUrl": "string",
  "remark": "string",
  "enable": 0
}

```

社群业务对象 t_social_group

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||自增id|
|typeId|integer(int64)|true|none||社群类型id|
|groupName|string(string)|true|none||社群名称|
|groupUrl|string(string)|true|none||社群二维码图片url|
|remark|string(string)|false|none||备注|
|enable|integer(int32)|true|none||0 启用  1 禁用|

<h2 id="tocS_SocialGroupTypeBo">SocialGroupTypeBo</h2>

<a id="schemasocialgrouptypebo"></a>
<a id="schema_SocialGroupTypeBo"></a>
<a id="tocSsocialgrouptypebo"></a>
<a id="tocssocialgrouptypebo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "typeName": "string",
  "remark": "string",
  "enable": 0
}

```

社群类型业务对象 t_social_group_type

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||自增id|
|typeName|string(string)|true|none||社群类型名|
|remark|string(string)|false|none||备注|
|enable|integer(int32)|true|none||0 启用  1 禁用|

<h2 id="tocS_RWxLoginVo">RWxLoginVo</h2>

<a id="schemarwxloginvo"></a>
<a id="schema_RWxLoginVo"></a>
<a id="tocSrwxloginvo"></a>
<a id="tocsrwxloginvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "isNew": 0,
    "token": "string",
    "openid": "string",
    "phoneNumber": "string",
    "platformType": 0,
    "customId": 0,
    "brandType": 0
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[WxLoginVo](#schemawxloginvo)|false|none||none|

<h2 id="tocS_WxLoginVo">WxLoginVo</h2>

<a id="schemawxloginvo"></a>
<a id="schema_WxLoginVo"></a>
<a id="tocSwxloginvo"></a>
<a id="tocswxloginvo"></a>

```json
{
  "isNew": 0,
  "token": "string",
  "openid": "string",
  "phoneNumber": "string",
  "platformType": 0,
  "customId": 0,
  "brandType": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|isNew|integer(int32)|false|none||是否新用户  0-非新用户 1-新用户|
|token|string|false|none||登录token|
|openid|string|false|none||登录openid|
|phoneNumber|string|false|none||手机号（其次关联）|
|platformType|integer(int32)|false|none||客户类型： 0 h5用户 1 小程序用户|
|customId|integer(int64)|false|none||客户id|
|brandType|integer(int32)|false|none||品牌： 1 yxr 2jxh 3 Mbti|

<h2 id="tocS_MbtiResultListQueryDto">MbtiResultListQueryDto</h2>

<a id="schemambtiresultlistquerydto"></a>
<a id="schema_MbtiResultListQueryDto"></a>
<a id="tocSmbtiresultlistquerydto"></a>
<a id="tocsmbtiresultlistquerydto"></a>

```json
{
  "infoCode": "string"
}

```

MBTI性格特征

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|infoCode|string|false|none||性格信息编码|

<h2 id="tocS_MbtiQuestionTestParam">MbtiQuestionTestParam</h2>

<a id="schemambtiquestiontestparam"></a>
<a id="schema_MbtiQuestionTestParam"></a>
<a id="tocSmbtiquestiontestparam"></a>
<a id="tocsmbtiquestiontestparam"></a>

```json
{
  "infoCode": "string",
  "testParams": [
    {
      "questionCode": "string",
      "answerCode": "string"
    }
  ]
}

```

问题测试查询参数

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|infoCode|string|true|none||性格信息编码|
|testParams|[[MbtiTestDimScoreDto](#schemambtitestdimscoredto)]|true|none||性格测试问题答案|

<h2 id="tocS_MbtiTestDimScoreDto">MbtiTestDimScoreDto</h2>

<a id="schemambtitestdimscoredto"></a>
<a id="schema_MbtiTestDimScoreDto"></a>
<a id="tocSmbtitestdimscoredto"></a>
<a id="tocsmbtitestdimscoredto"></a>

```json
{
  "questionCode": "string",
  "answerCode": "string"
}

```

性格测试维度得分

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|questionCode|string|false|none||问题编号|
|answerCode|string|false|none||问题编码|

<h2 id="tocS_MbtiInfoQuestionQueryDto">MbtiInfoQuestionQueryDto</h2>

<a id="schemambtiinfoquestionquerydto"></a>
<a id="schema_MbtiInfoQuestionQueryDto"></a>
<a id="tocSmbtiinfoquestionquerydto"></a>
<a id="tocsmbtiinfoquestionquerydto"></a>

```json
{
  "infoCode": "string"
}

```

问题测试查询参数

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|infoCode|string|true|none||性格信息编码|

<h2 id="tocS_RSocialGroupTypeVo">RSocialGroupTypeVo</h2>

<a id="schemarsocialgrouptypevo"></a>
<a id="schema_RSocialGroupTypeVo"></a>
<a id="tocSrsocialgrouptypevo"></a>
<a id="tocsrsocialgrouptypevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "typeName": "string",
    "enable": 0
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[SocialGroupTypeVo](#schemasocialgrouptypevo)|false|none||社群类型视图对象 t_social_group_type|

<h2 id="tocS_SocialGroupTypeVo">SocialGroupTypeVo</h2>

<a id="schemasocialgrouptypevo"></a>
<a id="schema_SocialGroupTypeVo"></a>
<a id="tocSsocialgrouptypevo"></a>
<a id="tocssocialgrouptypevo"></a>

```json
{
  "id": 0,
  "typeName": "string",
  "enable": 0
}

```

社群类型视图对象 t_social_group_type

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|typeName|string|false|none||社群类型名|
|enable|integer(int32)|false|none||0 启用  1 禁用|

<h2 id="tocS_TableDataInfoSocialGroupTypeVo">TableDataInfoSocialGroupTypeVo</h2>

<a id="schematabledatainfosocialgrouptypevo"></a>
<a id="schema_TableDataInfoSocialGroupTypeVo"></a>
<a id="tocStabledatainfosocialgrouptypevo"></a>
<a id="tocstabledatainfosocialgrouptypevo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "typeName": "string",
      "enable": 0
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[SocialGroupTypeVo](#schemasocialgrouptypevo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RSocialGroupVo">RSocialGroupVo</h2>

<a id="schemarsocialgroupvo"></a>
<a id="schema_RSocialGroupVo"></a>
<a id="tocSrsocialgroupvo"></a>
<a id="tocsrsocialgroupvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "typeId": 0,
    "groupName": "string",
    "groupUrl": "string",
    "remark": "string",
    "enable": 0,
    "typeName": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[SocialGroupVo](#schemasocialgroupvo)|false|none||社群视图对象 t_social_group|

<h2 id="tocS_SocialGroupVo">SocialGroupVo</h2>

<a id="schemasocialgroupvo"></a>
<a id="schema_SocialGroupVo"></a>
<a id="tocSsocialgroupvo"></a>
<a id="tocssocialgroupvo"></a>

```json
{
  "id": 0,
  "typeId": 0,
  "groupName": "string",
  "groupUrl": "string",
  "remark": "string",
  "enable": 0,
  "typeName": "string"
}

```

社群视图对象 t_social_group

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|typeId|integer(int64)|false|none||社群类型id|
|groupName|string|false|none||社群名称|
|groupUrl|string|false|none||社群二维码图片url|
|remark|string|false|none||备注|
|enable|integer(int32)|false|none||0 启用  1 禁用|
|typeName|string|false|none||社群类型名|

<h2 id="tocS_TableDataInfoSocialGroupVo">TableDataInfoSocialGroupVo</h2>

<a id="schematabledatainfosocialgroupvo"></a>
<a id="schema_TableDataInfoSocialGroupVo"></a>
<a id="tocStabledatainfosocialgroupvo"></a>
<a id="tocstabledatainfosocialgroupvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "typeId": 0,
      "groupName": "string",
      "groupUrl": "string",
      "remark": "string",
      "enable": 0,
      "typeName": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[SocialGroupVo](#schemasocialgroupvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RListSocialGroupTypeBaseVo">RListSocialGroupTypeBaseVo</h2>

<a id="schemarlistsocialgrouptypebasevo"></a>
<a id="schema_RListSocialGroupTypeBaseVo"></a>
<a id="tocSrlistsocialgrouptypebasevo"></a>
<a id="tocsrlistsocialgrouptypebasevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "id": 0,
      "typeName": "string",
      "groupList": [
        {
          "id": 0,
          "typeId": 0,
          "groupName": "string",
          "groupUrl": "string"
        }
      ]
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[SocialGroupTypeBaseVo](#schemasocialgrouptypebasevo)]|false|none||[社群类型视图对象 t_social_group_type]|

<h2 id="tocS_SocialGroupBaseVo">SocialGroupBaseVo</h2>

<a id="schemasocialgroupbasevo"></a>
<a id="schema_SocialGroupBaseVo"></a>
<a id="tocSsocialgroupbasevo"></a>
<a id="tocssocialgroupbasevo"></a>

```json
{
  "id": 0,
  "typeId": 0,
  "groupName": "string",
  "groupUrl": "string"
}

```

社群视图对象 t_social_group

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|typeId|integer(int64)|false|none||社群类型id|
|groupName|string|false|none||社群名称|
|groupUrl|string|false|none||社群二维码图片url|

<h2 id="tocS_SocialGroupTypeBaseVo">SocialGroupTypeBaseVo</h2>

<a id="schemasocialgrouptypebasevo"></a>
<a id="schema_SocialGroupTypeBaseVo"></a>
<a id="tocSsocialgrouptypebasevo"></a>
<a id="tocssocialgrouptypebasevo"></a>

```json
{
  "id": 0,
  "typeName": "string",
  "groupList": [
    {
      "id": 0,
      "typeId": 0,
      "groupName": "string",
      "groupUrl": "string"
    }
  ]
}

```

社群类型视图对象 t_social_group_type

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|typeName|string|false|none||社群类型名|
|groupList|[[SocialGroupBaseVo](#schemasocialgroupbasevo)]|false|none||社群列表|

<h2 id="tocS_RListAppMsgVo">RListAppMsgVo</h2>

<a id="schemarlistappmsgvo"></a>
<a id="schema_RListAppMsgVo"></a>
<a id="tocSrlistappmsgvo"></a>
<a id="tocsrlistappmsgvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "id": 0,
      "receiverId": 0,
      "senderId": 0,
      "msgType": 0,
      "readFlag": 0,
      "title": "string",
      "content": "string",
      "delCustomIds": "string",
      "remark": "string",
      "msgTypeName": "string",
      "createTime": "2019-08-24T14:15:22Z"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[AppMsgVo](#schemaappmsgvo)]|false|none||[站内信息视图对象 t_app_msg]|

<h2 id="tocS_RInteger">RInteger</h2>

<a id="schemarinteger"></a>
<a id="schema_RInteger"></a>
<a id="tocSrinteger"></a>
<a id="tocsrinteger"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": 0
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|integer(int32)|false|none||none|

<h2 id="tocS_CustomVerifyStatusVo">CustomVerifyStatusVo</h2>

<a id="schemacustomverifystatusvo"></a>
<a id="schema_CustomVerifyStatusVo"></a>
<a id="tocScustomverifystatusvo"></a>
<a id="tocscustomverifystatusvo"></a>

```json
{
  "nameVerifyStatus": 0,
  "nameVerifyStatusName": "string",
  "educationVerifyStatus": 0,
  "educationVerifyStatusName": "string",
  "jobVerifyStatus": 0,
  "jobVerifyStatusName": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|nameVerifyStatus|integer(int32)|false|none||实名认证状态 0-认证中|1-实名认证成功|2-实名认证失败|
|nameVerifyStatusName|string|false|none||实名认证状态：In_Certification-认证中, Certification_Successful-认证成功,Certification_Failed-认证失败|
|educationVerifyStatus|integer(int32)|false|none||学历认证状态 0-认证中|1-实名认证成功|2-实名认证失败|
|educationVerifyStatusName|string|false|none||学历认证状态：In_Certification-认证中, Certification_Successful-认证成功,Certification_Failed-认证失败|
|jobVerifyStatus|integer(int32)|false|none||工作认证状态 0-认证中|1-实名认证成功|2-实名认证失败|
|jobVerifyStatusName|string|false|none||工作认证状态：In_Certification-认证中, Certification_Successful-认证成功,Certification_Failed-认证失败|

<h2 id="tocS_RCustomVerifyStatusVo">RCustomVerifyStatusVo</h2>

<a id="schemarcustomverifystatusvo"></a>
<a id="schema_RCustomVerifyStatusVo"></a>
<a id="tocSrcustomverifystatusvo"></a>
<a id="tocsrcustomverifystatusvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "nameVerifyStatus": 0,
    "nameVerifyStatusName": "string",
    "educationVerifyStatus": 0,
    "educationVerifyStatusName": "string",
    "jobVerifyStatus": 0,
    "jobVerifyStatusName": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[CustomVerifyStatusVo](#schemacustomverifystatusvo)|false|none||none|

<h2 id="tocS_ChooseDto">ChooseDto</h2>

<a id="schemachoosedto"></a>
<a id="schema_ChooseDto"></a>
<a id="tocSchoosedto"></a>
<a id="tocschoosedto"></a>

```json
{
  "blindBox": 0,
  "shareId": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|blindBox|integer(int32)|true|none||是否拆盲盒：1-拆盲盒展示[打码照片] 2-非拆盲盒展示[正常照片] 3-无照片展示|
|shareId|string(string)|false|none||分享编号|

<h2 id="tocS_CustomVerifyReqBo">CustomVerifyReqBo</h2>

<a id="schemacustomverifyreqbo"></a>
<a id="schema_CustomVerifyReqBo"></a>
<a id="tocScustomverifyreqbo"></a>
<a id="tocscustomverifyreqbo"></a>

```json
{
  "customerId": 0
}

```

查询用户认证状态请求

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|customerId|integer(int64)|false|none||用户编号|

<h2 id="tocS_RListString">RListString</h2>

<a id="schemarliststring"></a>
<a id="schema_RListString"></a>
<a id="tocSrliststring"></a>
<a id="tocsrliststring"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    "string"
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[string]|false|none||none|

<h2 id="tocS_CustomImageItemVo">CustomImageItemVo</h2>

<a id="schemacustomimageitemvo"></a>
<a id="schema_CustomImageItemVo"></a>
<a id="tocScustomimageitemvo"></a>
<a id="tocscustomimageitemvo"></a>

```json
{
  "imageType": 0,
  "imageUrl": "string"
}

```

照片管理视图对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|imageType|integer(int32)|false|none||图片类型, 0=主图，1=盲盒照片，2=非盲盒照片|
|imageUrl|string|false|none||图片链接, 每项仅限一张图片|

<h2 id="tocS_CustomImageListVo">CustomImageListVo</h2>

<a id="schemacustomimagelistvo"></a>
<a id="schema_CustomImageListVo"></a>
<a id="tocScustomimagelistvo"></a>
<a id="tocscustomimagelistvo"></a>

```json
{
  "imageId": 0,
  "customId": 0,
  "images": [
    {
      "imageType": 0,
      "imageUrl": "string"
    }
  ]
}

```

照片管理视图对象 t_custom_image

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|imageId|integer(int64)|false|none||自增id|
|customId|integer(int64)|false|none||关联客户id|
|images|[[CustomImageItemVo](#schemacustomimageitemvo)]|false|none||照片|

<h2 id="tocS_RCustomImageListVo">RCustomImageListVo</h2>

<a id="schemarcustomimagelistvo"></a>
<a id="schema_RCustomImageListVo"></a>
<a id="tocSrcustomimagelistvo"></a>
<a id="tocsrcustomimagelistvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "imageId": 0,
    "customId": 0,
    "images": [
      {
        "imageType": 0,
        "imageUrl": "string"
      }
    ]
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[CustomImageListVo](#schemacustomimagelistvo)|false|none||照片管理视图对象 t_custom_image|

<h2 id="tocS_RecommendDto">RecommendDto</h2>

<a id="schemarecommenddto"></a>
<a id="schema_RecommendDto"></a>
<a id="tocSrecommenddto"></a>
<a id="tocsrecommenddto"></a>

```json
{
  "amount": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|amount|integer(int32)|true|none||每日每种类型推荐数量|

<h2 id="tocS_AppMsgListVo">AppMsgListVo</h2>

<a id="schemaappmsglistvo"></a>
<a id="schema_AppMsgListVo"></a>
<a id="tocSappmsglistvo"></a>
<a id="tocsappmsglistvo"></a>

```json
{
  "senderId": 0,
  "senderName": "string",
  "senderAvatarUrl": "string",
  "receiverId": 0,
  "receiverName": "string",
  "receiverAvatarUrl": "string",
  "msgList": [
    {
      "id": 0,
      "receiverId": 0,
      "senderId": 0,
      "msgType": 0,
      "readFlag": 0,
      "title": "string",
      "content": "string",
      "delCustomIds": "string",
      "remark": "string",
      "msgTypeName": "string",
      "createTime": "2019-08-24T14:15:22Z"
    }
  ],
  "sortTime": "2019-08-24T14:15:22Z",
  "unreadNum": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|senderId|integer(int64)|false|none||none|
|senderName|string|false|none||none|
|senderAvatarUrl|string|false|none||none|
|receiverId|integer(int64)|false|none||none|
|receiverName|string|false|none||none|
|receiverAvatarUrl|string|false|none||none|
|msgList|[[AppMsgVo](#schemaappmsgvo)]|false|none||[站内信息视图对象 t_app_msg]|
|sortTime|string(date-time)|false|none||none|
|unreadNum|integer(int32)|false|none||none|

<h2 id="tocS_RListAppMsgListVo">RListAppMsgListVo</h2>

<a id="schemarlistappmsglistvo"></a>
<a id="schema_RListAppMsgListVo"></a>
<a id="tocSrlistappmsglistvo"></a>
<a id="tocsrlistappmsglistvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "senderId": 0,
      "senderName": "string",
      "senderAvatarUrl": "string",
      "receiverId": 0,
      "receiverName": "string",
      "receiverAvatarUrl": "string",
      "msgList": [
        {
          "id": 0,
          "receiverId": 0,
          "senderId": 0,
          "msgType": 0,
          "readFlag": 0,
          "title": "string",
          "content": "string",
          "delCustomIds": "string",
          "remark": "string",
          "msgTypeName": "string",
          "createTime": "2019-08-24T14:15:22Z"
        }
      ],
      "sortTime": "2019-08-24T14:15:22Z",
      "unreadNum": 0
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[AppMsgListVo](#schemaappmsglistvo)]|false|none||none|

<h2 id="tocS_AppMsgReadDto">AppMsgReadDto</h2>

<a id="schemaappmsgreaddto"></a>
<a id="schema_AppMsgReadDto"></a>
<a id="tocSappmsgreaddto"></a>
<a id="tocsappmsgreaddto"></a>

```json
{
  "senderId": 0
}

```

站内消息读

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|senderId|integer(int64)|true|none||消息发送人ID|

<h2 id="tocS_AppMsgSendDto">AppMsgSendDto</h2>

<a id="schemaappmsgsenddto"></a>
<a id="schema_AppMsgSendDto"></a>
<a id="tocSappmsgsenddto"></a>
<a id="tocsappmsgsenddto"></a>

```json
{
  "receiverId": 0,
  "msgType": 0,
  "title": "string",
  "content": "string"
}

```

站内消息读

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|receiverId|integer(int64)|true|none||消息接收人ID|
|msgType|integer(int32)|false|none||消息类型|
|title|string|false|none||消息标题|
|content|string|true|none||消息内容|

<h2 id="tocS_CustomImageInfoVo">CustomImageInfoVo</h2>

<a id="schemacustomimageinfovo"></a>
<a id="schema_CustomImageInfoVo"></a>
<a id="tocScustomimageinfovo"></a>
<a id="tocscustomimageinfovo"></a>

```json
{
  "personalImageUrls": [
    "string"
  ],
  "blindImageUrls": [
    "string"
  ],
  "imageUrls": [
    "string"
  ]
}

```

照片管理视图

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|personalImageUrls|[string]|false|none||none|
|blindImageUrls|[string]|false|none||none|
|imageUrls|[string]|false|none||none|

<h2 id="tocS_VipBo">VipBo</h2>

<a id="schemavipbo"></a>
<a id="schema_VipBo"></a>
<a id="tocSvipbo"></a>
<a id="tocsvipbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "typeId": 0,
  "price": 0,
  "discountPrice": 0,
  "remark": "string",
  "bgColor": "string",
  "validTimeUnit": 0,
  "validTime": 0,
  "vipName": "string",
  "sortNum": 0
}

```

会员配置业务对象 t_vip

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||客户id|
|typeId|integer(int64)|true|none||会员类型id|
|price|number(number)|true|none||会员价格|
|discountPrice|number(number)|true|none||会员折扣价格|
|remark|string(string)|false|none||备注|
|bgColor|string(string)|false|none||背景颜色值|
|validTimeUnit|integer(int32)|false|none||有效时长单位，周，月，季，年|
|validTime|integer(int32)|false|none||有效时长(周期)，表示几周，几个月|
|vipName|string(string)|false|none||会员名称|
|sortNum|integer(int32)|false|none||排序|

<h2 id="tocS_VipTypeBo">VipTypeBo</h2>

<a id="schemaviptypebo"></a>
<a id="schema_VipTypeBo"></a>
<a id="tocSviptypebo"></a>
<a id="tocsviptypebo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "name": "string",
  "remark": "string",
  "ename": "string"
}

```

会员类型业务对象 t_vip_type

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||客户id|
|name|string(string)|true|none||会员类型名称|
|remark|string(string)|false|none||备注|
|ename|string(string)|false|none||none|

<h2 id="tocS_PlatformBo">PlatformBo</h2>

<a id="schemaplatformbo"></a>
<a id="schema_PlatformBo"></a>
<a id="tocSplatformbo"></a>
<a id="tocsplatformbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "name": "string",
  "channel": "string",
  "remark": "string",
  "enable": 0
}

```

平台业务对象 t_platform

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||自增id|
|name|string(string)|true|none||平台名称|
|channel|string(string)|false|none||开放渠道|
|remark|string(string)|false|none||备注|
|enable|integer(int32)|true|none||启用状态，0 启用  1 禁用|

<h2 id="tocS_PlatformAuthChannelDto">PlatformAuthChannelDto</h2>

<a id="schemaplatformauthchanneldto"></a>
<a id="schema_PlatformAuthChannelDto"></a>
<a id="tocSplatformauthchanneldto"></a>
<a id="tocsplatformauthchanneldto"></a>

```json
{
  "platformId": 0,
  "channelIds": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|platformId|integer(int64)|true|none||none|
|channelIds|string|false|none||none|

<h2 id="tocS_CustomVipBo">CustomVipBo</h2>

<a id="schemacustomvipbo"></a>
<a id="schema_CustomVipBo"></a>
<a id="tocScustomvipbo"></a>
<a id="tocscustomvipbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "vipId": 0,
  "customId": 0,
  "price": 0,
  "discountPrice": 0,
  "startTime": "2019-08-24T14:15:22Z",
  "endTime": "2019-08-24T14:15:22Z",
  "remark": "string",
  "vipName": "string"
}

```

会员管理业务对象 t_custom_vip

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||自增id|
|vipId|integer(int64)|true|none||会员id|
|customId|integer(int64)|true|none||用户id|
|price|number(number)|true|none||会员价格|
|discountPrice|number(number)|true|none||会员折扣价格|
|startTime|string(date-time)|true|none||会员卡开始时间|
|endTime|string(date-time)|false|none||会员卡结束时间|
|remark|string(string)|false|none||备注|
|vipName|string(string)|false|none||会员名称|

<h2 id="tocS_ChannelBo">ChannelBo</h2>

<a id="schemachannelbo"></a>
<a id="schema_ChannelBo"></a>
<a id="tocSchannelbo"></a>
<a id="tocschannelbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "type": 0,
  "name": "string",
  "remark": "string",
  "enable": 0
}

```

渠道业务对象 t_channel

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||自增id|
|type|integer(int64)|true|none||渠道类型|
|name|string(string)|true|none||渠道名称|
|remark|string(string)|false|none||备注|
|enable|integer(int32)|true|none||启用状态，0 启用  1 禁用|

<h2 id="tocS_ClaimMemberShipDto">ClaimMemberShipDto</h2>

<a id="schemaclaimmembershipdto"></a>
<a id="schema_ClaimMemberShipDto"></a>
<a id="tocSclaimmembershipdto"></a>
<a id="tocsclaimmembershipdto"></a>

```json
{
  "memberShipType": "string",
  "action": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|memberShipType|string|true|none||会员类型： cMember=创始人会员,gMember=股东会员,hMember=核心会员,pMember=普通会员|
|action|string|true|none||none|

<h2 id="tocS_RVipTypeVo">RVipTypeVo</h2>

<a id="schemarviptypevo"></a>
<a id="schema_RVipTypeVo"></a>
<a id="tocSrviptypevo"></a>
<a id="tocsrviptypevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "name": "string",
    "remark": "string",
    "ename": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[VipTypeVo](#schemaviptypevo)|false|none||会员类型视图对象 t_vip_type|

<h2 id="tocS_VipTypeVo">VipTypeVo</h2>

<a id="schemaviptypevo"></a>
<a id="schema_VipTypeVo"></a>
<a id="tocSviptypevo"></a>
<a id="tocsviptypevo"></a>

```json
{
  "id": 0,
  "name": "string",
  "remark": "string",
  "ename": "string"
}

```

会员类型视图对象 t_vip_type

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||客户id|
|name|string|false|none||会员类型名称|
|remark|string|false|none||备注|
|ename|string|false|none||none|

<h2 id="tocS_TableDataInfoVipTypeVo">TableDataInfoVipTypeVo</h2>

<a id="schematabledatainfoviptypevo"></a>
<a id="schema_TableDataInfoVipTypeVo"></a>
<a id="tocStabledatainfoviptypevo"></a>
<a id="tocstabledatainfoviptypevo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "name": "string",
      "remark": "string",
      "ename": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[VipTypeVo](#schemaviptypevo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RVipVo">RVipVo</h2>

<a id="schemarvipvo"></a>
<a id="schema_RVipVo"></a>
<a id="tocSrvipvo"></a>
<a id="tocsrvipvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "typeId": 0,
    "price": 0,
    "discountPrice": 0,
    "remark": "string",
    "bgColor": "string",
    "vipTypeName": "string",
    "validTimeUnit": 0,
    "validTimeUnitName": "string",
    "validTime": 0,
    "sortNum": 0,
    "vipName": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[VipVo](#schemavipvo)|false|none||会员配置视图对象 t_vip|

<h2 id="tocS_VipVo">VipVo</h2>

<a id="schemavipvo"></a>
<a id="schema_VipVo"></a>
<a id="tocSvipvo"></a>
<a id="tocsvipvo"></a>

```json
{
  "id": 0,
  "typeId": 0,
  "price": 0,
  "discountPrice": 0,
  "remark": "string",
  "bgColor": "string",
  "vipTypeName": "string",
  "validTimeUnit": 0,
  "validTimeUnitName": "string",
  "validTime": 0,
  "sortNum": 0,
  "vipName": "string"
}

```

会员配置视图对象 t_vip

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||客户id|
|typeId|integer(int64)|false|none||会员类型id|
|price|number|false|none||原价价格|
|discountPrice|number|false|none||会员价格|
|remark|string|false|none||备注|
|bgColor|string|false|none||背景颜色值|
|vipTypeName|string|false|none||none|
|validTimeUnit|integer(int32)|false|none||有效时长单位，周=1，月=2，季=3，年=4|
|validTimeUnitName|string|false|none||有效时长单位，周，月，季，年|
|validTime|integer(int32)|false|none||有效时长(周期)，表示几周，几个月|
|sortNum|integer(int32)|false|none||排序|
|vipName|string|false|none||会员名称|

<h2 id="tocS_TableDataInfoVipVo">TableDataInfoVipVo</h2>

<a id="schematabledatainfovipvo"></a>
<a id="schema_TableDataInfoVipVo"></a>
<a id="tocStabledatainfovipvo"></a>
<a id="tocstabledatainfovipvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "typeId": 0,
      "price": 0,
      "discountPrice": 0,
      "remark": "string",
      "bgColor": "string",
      "vipTypeName": "string",
      "validTimeUnit": 0,
      "validTimeUnitName": "string",
      "validTime": 0,
      "sortNum": 0,
      "vipName": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[VipVo](#schemavipvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_PlatformVo">PlatformVo</h2>

<a id="schemaplatformvo"></a>
<a id="schema_PlatformVo"></a>
<a id="tocSplatformvo"></a>
<a id="tocsplatformvo"></a>

```json
{
  "id": 0,
  "name": "string",
  "channel": "string",
  "remark": "string",
  "enable": 0
}

```

平台视图对象 t_platform

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|name|string|false|none||平台名称|
|channel|string|false|none||开放渠道|
|remark|string|false|none||备注|
|enable|integer(int32)|false|none||启用状态，0 启用  1 禁用|

<h2 id="tocS_RPlatformVo">RPlatformVo</h2>

<a id="schemarplatformvo"></a>
<a id="schema_RPlatformVo"></a>
<a id="tocSrplatformvo"></a>
<a id="tocsrplatformvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "name": "string",
    "channel": "string",
    "remark": "string",
    "enable": 0
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[PlatformVo](#schemaplatformvo)|false|none||平台视图对象 t_platform|

<h2 id="tocS_TableDataInfoPlatformVo">TableDataInfoPlatformVo</h2>

<a id="schematabledatainfoplatformvo"></a>
<a id="schema_TableDataInfoPlatformVo"></a>
<a id="tocStabledatainfoplatformvo"></a>
<a id="tocstabledatainfoplatformvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "name": "string",
      "channel": "string",
      "remark": "string",
      "enable": 0
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[PlatformVo](#schemaplatformvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_CustomVipVo">CustomVipVo</h2>

<a id="schemacustomvipvo"></a>
<a id="schema_CustomVipVo"></a>
<a id="tocScustomvipvo"></a>
<a id="tocscustomvipvo"></a>

```json
{
  "id": 0,
  "vipId": 0,
  "customId": 0,
  "price": 0,
  "discountPrice": 0,
  "startTime": "2019-08-24T14:15:22Z",
  "endTime": "2019-08-24T14:15:22Z",
  "remark": "string",
  "vipName": "string"
}

```

会员管理视图对象 t_custom_vip

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|vipId|integer(int64)|false|none||会员id|
|customId|integer(int64)|false|none||用户id|
|price|number|false|none||会员价格|
|discountPrice|number|false|none||会员折扣价格|
|startTime|string(date-time)|false|none||会员卡开始时间|
|endTime|string(date-time)|false|none||会员卡结束时间|
|remark|string|false|none||备注|
|vipName|string|false|none||会员名称|

<h2 id="tocS_RCustomVipVo">RCustomVipVo</h2>

<a id="schemarcustomvipvo"></a>
<a id="schema_RCustomVipVo"></a>
<a id="tocSrcustomvipvo"></a>
<a id="tocsrcustomvipvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "vipId": 0,
    "customId": 0,
    "price": 0,
    "discountPrice": 0,
    "startTime": "2019-08-24T14:15:22Z",
    "endTime": "2019-08-24T14:15:22Z",
    "remark": "string",
    "vipName": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[CustomVipVo](#schemacustomvipvo)|false|none||会员管理视图对象 t_custom_vip|

<h2 id="tocS_TableDataInfoCustomVipVo">TableDataInfoCustomVipVo</h2>

<a id="schematabledatainfocustomvipvo"></a>
<a id="schema_TableDataInfoCustomVipVo"></a>
<a id="tocStabledatainfocustomvipvo"></a>
<a id="tocstabledatainfocustomvipvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "vipId": 0,
      "customId": 0,
      "price": 0,
      "discountPrice": 0,
      "startTime": "2019-08-24T14:15:22Z",
      "endTime": "2019-08-24T14:15:22Z",
      "remark": "string",
      "vipName": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[CustomVipVo](#schemacustomvipvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_ChannelVo">ChannelVo</h2>

<a id="schemachannelvo"></a>
<a id="schema_ChannelVo"></a>
<a id="tocSchannelvo"></a>
<a id="tocschannelvo"></a>

```json
{
  "id": 0,
  "type": 0,
  "name": "string",
  "remark": "string",
  "enable": 0,
  "flag": true
}

```

渠道视图对象 t_channel

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|type|integer(int64)|false|none||渠道类型|
|name|string|false|none||渠道名称|
|remark|string|false|none||备注|
|enable|integer(int32)|false|none||启用状态，0 启用  1 禁用|
|flag|boolean|false|none||用户是否存在此角色标识 默认不存在|

<h2 id="tocS_RChannelVo">RChannelVo</h2>

<a id="schemarchannelvo"></a>
<a id="schema_RChannelVo"></a>
<a id="tocSrchannelvo"></a>
<a id="tocsrchannelvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "type": 0,
    "name": "string",
    "remark": "string",
    "enable": 0,
    "flag": true
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[ChannelVo](#schemachannelvo)|false|none||渠道视图对象 t_channel|

<h2 id="tocS_TableDataInfoChannelVo">TableDataInfoChannelVo</h2>

<a id="schematabledatainfochannelvo"></a>
<a id="schema_TableDataInfoChannelVo"></a>
<a id="tocStabledatainfochannelvo"></a>
<a id="tocstabledatainfochannelvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "type": 0,
      "name": "string",
      "remark": "string",
      "enable": 0,
      "flag": true
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[ChannelVo](#schemachannelvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_MemberTypeVo">MemberTypeVo</h2>

<a id="schemamembertypevo"></a>
<a id="schema_MemberTypeVo"></a>
<a id="tocSmembertypevo"></a>
<a id="tocsmembertypevo"></a>

```json
{
  "vipId": 0,
  "vipName": "string",
  "bgColor": "string",
  "startTime": "2019-08-24T14:15:22Z",
  "endTime": "2019-08-24T14:15:22Z"
}

```

会员类型Vo

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|vipId|integer(int64)|false|none||会员id|
|vipName|string|false|none||会员名称|
|bgColor|string|false|none||背景颜色值|
|startTime|string(date-time)|false|none||会员卡开始时间|
|endTime|string(date-time)|false|none||会员卡结束时间|

<h2 id="tocS_BrandBo">BrandBo</h2>

<a id="schemabrandbo"></a>
<a id="schema_BrandBo"></a>
<a id="tocSbrandbo"></a>
<a id="tocsbrandbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "name": "string",
  "type": 0,
  "wxMpId": 0,
  "enable": 0,
  "remark": "string"
}

```

品牌业务对象 t_brand

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||品牌主键id|
|name|string(string)|true|none||品牌名称|
|type|integer(int64)|true|none||品牌类型|
|wxMpId|integer(int64)|false|none||关联的微信公众号: 用于通知模板消息|
|enable|integer(int32)|true|none||启用状态，0 启用  1 禁用|
|remark|string(string)|false|none||备注|

<h2 id="tocS_RListWxMsgConfigVo">RListWxMsgConfigVo</h2>

<a id="schemarlistwxmsgconfigvo"></a>
<a id="schema_RListWxMsgConfigVo"></a>
<a id="tocSrlistwxmsgconfigvo"></a>
<a id="tocsrlistwxmsgconfigvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "id": 0,
      "appId": "string",
      "msgType": 0,
      "subType": 0,
      "subTypeName": "string",
      "msgTemplateId": "string",
      "jumpUrl": "string",
      "enable": 0,
      "remark": "string",
      "delFlag": "string",
      "appName": "string",
      "msgTypeName": "string",
      "paramOne": "string",
      "paramTwo": "string",
      "paramThree": "string",
      "paramFour": "string",
      "paramFive": "string",
      "paramRemark": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[WxMsgConfigVo](#schemawxmsgconfigvo)]|false|none||[微信模板消息配置视图对象 t_wx_msg_config]|

<h2 id="tocS_BrandVo">BrandVo</h2>

<a id="schemabrandvo"></a>
<a id="schema_BrandVo"></a>
<a id="tocSbrandvo"></a>
<a id="tocsbrandvo"></a>

```json
{
  "id": 0,
  "name": "string",
  "type": 0,
  "wxMpId": 0,
  "enable": 0,
  "remark": "string",
  "wxMpName": "string"
}

```

品牌视图对象 t_brand

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||品牌主键id|
|name|string|false|none||品牌名称|
|type|integer(int64)|false|none||品牌类型|
|wxMpId|integer(int64)|false|none||关联的微信公众号: 用于通知模板消息|
|enable|integer(int32)|false|none||启用状态，0 启用  1 禁用|
|remark|string|false|none||备注|
|wxMpName|string|false|none||none|

<h2 id="tocS_RBrandVo">RBrandVo</h2>

<a id="schemarbrandvo"></a>
<a id="schema_RBrandVo"></a>
<a id="tocSrbrandvo"></a>
<a id="tocsrbrandvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "name": "string",
    "type": 0,
    "wxMpId": 0,
    "enable": 0,
    "remark": "string",
    "wxMpName": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[BrandVo](#schemabrandvo)|false|none||品牌视图对象 t_brand|

<h2 id="tocS_TableDataInfoBrandVo">TableDataInfoBrandVo</h2>

<a id="schematabledatainfobrandvo"></a>
<a id="schema_TableDataInfoBrandVo"></a>
<a id="tocStabledatainfobrandvo"></a>
<a id="tocstabledatainfobrandvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "name": "string",
      "type": 0,
      "wxMpId": 0,
      "enable": 0,
      "remark": "string",
      "wxMpName": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[BrandVo](#schemabrandvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RListBrandVo">RListBrandVo</h2>

<a id="schemarlistbrandvo"></a>
<a id="schema_RListBrandVo"></a>
<a id="tocSrlistbrandvo"></a>
<a id="tocsrlistbrandvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "id": 0,
      "name": "string",
      "type": 0,
      "wxMpId": 0,
      "enable": 0,
      "remark": "string",
      "wxMpName": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[BrandVo](#schemabrandvo)]|false|none||[品牌视图对象 t_brand]|

<h2 id="tocS_RListVipVo">RListVipVo</h2>

<a id="schemarlistvipvo"></a>
<a id="schema_RListVipVo"></a>
<a id="tocSrlistvipvo"></a>
<a id="tocsrlistvipvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "id": 0,
      "typeId": 0,
      "price": 0,
      "discountPrice": 0,
      "remark": "string",
      "bgColor": "string",
      "vipTypeName": "string",
      "validTimeUnit": 0,
      "validTimeUnitName": "string",
      "validTime": 0,
      "sortNum": 0,
      "vipName": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[VipVo](#schemavipvo)]|false|none||[会员配置视图对象 t_vip]|

<h2 id="tocS_MsgAppConfigBo">MsgAppConfigBo</h2>

<a id="schemamsgappconfigbo"></a>
<a id="schema_MsgAppConfigBo"></a>
<a id="tocSmsgappconfigbo"></a>
<a id="tocsmsgappconfigbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "type": 0,
  "appName": "string",
  "appId": "string",
  "secret": "string",
  "token": "string",
  "aesKey": "string",
  "phoneNumbers": "string",
  "remark": "string",
  "delFlag": "string",
  "enable": 0
}

```

【微信公众号配置】业务对象 t_wx_mp_config

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||自增id|
|type|integer(int32)|true|none||应用类型： 1=公众号, 2=小程序|
|appName|string(string)|true|none||应用名称|
|appId|string(string)|true|none||应用编号|
|secret|string(string)|true|none||密钥|
|token|string(string)|true|none||令牌|
|aesKey|string(string)|true|none||aes加密密钥|
|phoneNumbers|string(string)|false|none||运维人员手机号, 用逗号隔开|
|remark|string(string)|false|none||备注|
|delFlag|string(string)|false|none||逻辑删除：0 正常，1 删除|
|enable|integer(int32)|true|none||启用状态 0 启用  1 禁用|

<h2 id="tocS_BrandMsgAppBo">BrandMsgAppBo</h2>

<a id="schemabrandmsgappbo"></a>
<a id="schema_BrandMsgAppBo"></a>
<a id="tocSbrandmsgappbo"></a>
<a id="tocsbrandmsgappbo"></a>

```json
{
  "createBy": "string",
  "createTime": "2019-08-24T14:15:22Z",
  "updateBy": "string",
  "updateTime": "2019-08-24T14:15:22Z",
  "params": {
    "property1": {},
    "property2": {}
  },
  "id": 0,
  "brandType": 0,
  "platformType": 0,
  "msgAppId": "string",
  "enable": 0,
  "remark": "string"
}

```

品牌消息应用关联业务对象 t_brand_msg_app

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|createBy|string(string)|false|none||创建者|
|createTime|string(date-time)|false|none||创建时间|
|updateBy|string(string)|false|none||更新者|
|updateTime|string(date-time)|false|none||更新时间|
|params|object(object)|false|none||请求参数|
|» **additionalProperties**|object|false|none||none|
|id|integer(int64)|true|none||主键id|
|brandType|integer(int32)|true|none||品牌类型: 1=yxr 2=jxh 3=mbti|
|platformType|integer(int32)|true|none||应用类型：0=h5, 1=mini|
|msgAppId|string(string)|true|none||消息应用编号，用于查找通知消息配置|
|enable|integer(int32)|true|none||启用状态，0 启用  1 禁用|
|remark|string(string)|false|none||备注|

<h2 id="tocS_CustomVerifyAuditDto">CustomVerifyAuditDto</h2>

<a id="schemacustomverifyauditdto"></a>
<a id="schema_CustomVerifyAuditDto"></a>
<a id="tocScustomverifyauditdto"></a>
<a id="tocscustomverifyauditdto"></a>

```json
{
  "verifyType": 0,
  "customId": 0,
  "certifiedStatus": 0,
  "certificationFailReason": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|verifyType|integer(int32)|true|none||1-实名认证, 2-学历认证, 3,工作认证|
|customId|integer(int64)|true|none||客户Id|
|certifiedStatus|integer(int32)|true|none||认证状态 0-认证中|1-认证成功|2-认证失败|
|certificationFailReason|string|false|none||工作认证失败原因|

<h2 id="tocS_RListVipTypeVo">RListVipTypeVo</h2>

<a id="schemarlistviptypevo"></a>
<a id="schema_RListVipTypeVo"></a>
<a id="tocSrlistviptypevo"></a>
<a id="tocsrlistviptypevo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "id": 0,
      "name": "string",
      "remark": "string",
      "ename": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[VipTypeVo](#schemaviptypevo)]|false|none||[会员类型视图对象 t_vip_type]|

<h2 id="tocS_MsgAppConfigVo">MsgAppConfigVo</h2>

<a id="schemamsgappconfigvo"></a>
<a id="schema_MsgAppConfigVo"></a>
<a id="tocSmsgappconfigvo"></a>
<a id="tocsmsgappconfigvo"></a>

```json
{
  "id": 0,
  "type": 0,
  "appName": "string",
  "appId": "string",
  "secret": "string",
  "token": "string",
  "aesKey": "string",
  "phoneNumbers": "string",
  "enable": 0,
  "remark": "string",
  "delFlag": "string"
}

```

【微信公众号配置】视图对象 t_wx_mp_config

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|type|integer(int32)|false|none||none|
|appName|string|false|none||应用名称|
|appId|string|false|none||应用编号|
|secret|string|false|none||密钥|
|token|string|false|none||令牌|
|aesKey|string|false|none||aes加密密钥|
|phoneNumbers|string|false|none||运维人员手机号|
|enable|integer(int32)|false|none||none|
|remark|string|false|none||备注|
|delFlag|string|false|none||逻辑删除：0 正常，1 删除|

<h2 id="tocS_RMsgAppConfigVo">RMsgAppConfigVo</h2>

<a id="schemarmsgappconfigvo"></a>
<a id="schema_RMsgAppConfigVo"></a>
<a id="tocSrmsgappconfigvo"></a>
<a id="tocsrmsgappconfigvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "type": 0,
    "appName": "string",
    "appId": "string",
    "secret": "string",
    "token": "string",
    "aesKey": "string",
    "phoneNumbers": "string",
    "enable": 0,
    "remark": "string",
    "delFlag": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[MsgAppConfigVo](#schemamsgappconfigvo)|false|none||【微信公众号配置】视图对象 t_wx_mp_config|

<h2 id="tocS_TableDataInfoMsgAppConfigVo">TableDataInfoMsgAppConfigVo</h2>

<a id="schematabledatainfomsgappconfigvo"></a>
<a id="schema_TableDataInfoMsgAppConfigVo"></a>
<a id="tocStabledatainfomsgappconfigvo"></a>
<a id="tocstabledatainfomsgappconfigvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "type": 0,
      "appName": "string",
      "appId": "string",
      "secret": "string",
      "token": "string",
      "aesKey": "string",
      "phoneNumbers": "string",
      "enable": 0,
      "remark": "string",
      "delFlag": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[MsgAppConfigVo](#schemamsgappconfigvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_RListMsgAppConfigVo">RListMsgAppConfigVo</h2>

<a id="schemarlistmsgappconfigvo"></a>
<a id="schema_RListMsgAppConfigVo"></a>
<a id="tocSrlistmsgappconfigvo"></a>
<a id="tocsrlistmsgappconfigvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": [
    {
      "id": 0,
      "type": 0,
      "appName": "string",
      "appId": "string",
      "secret": "string",
      "token": "string",
      "aesKey": "string",
      "phoneNumbers": "string",
      "enable": 0,
      "remark": "string",
      "delFlag": "string"
    }
  ]
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[[MsgAppConfigVo](#schemamsgappconfigvo)]|false|none||[【微信公众号配置】视图对象 t_wx_mp_config]|

<h2 id="tocS_BrandMsgAppVo">BrandMsgAppVo</h2>

<a id="schemabrandmsgappvo"></a>
<a id="schema_BrandMsgAppVo"></a>
<a id="tocSbrandmsgappvo"></a>
<a id="tocsbrandmsgappvo"></a>

```json
{
  "id": 0,
  "brandType": 0,
  "platformType": 0,
  "msgAppId": "string",
  "enable": 0,
  "remark": "string",
  "brandName": "string",
  "platformName": "string",
  "msgAppName": "string"
}

```

品牌消息应用关联视图对象 t_brand_msg_app

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||主键id|
|brandType|integer(int32)|false|none||品牌类型: 1=yxr 2=jxh 3=mbti|
|platformType|integer(int32)|false|none||应用类型：0=h5, 1=mini|
|msgAppId|string|false|none||消息应用编号，用于查找通知消息配置|
|enable|integer(int32)|false|none||启用状态，0 启用  1 禁用|
|remark|string|false|none||备注|
|brandName|string|false|none||none|
|platformName|string|false|none||none|
|msgAppName|string|false|none||none|

<h2 id="tocS_RBrandMsgAppVo">RBrandMsgAppVo</h2>

<a id="schemarbrandmsgappvo"></a>
<a id="schema_RBrandMsgAppVo"></a>
<a id="tocSrbrandmsgappvo"></a>
<a id="tocsrbrandmsgappvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "brandType": 0,
    "platformType": 0,
    "msgAppId": "string",
    "enable": 0,
    "remark": "string",
    "brandName": "string",
    "platformName": "string",
    "msgAppName": "string"
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[BrandMsgAppVo](#schemabrandmsgappvo)|false|none||品牌消息应用关联视图对象 t_brand_msg_app|

<h2 id="tocS_TableDataInfoBrandMsgAppVo">TableDataInfoBrandMsgAppVo</h2>

<a id="schematabledatainfobrandmsgappvo"></a>
<a id="schema_TableDataInfoBrandMsgAppVo"></a>
<a id="tocStabledatainfobrandmsgappvo"></a>
<a id="tocstabledatainfobrandmsgappvo"></a>

```json
{
  "total": 0,
  "rows": [
    {
      "id": 0,
      "brandType": 0,
      "platformType": 0,
      "msgAppId": "string",
      "enable": 0,
      "remark": "string",
      "brandName": "string",
      "platformName": "string",
      "msgAppName": "string"
    }
  ],
  "code": 0,
  "msg": "string"
}

```

表格分页数据对象

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|total|integer(int64)|false|none||总记录数|
|rows|[[BrandMsgAppVo](#schemabrandmsgappvo)]|false|none||列表数据|
|code|integer(int32)|false|none||消息状态码|
|msg|string|false|none||消息内容|

<h2 id="tocS_AdminChooseDto">AdminChooseDto</h2>

<a id="schemaadminchoosedto"></a>
<a id="schema_AdminChooseDto"></a>
<a id="tocSadminchoosedto"></a>
<a id="tocsadminchoosedto"></a>

```json
{
  "keyWords": "string"
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|keyWords|string(string)|false|none||客户ID/昵称/微信号|

<h2 id="tocS_CustomVerifyVo">CustomVerifyVo</h2>

<a id="schemacustomverifyvo"></a>
<a id="schema_CustomVerifyVo"></a>
<a id="tocScustomverifyvo"></a>
<a id="tocscustomverifyvo"></a>

```json
{
  "verifyType": 0,
  "customId": 0
}

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|verifyType|integer(int32)|true|none||1实名认证，2 学历认证 3工作认证|
|customId|integer(int64)|true|none||客户Id|

<h2 id="tocS_CustomInviteDto">CustomInviteDto</h2>

<a id="schemacustominvitedto"></a>
<a id="schema_CustomInviteDto"></a>
<a id="tocScustominvitedto"></a>
<a id="tocscustominvitedto"></a>

```json
{
  "inviteType": 0
}

```

查询引荐朋友

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|inviteType|integer(int32)|false|none||邀请类型, 1-邀请, 2-代言|

<h2 id="tocS_CustomInviteRelationDto">CustomInviteRelationDto</h2>

<a id="schemacustominviterelationdto"></a>
<a id="schema_CustomInviteRelationDto"></a>
<a id="tocScustominviterelationdto"></a>
<a id="tocscustominviterelationdto"></a>

```json
{
  "inviterCustomId": 0
}

```

添加代言关系

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|inviterCustomId|integer(int64)|true|none||邀请用户编号|

<h2 id="tocS_ActivityCustomInfoVo">ActivityCustomInfoVo</h2>

<a id="schemaactivitycustominfovo"></a>
<a id="schema_ActivityCustomInfoVo"></a>
<a id="tocSactivitycustominfovo"></a>
<a id="tocsactivitycustominfovo"></a>

```json
{
  "customId": 0,
  "nickName": "string",
  "imageUrl": "string"
}

```

报名用户视图对象 t_activity_custom

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|customId|integer(int64)|false|none||参加活动用户id|
|nickName|string|false|none||参加活动用户id|
|imageUrl|string|false|none||用户头像|

<h2 id="tocS_ActivityDetailVo">ActivityDetailVo</h2>

<a id="schemaactivitydetailvo"></a>
<a id="schema_ActivityDetailVo"></a>
<a id="tocSactivitydetailvo"></a>
<a id="tocsactivitydetailvo"></a>

```json
{
  "id": 0,
  "title": "string",
  "typeId": 0,
  "grade": 0,
  "titleImg": "string",
  "link": "string",
  "subTitle": "string",
  "maxNum": 0,
  "maxMaleNum": 0,
  "maxFemaleNum": 0,
  "address": "string",
  "detail": "string",
  "detailImg": "string",
  "beginTime": "2019-08-24T14:15:22Z",
  "endTime": "2019-08-24T14:15:22Z",
  "isSelect": 0,
  "nowNum": 0,
  "nowMaleNum": 0,
  "nowFemaleNum": 0,
  "maxChooseNum": 0,
  "briefIntroduction": "string",
  "activityCost": "string",
  "activityPrice": 0,
  "isOnline": "string",
  "activityType": 0,
  "preEnrollNum": 0,
  "activityPlatform": "string",
  "typeTitle": "string",
  "enrollStatus": 0,
  "enrollStatusName": "string",
  "payStatus": 0,
  "payStatusName": "string",
  "activityStatus": "string",
  "activityCustomInfoVoList": [
    {
      "customId": 0,
      "nickName": "string",
      "imageUrl": "string"
    }
  ]
}

```

活动列表视图对象 t_activity

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|id|integer(int64)|false|none||自增id|
|title|string|false|none||活动名称|
|typeId|integer(int64)|false|none||活动类型id|
|grade|integer(int32)|false|none||活动等级，数字越大优先级越高，普通活动为0|
|titleImg|string|false|none||活动封面图片|
|link|string|false|none||对应公众号链接|
|subTitle|string|false|none||副标题|
|maxNum|integer(int64)|false|none||活动最大人数,如果为0则无限大|
|maxMaleNum|integer(int64)|false|none||男生最大人数（不设置则不限制 ）|
|maxFemaleNum|integer(int64)|false|none||女生最大人数（不设置则不限制 ）|
|address|string|false|none||活动地址|
|detail|string|false|none||活动详情|
|detailImg|string|false|none||活动详情图片url|
|beginTime|string(date-time)|false|none||活动开始时间-年月日时分秒|
|endTime|string(date-time)|false|none||活动开始时间-年月日时分秒|
|isSelect|integer(int32)|false|none||是否开启互选 0-未开启|1-开启|2-互选结束|
|nowNum|integer(int64)|false|none||目前报名活动人数|
|nowMaleNum|integer(int64)|false|none||目前报名男生人数|
|nowFemaleNum|integer(int64)|false|none||目前报名女生人数|
|maxChooseNum|integer(int64)|false|none||个人互选上限|
|briefIntroduction|string|false|none||活动简介|
|activityCost|string|false|none||活动费用介绍|
|activityPrice|number|false|none||活动费用|
|isOnline|string|false|none||0:上线 1 下线|
|activityType|integer(int32)|false|none||0 非公益 1 公益|
|preEnrollNum|integer(int64)|false|none||预报名人数|
|activityPlatform|string|false|none||0 所有平台 1 h5 2 小程序|
|typeTitle|string|false|none||活动类型名|
|enrollStatus|integer(int32)|false|none||报名状态 0 未报名 1 未支付,报名中 2 已支付,报名成功  3 报名失败，全额退款|
|enrollStatusName|string|false|none||报名状态 0 未报名 1 未支付,报名中 2 已支付,报名成功  3 报名失败，全额退款|
|payStatus|integer(int32)|false|none||支付状态 0 未支付  1 已支付 2 退款|
|payStatusName|string|false|none||支付状态 0 未支付  1 已支付 2 退款|
|activityStatus|string|false|none||活动状态：0-未开始|1-报名中|2-报名结束，活动进行中|3-活动结束|
|activityCustomInfoVoList|[[ActivityCustomInfoVo](#schemaactivitycustominfovo)]|false|none||[报名用户视图对象 t_activity_custom]|

<h2 id="tocS_RActivityDetailVo">RActivityDetailVo</h2>

<a id="schemaractivitydetailvo"></a>
<a id="schema_RActivityDetailVo"></a>
<a id="tocSractivitydetailvo"></a>
<a id="tocsractivitydetailvo"></a>

```json
{
  "code": 0,
  "msg": "string",
  "data": {
    "id": 0,
    "title": "string",
    "typeId": 0,
    "grade": 0,
    "titleImg": "string",
    "link": "string",
    "subTitle": "string",
    "maxNum": 0,
    "maxMaleNum": 0,
    "maxFemaleNum": 0,
    "address": "string",
    "detail": "string",
    "detailImg": "string",
    "beginTime": "2019-08-24T14:15:22Z",
    "endTime": "2019-08-24T14:15:22Z",
    "isSelect": 0,
    "nowNum": 0,
    "nowMaleNum": 0,
    "nowFemaleNum": 0,
    "maxChooseNum": 0,
    "briefIntroduction": "string",
    "activityCost": "string",
    "activityPrice": 0,
    "isOnline": "string",
    "activityType": 0,
    "preEnrollNum": 0,
    "activityPlatform": "string",
    "typeTitle": "string",
    "enrollStatus": 0,
    "enrollStatusName": "string",
    "payStatus": 0,
    "payStatusName": "string",
    "activityStatus": "string",
    "activityCustomInfoVoList": [
      {
        "customId": 0,
        "nickName": "string",
        "imageUrl": "string"
      }
    ]
  }
}

```

响应信息主体

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|code|integer(int32)|false|none||none|
|msg|string|false|none||none|
|data|[ActivityDetailVo](#schemaactivitydetailvo)|false|none||活动列表视图对象 t_activity|

<h2 id="tocS_getCustomerUsingGETActivityid">getCustomerUsingGETActivityid</h2>

<a id="schemagetcustomerusinggetactivityid"></a>
<a id="schema_getCustomerUsingGETActivityid"></a>
<a id="tocSgetcustomerusinggetactivityid"></a>
<a id="tocsgetcustomerusinggetactivityid"></a>

```json
0

```

### 属性

|名称|类型|必选|约束|中文名|说明|
|---|---|---|---|---|---|
|*anonymous*|integer(int32)|false|none||none|

