import logging
from pprint import pprint

import pandas as pd
import requests

# 设置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class PortfolioAPI:
    def __init__(self, base_url="https://t.10jqka.com.cn"):
        self.base_url = base_url
        self.headers = {
            "Host": "t.10jqka.com.cn",
            "Connection": "keep-alive",
            "Accept": "application/json, text/plain, */*",
            "User-Agent": "Mozilla/5.0 (Linux; Android 9; ASUS_I003DD Build/PI; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/68.0.3440.70 Mobile Safari/537.36 Hexin_Gphone/11.17.03 (Royal Flush) hxtheme/0 innerversion/G037.08.983.1.32 followPhoneSystemTheme/0 userid/641926488 getHXAPPAccessibilityMode/0 hxNewFont/1 isVip/0 getHXAPPFontSetting/normal getHXAPPAdaptOldSetting/0",
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Encoding": "gzip, deflate",
            "Accept-Language": "zh-CN,en-US;q=0.9",
            "X-Requested-With": "com.hexin.plat.android"
        }

    def get_newest_relocate_post(self, portfolio_id):
        url = f"{self.base_url}/portfolio/post/v2/get_newest_relocate_post?id={portfolio_id}"
        referer = f"{self.base_url}/pkgfront/tgService.html?type=portfolio&id={portfolio_id}"
        self.headers["Referer"] = referer

        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP 错误发生: {http_err} (ID: {portfolio_id})")
            return None
        except Exception as err:
            logging.error(f"其他错误发生: {err} (ID: {portfolio_id})")
            return None

        result = response.json()
        pprint(result)
        return self._extract_data(result)

    def _extract_data(self, result):
        extract_data = []
        data = result.get("testdata")
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

                extract_data.append({
                    "说明": content,
                    "时间": createAt,
                    "代码": code,
                    "名称": name,
                    "参考价": finalPrice,
                    "当前比例": concurrentRatio,
                    "新比例": newRatio
                })

        return extract_data

def main():
    idids = [19483, 14533, 16281, 23768, 8426, 9564, 6994, 7152, 20335, 21302, 19347, 8187, 18565, 14980, 16428]
    api = PortfolioAPI()
    all_results = []

    for portfolio_id in idids:
        result = api.get_newest_relocate_post(portfolio_id)
        if result:
            all_results.extend(result)
        else:
            logging.info("没有成功获取任何数据")

    if all_results:
        df_all = pd.DataFrame(all_results)
        df_all.to_excel(r"D:\1document\1test\PycharmProject_gitee\others\量化投资\THS\组合\保存的数据\最新调仓接口.xlsx", index=False)
        print(df_all)
    else:
        logging.info("没有成功获取任何数据")

if __name__ == "__main__":
    main()
    '''
封装 API 请求：将与 API 相关的逻辑封装在 PortfolioAPI 类中，提高了内聚性。
减少耦合：通过类的方式，将 API 请求和数据处理分离，降低了耦合度。
单一职责：PortfolioAPI 类只负责与 API 的交互，main 函数只负责处理业务逻辑。'''
