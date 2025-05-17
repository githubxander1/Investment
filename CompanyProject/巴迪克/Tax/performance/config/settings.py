# config/settings.py

import os

class Config:
    API_BASE_URL = "http://balitax-test.com"
    CREATE_ENDPOINT = "/v1.0/declaration/create"

    DB_CONFIG = {
        "host": "192.168.0.50",
        "port": 3306,
        "user": "balitax_test",
        "password": "VSwE8zVrfuUP#HN",
        "database": "performance_results",
        "charset": "utf8mb4"
    }

    LOG_PATH = os.path.join(os.getcwd(), "logs", "performance.log")
    REPORT_PATH = os.path.join(os.getcwd(), "reports")
