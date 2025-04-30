# utils/sql_handler.py
import os
import pymysql
from contextlib import contextmanager
import yaml
from typing import Optional, Tuple, Any

class SQLHandler:
    def __init__(self, yaml_path: str, environment: str, project: str):
        """
        优化后的初始化方法
        :param yaml_path: 配置文件路径
        :param environment: 环境标识（test/prod）
        :param project: 项目名称（tax/payok等）
        """
        if not os.path.exists(yaml_path):
            raise FileNotFoundError(f"YAML配置文件不存在: {yaml_path}")

        with open(yaml_path, 'r', encoding='utf-8') as file:
            config_data = yaml.safe_load(file)

        # 增加配置层级校验
        if not config_data.get(environment) or not config_data[environment].get(project):
            raise ValueError(f"无效的环境或项目配置: {environment}/{project}")

        self.config = config_data[environment][project]
        self._init_connection_info()

    def _init_connection_info(self):
        """统一处理连接配置"""
        self.connection_info = {
            'host': str(self.config['ip']).strip("'\""),
            'port': int(self.config['port']),
            'user': str(self.config['user']).strip("'\""),
            'password': str(self.config['password']).strip("'\""),
            'database': str(self.config['db_name']).strip("'\"")
        }
        self.tables = {
            k.strip("'\""): v.strip("'\"")
            for k, v in self.config.get('tables', {}).items()
        }

    def __enter__(self):
        """实现上下文管理入口"""
        self.conn = pymysql.connect(**self.connection_info)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """实现上下文管理出口"""
        if hasattr(self, 'conn') and self.conn:
            self.conn.close()

    @contextmanager
    def _get_connection(self):
        """连接上下文管理器"""
        conn = pymysql.connect(**self.connection_info)
        try:
            yield conn
        finally:
            conn.close()

    def query_one(self, sql: str, params: Optional[Tuple] = None) -> Optional[Tuple]:
        """
        通用查询方法（单条记录）
        :param sql: 带%s占位符的SQL语句
        :param params: 参数元组
        :return: 查询结果元组或None
        """
        with self._get_connection() as conn:
            with conn.cursor() as cursor:
                try:
                    cursor.execute(sql, params or ())
                    return cursor.fetchone()
                except pymysql.Error as e:
                    print(f"SQL执行失败: {str(e)}")
                    raise

    def get_table(self, table_key: str) -> str:
        """
        获取完整表名
        :param table_key: 配置中的表键名
        :return: 实际表名（带Schema前缀）
        """
        if table_key not in self.tables:
            raise KeyError(f"未配置的表键名: {table_key}")
        return f"{self.connection_info['database']}.{self.tables[table_key]}"

if __name__ == '__main__':
    # 动态获取配置文件路径
    current_dir = os.path.dirname(os.path.abspath(__file__))
    yaml_path = os.path.normpath(os.path.join(current_dir, "../common/sql_config.yaml"))

    # def get_google_secret_key(environment, project, table, login_name) -> str:
    #     """安全查询示例"""
    #     try:
    #         handler = SQLHandler(yaml_path, environment, project)
    #         sql = f"SELECT google_secret_key FROM {handler.get_table(table)} WHERE login_name = %s"
    #         result = handler.query_one(sql, (login_name,))
    #         return result[0] if result else None
    #     except Exception as e:
    #         print(f"查询失败: {str(e)}")
    #         return None

    # 测试查询
    def get_tax_agent_info(environment, project, table, company_name: str) -> tuple:
        try:
            handler = SQLHandler(yaml_path, environment, project)
            sql = f"SELECT agent_no, sign_key FROM {handler.get_table(table)} WHERE company_name = %s"
            agent_info = handler.query_one(sql, (company_name,))

            if agent_info:
                print(f"AgentNo: {agent_info[0]}\nSignKey: {agent_info}")
                return agent_info  # 添加返回语句
            else:
                print("未找到匹配记录")
                return (None, None)  # 返回空值元组

        except Exception as e:
            print(f"测试失败: {str(e)}")
            return (None, None)  # 异常时返回空值


    print("Agent配置测试:")
    agent_no,  sign_key = get_tax_agent_info('test', 'tax', 'agent_base_info', 'tax001')
    print(f"AgentNo: {agent_no}\nSignKey: {sign_key[:6]}******")

    # # Google密钥查询测试
    # print("\nGoogle密钥测试:")
    # # secret = get_google_secret_key('test','payok','platform_operator','Xander@test.com')
    # secret = get_google_secret_key('test','tax','tax_operator','tax001@test.com')
    # print(f"查询结果: {secret or '无记录'}")
