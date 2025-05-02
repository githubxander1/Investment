
import  requests

def getMsgSum(id,col):
    req = requests.get(url="http://192.168.5.27:8888/1/statistic/getMsgSum",
                       params="access_token=23421422&agencyId=%s&colFlag=%s"%(id,col))
    return req



def createAgency(name,phone):
    req = requests.post(url="http://192.168.5.27:8888/1/agency/createAgency", json={
        "access_token":"XXXXX",
        "agencyId":1,
        "userId":5453,
         "name" : name,
         "contact":"张三",
         "phone":phone,
         "email":"test@163.com",
         "province":"32",
         "city":"32",
         "area":"46",
         "address":"莲花西街道",
         "describe" :"参数测试"
    } )
    return req


def modifyAgency(id,contact):
    req = requests.post(url="http://192.168.5.240:8888/1/agency/modifyAgency", json={
     "access_token":"xxxxx",
     "agencyId":2,
     "userId":5453,
     "id":id,
     "params":{
            "contact":contact
             }
    } )
    return req



