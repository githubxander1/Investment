import json
import logging

from .com_request import case_request
from .com_hotload import hot_load
from .com_refer import get_req_and_write_yaml, get_res_and_write_yaml
from .com_db import DatabasePostgresql
def caseflow(case_info):
    # 替换热加载函数表达式${func(...)}
    if "${" in json.dumps(case_info):
        case_info = hot_load(case_info)
    # 执行用例
    res = case_request(**case_info['request'])
    # 判断如果有refer参数，就是需要提取响应信息进行关联
    if case_info.get('refer', 0):
        get_res_and_write_yaml(res, *case_info['refer'])
    # 判断如果有local参数，就是需要提取请求信息或预设其他信息进行关联
    if case_info.get('local', 0):
        get_req_and_write_yaml(*case_info['local'])
    # 日志
    if res.request.body is None:
        logging.info(
            "\n所属模块：%s" % case_info.get('epic', None) +
            "\n功能点：%s" % case_info.get('feature', None) +
            "\n测试点：%s" % case_info.get('story', None) +
            "\n用例序号：%s" % case_info.get('title', None) +
            "\n请求地址：%s" % res.request.url +
            "\n请求方式：%s" % res.request.method +
            "\n请求头：%s" % res.request.headers +
            "\n请求体：%s" % None +
            "\n响应信息：%s" % res.text
        )
    else:
        logging.info(
            "\n所属模块：%s" % case_info.get('epic', None) +
            "\n功能点：%s" % case_info.get('feature', None) +
            "\n测试点：%s" % case_info.get('story', None) +
            "\n用例序号：%s" % case_info.get('title', None) +
            "\n请求地址：%s" % res.request.url +
            "\n请求方式：%s" % res.request.method +
            "\n请求头：%s" % res.request.headers +
            # 如果参数是二进制编码字符，限制最大500个字符
            "\n请求体：%s" % res.request.body[:500] +
            "\n响应信息：%s" % res.text
        )
    # 断言
    if case_info.get('check', 0):
        check_list = case_info['check']
        # json值相等断言，支持多个预期结果, check_list = [json, [属性1,属性2...,预期结果1], [属性1,属性2...,预期结果2], ...]
        if check_list[0] == 'json':
            expect_result_list = []
            actual_result_list = []
            for i in range(1, len(check_list)):
                expect_result = check_list[i][-1]
                expect_result_list.append(expect_result)
                actual_result = getattr(res, 'json')()
                for j in range(len(check_list[i]) - 1):
                    attr = check_list[i][j]
                    try:
                        # actual_result被调用过程中可能遇到没有attr的键
                        actual_result = actual_result[attr]
                    except Exception as e:
                        logging.error(e)
                        break
                actual_result_list.append(actual_result)
            assert expect_result_list == actual_result_list, logging.error(
                f"\n断言失败：预期结果【{expect_result_list}】 == 实际结果【{actual_result_list}】")
            logging.info(f"\n断言成功：预期结果【{expect_result_list}】 == 实际结果【{actual_result_list}】")
        # 字符串值包含断言, check_list = [text_in, 'str']
        elif check_list[0] == 'text_in':
            assert check_list[1] in getattr(res, 'text'), logging.error(
                f"\n断言失败：预期结果【{check_list[1]}】 in 实际结果【{getattr(res, 'text')}】")
            logging.info(f"\n断言成功：预期结果【{check_list[1]}】 in 实际结果【{getattr(res, 'text')}】")
        # 字符串值不包含断言, check_list = [text_not_in, 'str']，注意判断返回数据是json串的key与value原格式是没有空格的，我们看到的有空格的都是工具美化后的
        elif check_list[0] == 'text_not_in':
            assert str(check_list[1]) not in getattr(res, 'text'), logging.error(
                f"\n断言失败：预期结果【{check_list[1]}】 not in 实际结果【{getattr(res, 'text')}】")
            logging.info(f"\n断言成功：预期结果【{check_list[1]}】 not in 实际结果【{getattr(res, 'text')}】")
        # 数据库db_system查询断言：check_list = [db,数据库名,[sql语句,字段,字段预期值]] or [db,数据库名,[sql语句]]
        # 数据库查询结果对应为：[RealDictRow([(字段,实际值),(字段,实际值),(字段,实际值)...])] or []
        elif check_list[0] == 'db':
            # 数据库实例
            db = DatabasePostgresql(check_list[1])
            if check_list[2][-1] == check_list[2][0]:
                actual_result = db.se(check_list[2][0])
                assert actual_result == [], logging.error(
                    f"\n断言失败：预期结果【[]】 == 实际结果【{actual_result}】")
                logging.info(f"\n断言成功：预期结果【[]】 == 实际结果【{actual_result}】")
            # 有的数据不是物理删除，只是打了删除标记走else流程断言标记删除的字段
            else:
                actual_result = db.se(check_list[2][0])[0].get(check_list[2][1], '字段不存在')
                expect_result = check_list[2][2]
                assert str(expect_result) in str(actual_result), logging.error(
                    f"\n断言失败：预期结果【{expect_result}】 in 实际结果【{actual_result}】")
                logging.info(f"\n断言成功：预期结果【{expect_result}】 in 实际结果【{actual_result}】")
        else:
            logging.error(f'暂时不支持的断言方式：{check_list[0]}')
            raise ValueError(f'暂时不支持的断言方式：{check_list[0]}')
    else:
        logging.info('此用例未设置断言......')
    return res