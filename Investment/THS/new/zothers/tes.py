from pprint import pprint

exists_data = {
    "记录": [
        {
            "组合名称": "超短稳定",
            "代码": "600169",
            "股票名称": "太原重工",
            "市场": "沪深A股",
            "操作": "卖出",
            "最新价": 2.76,
            "当前比例%": 5.19,
            "新比例%": 0
        },
        {
            "组合名称": "超短稳定",
            "代码": "002445",
            "股票名称": "中南文化",
            "市场": "沪深A股",
            "操作": "买入",
            "最新价": 2.52,
            "当前比例%": 0,
            "新比例%": 20
        }
    ]
}

compare_data = {
    "记录": [
        {
            "组合名称": "超短稳定",
            "代码": "600169",
            "股票名称": "太原重工",
            "市场": "沪深A股",
            "操作": "卖出",
            "最新价": 2.76,
            "当前比例%": 5.19,
            "新比例%": 0
        },
        {
            "组合名称": "超短稳定",
            "代码": "002445",
            "股票名称":"中南文化",
            "市场": "沪深A股",
            "操作": "买入",
            "最新价": 2.52,
            "当前比例%": 0,
            "新比例%": 20
        }
        ,
        {
            "组合名称": "每天进步一点点",
            "代码": "002445",
            "股票名称": "中南文化",
            "市场": "沪深A股",
            "操作": "买入",
            "最新价": 2.52,
            "当前比例%": 0,
            "新比例%": 20
        }
    ]
}

#对比两个data每一个列表的每一个字段，找出compare里和exists里不同那一条记录，并通知
def compare_data_and_notify(exists_data, compare_data):
    for exists_record in exists_data:
        for compare_record in compare_data:
            if exists_record['组合名称'] == compare_record['组合名称']:
                if exists_record['代码'] != compare_record['代码']:
                    print(f"{exists_record['组合名称']} 的代码有变化，从 {exists_record['代码']} 变为 {compare_record['代码']}")
                else:
                    print()
            # if exists_record['代码'] == compare_record['代码']:
            #     if exists_record['新比例%'] != compare_record['新比例%']:
            #         print(f"{exists_record['代码']} 的新比例有变化，从 {exists_record['新比例%']} 变为 {compare_record['新比例%']}")
            #     else:
            #         print()
compare_data_and_notify(exists_data, compare_data)
# # 控制台输出示例
# pprint()