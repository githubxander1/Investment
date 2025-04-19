

#新建代理商接口json
def createAgencyJson(agencyId,name,phone):
    jsonText={
     "access_token":"XXXXX",
     "agencyId":int(agencyId),
     "userId":1,
     "name" : name,
     "contact":"张三",
     "phone":int(phone),
     "email":"test@163.com",
     "province":"11",
     "city":"1101",
     "area":"",
     "address":"一楼101",
     "describe" :None
}
    return jsonText



#外发新建代理商接口json验证数据报文,如果有别的地方有就从别的地方获取
def send_createAgencyJson():
    Json={
         "access_token":"XXXXX",
         "agencyId":29,
         "userId":1,
         "name" : "a00000029",
         "contact":"张三",
         "phone":13312345678,
         "email":"test@163.com",
         "province":"11",
         "city":"1101",
         "area":"",
         "address":"一楼101",
         "describe" :None
    }
    return Json



