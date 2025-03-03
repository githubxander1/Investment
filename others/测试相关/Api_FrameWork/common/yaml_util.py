
import yaml

# 读
def r_yaml(path):
    with open(path,encoding='utf-8') as f:
        data = yaml.safe_load(f)
        return data

# 清空写
def w_yaml(path,data):
    with open(path,'w', encoding='utf-8') as f:
        yaml.safe_dump(data,f, allow_unicode=True)


# 追加写
def a_yaml(path,data):
    with open(path,'a', encoding='utf-8') as f:
        yaml.safe_dump(data,f, allow_unicode=True)

# 清空
def c_yaml(path):
    with open(path, 'w', encoding='utf8') as f:
        pass