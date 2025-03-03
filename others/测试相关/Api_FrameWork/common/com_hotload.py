
import json
import re
# 热加载：让用例文件中的模板字符可以调用python的方法实现数据的替换
def hot_load(case_info):
    # 把case_info字典转成字符串
    case_info_json = json.dumps(case_info, ensure_ascii=False)
    # 正则匹配找到热加载模板，匹配出func和arg组成一个二元组group，group[0]就是函数名，group[1]就是参数名
    groups = re.findall(r'\$\{(.*?)\((.*?)\)\}', case_info_json)
    for group in groups:
        if group[1] == '':  # 没有参数
            new_value = getattr(HotData, group[0])()
        else:  # 有参数
            new_value = getattr(HotData, group[0])(*group[1].split(','))
        # 拼接旧值
        old_value = "${" + group[0] + "(" + group[1] + ")}"
        # 替换旧值，每次循环替换掉对应的模板，再转回字典
        case_info_json = case_info_json.replace(old_value, str(new_value))
        case_info = json.loads(case_info_json)
    return case_info


import time
from faker import Faker
import random
import yaml
import settings

fake = Faker(['zh_CN'])


class HotLoad:
    """--------------------配置信息读取--------------------"""
    def user_id(self):
        return settings.user_id

    '''--------------------接口关联数据读取--------------------'''

    def read_refer_yaml(self, key):
        with open("refer.yaml", encoding='utf8') as f:
            data = yaml.safe_load(f)
            return data[key]

    '''-----------------------环境----------------------'''

    # 图书馆预约web端测试环境
    def lib_web_env(self):
        # return 'http://172.18.1.199:32420'
        return 'http://172.18.1.203:31794'

    # 图书馆预约接口
    def lib_if_env(self):
        return 'http://172.18.1.199:31583'

    # 图书馆预约移动端测试环境
    def lib_mobile_env(self):
        return 'https://test-tsgyy.cqust.edu.cn'

    # 身份中台测试环境
    def ic_env(self):
        return 'http://172.18.1.199:31176'

    # 消息中心测试环境
    def msg_env(self):
        return 'http://172.18.1.199:30154'

    # 网格值班测试环境
    def grid_schedule(self):
        return 'https://test.dqxfz.site'
    '''-----------------------mock数据---------------------'''

    # 人名
    def name(self):
        return fake.name()

    # 电话号码
    def phone_number(self):
        return fake.phone_number()

    # 身份证号码
    def ssn(self):
        return fake.ssn()

    # 地址
    def address(self):
        return fake.address()

    # 日期时间1987-12-13 08:39:46
    def date_time(self):
        return fake.date_time()

    # 时间
    def time_(self):
        return fake.time()

    # 日期
    def date_(self):
        return fake.date()

    # 当前时间+n秒
    def delay_time(self, n):
        return time.strftime("%Y-%m-%dT%H:%M:%S", time.localtime(time.time() + int(n)))

    # 邮箱地址
    def email(self):
        return fake.email()

    # 工作岗位
    def job(self):
        return fake.job()

    # 公司名
    def company(self):
        return fake.company()

    # 用户名
    def user_name(self):
        return fake.user_name()

    # 描述信息
    def text(self):
        return fake.text()

    # 指定范围随机数
    def random_int(self, m, n):
        return random.randint(int(m), int(n))

    # 指定字符和数量
    def char(self, s, n):
        return s * int(n)