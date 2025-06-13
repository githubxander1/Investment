
import requests

def upload():
    url = base_url + "/declaration-admin/oss/upload"

    data ={
        "file": open("test.txt", "rb"),
        "fileType": 2
    }

    r = requests.post(url, data=data)
    print(r.text)