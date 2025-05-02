import os

import yaml


def load_yamldata():
    script_path=os.path.abspath(__file__)#当前脚本绝对路径
    curent_directory=os.path.dirname(script_path)#获取当前目录的路径
    file_path=os.path.join(curent_directory,'testdata.yaml')#连接文件名和当前目录，得到完整文件路径
    with open(file_path, 'r', encoding='utf-8') as file:
        data = yaml.safe_load(file)
        # filter_data = [item for item in testdata if not item.get('skip', 'n') == 'y']
    # return filter_data
    return data

# testdata=load_yamldata()
# pprint(testdata)
# pprint(type(testdata))
# pprint(testdata['groupDescription'])
