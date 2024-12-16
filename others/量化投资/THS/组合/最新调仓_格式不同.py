import datetime
from pprint import pprint
import requests
import pandas as pd
import logging

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def determine_market(stock_code):
    # 根据股票代码判断市场
    if stock_code.startswith(('60', '00')):
        return '沪深A股'
    elif stock_code.startswith('688'):
        return '科创板'
    elif stock_code.startswith('300'):
        return '创业板'
    elif stock_code.startswith(('4', '8')):
        return '北交所'
    else:
        return '其他'

def get_name_desc(product_id):
    url = "https://dq.10jqka.com.cn/fuyao/tg_package/package/v1/get_package_portfolio_infos"
    headers = {
        "Host": "dq.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 10; Redmi Note 7 Pro Build/QKQ1.190915.002; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/87.0.4280.101 Mobile Safari/537.36 Hexin_Gphone/11.16.10 (Royal Flush) hxtheme/1 innerversion/G037.08.980.1.32 followPhoneSystemTheme/1 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Origin": "https://t.10jqka.com.cn",
        "X-Requested-With": "com.hexin.plat.android",
        "Sec-Fetch-Site": "same-site",
        "Sec-Fetch-Mode": "cors",
        "Sec-Fetch-Dest": "empty",
        "Referer": "https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id=19483",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7",
        "Cookie": "IFUserCookieKey={}; user=MDptb182NDE5MjY0ODg6Ok5vbmU6NTAwOjY1MTkyNjQ4ODo3,ExMTExMTExMTExLDQwOzQ0LDExLDQwOzYsMSw0MDs1LDEsNDA7MSwxMDEsNDA7MiwxLDQwOzMsMSw0MDs1LDEsNDA7OCwwMDAwMDAwMDAwMDAwMDAwMDAwMDAwMSw0MDsxMDIsMSw0MDoyNzo6OjY0MTkyNjQ4ODoxNzM0MDUzNTg5Ojo6MTY1ODE0Mjc4MDoyNjc4NDAwOjA6MTE3MTRjYTYwODhjNjRmYzZmNDFlZDRkOTJhMDU3NTMwOjox; userid=641926488; u_name=mo_641926488; escapename=mo_641926488; ticket=58d0f4bf66d65411bb8d8aa431e00721; user_status=0; hxmPid=sns_my_pay_new; v=AxLXmrX7ofaqkd2K73acRpPBYdP0Ixa9SCcK4dxrPkWw771JxLNmzRi3WvOv"
    }
    params = {
        "product_id": product_id,
        "product_type": "portfolio"
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        response.raise_for_status()
        result = response.json()
        if result['status_code'] == 0:
            product_name = result['data']['baseInfo']['productName']
            product_desc = result['data']['baseInfo']['productDesc']
            return {
                "策略id": product_id,
                "策略名称": product_name,
                "策略描述": product_desc
            }
        else:
            print(f"Failed to retrieve data for product_id: {product_id}")
            return None
    except requests.RequestException as e:
        print(f"请求出现错误: {e}")
        return None
def get_newest_relocate_post(portfolio_id):
    # 请求的URL
    url = f"https://t.10jqka.com.cn/portfolio/post/v2/get_newest_relocate_post?id={portfolio_id}"
    # 请求头，直接复制提供的内容
    headers = {
        "Host": "t.10jqka.com.cn",
        "Connection": "keep-alive",
        "Accept": "application/json, text/plain, */*",
        "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": f"https://t.10jqka.com.cn/pkgfront/tgService.html?type=portfolio&id={portfolio_id}",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,en-US;q=0.9",
        "X-Requested-With": "com.hexin.plat.android"
    }

    # 发送GET请求
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()  # 如果响应状态码不是200，会抛出HTTPError异常
    except requests.exceptions.HTTPError as http_err:
        logging.error(f"HTTP 错误发生: {http_err} (ID: {portfolio_id})")
        return None
    except Exception as err:
        logging.error(f"其他错误发生: {err} (ID: {portfolio_id})")
        return None

    result = response.json()
    # pprint(result)

    extract_data = []
    data = result.get("data")
    if data:
        content = data.get("content")
        createAt = data.get("createAt")
        relocatelist = data.get("relocateList", [])

        for relocate in relocatelist:
            code = relocate.get("code")
            concurrentRatio = relocate.get("currentRatio")
            finalPrice = relocate.get("finalPrice")
            name = relocate.get("name")
            newRatio = relocate.get("newRatio")

            #提取今日操作的
            current_date = datetime.datetime.now().date()  # 获取当前日期
            # print(current_date)
            # 提取 createAt_date 字段中的年月日部分
            createAt_date = pd.to_datetime(createAt).date()
            # print(current_date)

            # 对比年月日是否为当天
            # if createAt_date == current_date:
            extract_data.append({
                "策略id": portfolio_id,
                "策略名称": get_name_desc(portfolio_id).get("策略名称"),
                "描述": get_name_desc(portfolio_id).get("策略描述"),
                "说明": content,
                "时间": createAt,
                # "股票代码": code,
                "股票名称": name,
                "所属市场": determine_market(code),
                "参考价": finalPrice,
                "操作":  '卖出' if newRatio < concurrentRatio else '买入',  # 添加操作列
                "当前比例": f"{concurrentRatio * 100:.2f}%",
                "新比例": f"{newRatio * 100:.2f}%"
            })

    return extract_data

def main():
    # 要查询的id列表
    idids = [
        19483, 14533, 16281, 23768, 8426, 9564, 6994, 7152, 20335, 21302, 19347, 8187, 18565, 14980, 16428
    ]

    all_results = []

    # 遍历每个id
    for portfolio_id in idids:
        result = get_newest_relocate_post(portfolio_id)
        if result:
            # df = pd.DataFrame(result)
            # print(df)
            all_results.extend(result)
        # print(all_results)
        else:
            logging.info("没有成功获取任何数据")

    # 打印到控制台
    if all_results:
        df_all = pd.DataFrame(all_results)
        print(df_all)
        # 保存为Excel文件
        df_all.to_excel("组合今天最新调仓.xlsx", index=False)
    else:
        logging.info("没有成功获取任何数据")

if __name__ == "__main__":
    main()
