
import requests

def register():
    url = base_url + "/declaration-admin/agent/operator/registerAgent"

    data = {
      "companyName": "companyName",
      "companyBrandName": "companyBrandName",
      "companyType": 1,
      "npwp": "12.321.265.1-156.3688",
      "officialWebsite": "http://baidu.com",
      "companyAddress": "companyAddress",
      "legalPerson": "persona",
      "legalPersonPhone": "12345678987",
      "legalPersonAddress": "legalPersonAddress",
      "contactPerson": "persona",
      "contactPersonPhone": "12345678998",
      "bidNumberFile": "6bec6aa3ebb728de2911ea7fa023d6066bb0d00af47907f98913925e769532da.png",
      "taxNumberFile": "6bec6aa3ebb728de2911ea7fa023d6066bb0d00af47907f98913925e769532da.png",
      "passportFile": "6bec6aa3ebb728de2911ea7fa023d6066bb0d00af47907f98913925e769532da.png",
      "loginName": "test@agent.com",
      "password": "123456789",
      "verifyCode": "yW31PY"
    }

    r = requests.post(url, json=data)
    print(r.json())
