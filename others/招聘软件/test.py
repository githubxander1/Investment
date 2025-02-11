import requests


def fetch_experiment_config():
    url = "https://fe-api.zhaopin.com/experiment/config?clientId=2fd27151-b667-47a6-ac7f-f5b93ba9c279&spaceName=i.zhaopin.com"
    headers = {
        "accept": "*/*",
        "accept-language": "zh-CN,zh;q=0.9",
        "sec-ch-ua": "\"Chromium\";v=\"121\", \"Not A(Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site"
    }
    referrer = "https://i.zhaopin.com/"
    headers["referer"] = referrer

    session = requests.Session()
    response = session.get(url, headers=headers)
    if response.status_code == 200:
        return response.text, session
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return None, session


def previous_interface(session,name):
    # 定义请求的URL
    url = "https://fe-api.zhaopin.com/c/i/shielding-enterprise/add"

    # 定义请求头
    headers = {
        "accept": "application/json, text/plain, */*",
        "accept-language": "zh-CN,zh;q=0.9",
        "content-type": "application/json;charset=UTF-8",
        "sec-ch-ua": "\"Chromium\";v=\"121\", \"Not A(Brand\";v=\"99\"",
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "\"Windows\"",
        "sec-fetch-dest": "empty",
        "sec-fetch-mode": "cors",
        "sec-fetch-site": "same-site",
        "x-zp-pom-code": "4077",
        "cookie": "x-zp-client-id=2fd27151-b667-47a6-ac7f-f5b93ba9c279; sajssdk_2015_cross_new_user=1; sensorsdata2015jssdkchannel=%7B%22prop%22%3A%7B%22_sa_channel_landing_url%22%3A%22%22%7D%7D; Hm_lvt_7fa4effa4233f03d11c7e2c710749600=1736414481; HMACCOUNT=C2895077A52D2177; at=fdb4d115626c48b5af34f1ff2a61b39d; rt=2c628a8e5b89478c9b67551f2bfce66c; sts_deviceid=1944a5eea2d16e-029a88aff9b36-3e3b7a0e-655712-1944a5eea2e4c0; sts_sg=1; sts_chnlsid=Unknown; zp_src_url=https%3A%2F%2Fpassport.zhaopin.com%2F; ZP_OLD_FLAG=false; LastCity=%E6%B7%B1%E5%9C%B3; LastCity%5Fid=765; locationInfo_search={%22code%22:%22%22}; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%221108031382%22%2C%22first_id%22%3A%221944941ffaa17-09dcd02bd354e98-3e3b7a0e-655712-1944941ffab29f%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22identities%22%3A%22eyIkaWRlbnRpdHlfY29va2llX2lkIjoiMTk0NDk0MWZmYWExNy0wOWRjZDAyYmQzNTRlOTgtM2UzYjdhMGUtNjU1NzEyLTE5NDQ5NDFmZmFiMjlmIiwiJGlkZW50aXR5X2xvZ2luX2lkIjoiMTEwODAzMTM4MiJ9%22%2C%22history_login_id%22%3A%7B%22name%22%3A%22%24identity_login_id%22%2C%22value%22%3A%221108031382%22%7D%2C%22%24device_id%22%3A%221944941ffaa17-09dcd02bd354e98-3e3b7a0e-655712-1944941ffab29f%22%7D; selectCity_search=765; Hm_lpvt_7fa4effa4233f03d11c7e2c710749600=1736427089; zp_passport_deepknow_sessionId=03838883s88e8a449b954677f8cc927f994d; ZL_REPORT_GLOBAL={%22jobs%22:{%22recommandActionidShare%22:%22fc62ef36-98f4-4a42-8e1d-6399680f45ef-job%22}}"
    }
    body = {
        "at": "fdb4d115626c48b5af34f1ff2a61b39d",
        "rt": "2c628a8e5b89478c9b67551f2bfce66c",
        # "_v": "0.77444523",
        # "x-zp-pom-request-id": "e33f5ee0e47a4174ba4d8f7d15da71b0-1736427149768-552466",
        # "x-zp-client-id": "2fd27151-b667-47a6-ac7f-f5b93ba9c279"
        "isKeyWord": False,
        "name": name
    }

    # 定义请求来源
    referrer = "https://i.zhaopin.com/"
    headers["referer"] = referrer

    # 定义请求体
    # body = "{\"name\":\"广州菁灵科技有限公司\",\"isKeyWord\":false,\"at\":\"fdb4d115626c48b5af34f1ff2a61b39d\",\"rt\":\"2c628a8e5b89478c9b67551f2bfce66c\"}"

    # 发送POST请求
    response = requests.post(url, headers=headers, data=body)
    if response.status_code == 200:
        return response.text
    else:
        print(f"请求失败，状态码: {response.status_code}")
        return None


if __name__ == "__main__":
    result, session = fetch_experiment_config()
    if session:
        previous_result = previous_interface(session, "广州菁灵科技有限公司")
        if previous_result:
            print(previous_result)
