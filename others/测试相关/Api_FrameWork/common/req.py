import requests


class RequestUtil:

    def __init__(self):
        self.sess = requests.Session()

    def case_request(self, **kwargs):
        """
        处理文件上传参数,可上传单个文件或一次性上传多个文件。
        """
        for arg_key, arg_value in kwargs.items():
            # kwargs解包后找到request()函数需要传文件的关键字参数files
            if arg_key == 'files':
                # files的值在yaml文件中读出是字典形式，k表示接口的参数名，v表示参数值
                for k, v in arg_value.items():
                    # files = []
                    kwargs[arg_key] = []
                    # 这里v是一个带有文件路径的集合
                    for path in v:
                        # 处理某些文件，比如图片需要声明MIME类型服务器才能正确处理
                        if path.split('.')[-1].lower() == 'png':
                            kwargs[arg_key].append((k, ('',open(path, "rb"),'image/png',{'Expires': '0'})))
                        elif path.split('.')[-1].lower() == 'jpg' or path.split('.')[-1].lower() == 'jpeg':
                            kwargs[arg_key].append((k, ('',open(path, "rb"),'image/jpeg',{'Expires': '0'})))
                        else:
                            # 让files = [(),(),()...]，实现多文件一次性上传，兼容单个文件上传
                            kwargs[arg_key].append((k, open(path, "rb")))

        return self.sess.request(**kwargs)
    pass