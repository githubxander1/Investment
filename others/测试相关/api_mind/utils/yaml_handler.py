# z_others.测试相关.ApiTest_mindmaster.api_mind.utils.yaml_handler.py
import yaml


def read_yaml(file_path):
    # 获取项目根目录
    # project_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    # file__path = os.path.join(project_root, file_path)
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            return yaml.safe_load(file)
    except FileNotFoundError:
        print(f"文件不存在: {file_path}")
        return None
    except yaml.YAMLError as e:
        print(f"YAML解析错误: {e}")
        return None
    except Exception as e:
        print(f"发生错误: {e}")
        return None
def write_yaml(data, file_path):
    with open(file_path, 'w', encoding='utf-8') as file:
        yaml.dump(data, file, allow_unicode=True)
