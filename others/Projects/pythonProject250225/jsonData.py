import requests


def getAgencyDetail(id):
    js=requests.get(url="http://192.168.5.27:8888/1/agency/getAgencyDetail",
             params="access_token=xxxxx&agencyId=1&id=%s&colFlag=207"%id).json()

    return js

