
from .com_yaml import r_yaml
import os
import logging
def case_request(**kwargs):
    sess = requests.Session()
    # sess.proxies = {'http': '127.0.0.1:8888'}
    for arg_key, arg_value in kwargs.items():
        '''处理请求参数中有文件参数'''
        if arg_key == 'files':
            # files的值在yaml文件中读出是字典形式，k表示接口的参数名，v表示参数值
            for k, v in arg_value.items():
                # files = []
                kwargs[arg_key] = []
                # 这里v是一个带有文件路径的集合
                for path in v:
                    # 处理某些文件，比如图片需要声明MIME类型服务器才能正确处理
                    if path.split('.')[-1].lower() == 'png':
                        kwargs[arg_key].append((k, ('', open(path, "rb"), 'image/png', {'Expires': '0'})))
                    elif path.split('.')[-1].lower() == 'jpg' or path.split('.')[-1].lower() == 'jpeg':
                        kwargs[arg_key].append((k, ('', open(path, "rb"), 'image/jpeg', {'Expires': '0'})))
                    else:
                        # 让files = [(),(),()...]，实现多文件一次性上传，兼容单个文件上传
                        kwargs[arg_key].append((k, open(path, "rb")))
    '''处理headers和token'''
    # 传了headers，但值不为空，比如传了一些Content-Type之类的
    if kwargs.get('headers', 0):
        data = r_yaml(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp/refer.yaml'))
        # 第一次refer.yaml没有数据，data可能为None，比如登录
        if data:
            kwargs.update({'headers': {'token': data.get('token', 0)}})
            try:
                return sess.request(**kwargs, timeout=20)
            except Exception as e:
                logging.error(f'\n用例执行失败\n用例信息：{kwargs}\n用例执行失败原因：{e}')
        else:
            try:
                return sess.request(**kwargs, timeout=20)
            except Exception as e:
                logging.error(f'\n用例执行失败\n用例信息：{kwargs}\n用例执行失败原因：{e}')
    # 没传headers，或者headers值为空
    else:
        data = r_yaml(os.path.join(os.path.dirname(os.path.dirname(__file__)), 'temp/refer.yaml'))
        if data:
            kwargs.update({'headers': {'token': data.get('token', 0)}})
            try:
                return sess.request(**kwargs, timeout=20)
            except Exception as e:
                logging.error(f'\n用例执行失败\n用例信息：{kwargs}\n用例执行失败原因：{e}')
        try:
            return sess.request(**kwargs, timeout=20)
        except Exception as e:
            logging.error(f'\n用例执行失败\n用例信息：{kwargs}\n用例执行失败原因：{e}')