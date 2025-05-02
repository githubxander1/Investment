# yaml_handler.py
import yaml

def read_yaml(yaml_file):
    with open(yaml_file, 'r', encoding='utf-8') as f:
        cfg = yaml.safe_load(f)
    return cfg

def get_db_config(yaml_file, db_name, table_name):
    config = read_yaml(yaml_file)
    db_config = config.get(db_name, {})
    table_config = db_config.get('tables', {}).get(table_name, None)

    if not table_config:
        print(f"未找到数据库或表配置: {db_name}, {table_name}")
        return None

    db_config['table_name'] = table_config
    return db_config
