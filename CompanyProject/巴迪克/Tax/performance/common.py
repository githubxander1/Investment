import os
import hmac
import json
import hashlib
import datetime
import requests
from urllib.parse import urlparse
from typing import Dict, Tuple
from CompanyProject.巴迪克.utils.sql_handler import SQLHandler

# 配置常量
CONFIG = {
    "BASE_URL": "http://balitax-test.com/declaration-api",
    "YAML_PATH": os.path.normpath(os.path.join(
        os.path.dirname(os.path.abspath(__file__)),
        "../../common/sql_config.yaml"
    ))
}

class TaxAPIBase:
    """税务申报API客户端基类"""

    def __init__(self, company_name: str, environment: str = 'test'):
        """
        初始化税务API客户端
        :param environment: 环境标识（test/prod）
        :param company_name: 代理公司名称
        """
        self.environment = environment
        self.company_name = company_name
        self.agent_id, self.secret_key = self._load_agent_credentials()

    def _load_agent_credentials(self) -> Tuple[str, str]:
        """从数据库加载代理凭证"""
        try:
            with SQLHandler(CONFIG['YAML_PATH'], self.environment, 'tax') as handler:
                sql = f"SELECT agent_no, sign_key FROM {handler.get_table('agent_base_info')} WHERE company_name = %s"
                result = handler.query_one(sql, (self.company_name,))
                print(f"agent_no: {result[0]} , sign_key: {result[1]}")

            if not result:
                raise ValueError(f"未找到公司 {self.company_name} 的信息")
            return result[0], result[1]
        except Exception as e:
            print(f"[ERROR] 凭证加载失败: {str(e)}")
            raise

    @staticmethod
    def _generate_iso_timestamp() -> str:
        """生成ISO 8601格式时间戳（带毫秒和时区）"""
        now = datetime.datetime.now(datetime.timezone.utc).astimezone()
        tz_offset = now.utcoffset()
        hours, minutes = divmod(int(tz_offset.total_seconds()) // 60, 60)
        return now.strftime(f"%Y-%m-%dT%H:%M:%S.{now.microsecond//1000:03d}") + \
            f"{'+' if hours >= 0 else '-'}{abs(hours):02d}:{minutes:02d}"

    def _generate_signature(self, endpoint_path: str, payload: Dict) -> str:
        """生成HMAC-SHA256签名"""
        # 压缩JSON payload
        payload_str = json.dumps(payload, separators=(',', ':'), ensure_ascii=False)

        # 生成签名
        timestamp = self._generate_iso_timestamp()
        payload_hash = hashlib.sha256(payload_str.encode()).hexdigest().lower()
        canonical_str = f"POST:{endpoint_path.lower()}:{payload_hash}:{timestamp}"
        return hmac.new(
            self.secret_key.encode(),
            canonical_str.encode(),
            hashlib.sha256
        ).hexdigest()

    def send_request(self, endpoint_path: str, payload: Dict) -> Dict:
        """发送请求"""
        try:
            # 准备请求参数
            headers = {
                "Content-Type": "application/json; charset=utf-8",
                "X-AGENT-ID": self.agent_id,
                "X-TIMESTAMP": self._generate_iso_timestamp(),
                "X-SIGNATURE": self._generate_signature(endpoint_path, payload),
                "Host": urlparse(CONFIG['BASE_URL']).netloc
            }

            # 发送请求
            response = requests.post(
                url=f"{CONFIG['BASE_URL']}{endpoint_path}",
                data=json.dumps(payload, separators=(',', ':')),
                headers=headers
            )
            response.raise_for_status()

            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"[ERROR] 请求失败: {str(e)}")
            return {"error": str(e)}
        except Exception as e:
            print(f"[ERROR] 系统错误: {str(e)}")
            return {"error": "Internal error"}
