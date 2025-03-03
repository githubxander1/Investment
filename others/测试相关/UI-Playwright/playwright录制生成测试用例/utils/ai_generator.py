import yaml
from typing import List, Dict


def generate_test_data(elements: List[Dict]) -> List[Dict]:
    # 模拟 AI 生成逻辑（实际需调用 API）
    test_cases = [
        {
            "case_name": "正常流程",
            "data": {elem["id"]: "test_value" for elem in elements if elem["tag"] == "input"},
            "expected": "success"
        },
        {
            "case_name": "空值校验",
            "data": {elem["id"]: "" for elem in elements if elem["tag"] == "input"},
            "expected": "error"
        }
    ]

    # 保存为 YAML
    with open("data/login_data.yaml", "w") as f:
        yaml.dump(test_cases, f)

    return test_cases