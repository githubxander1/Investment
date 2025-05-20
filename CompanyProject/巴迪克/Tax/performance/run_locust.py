# run_locust.py
import os
import sys
import argparse
import subprocess


def start_locust():
    print("🚀 正在启动 Locust 压测...")
    result = subprocess.run([
        "locust",
        "-f", "locustfile_1.py",
        "--host", "http://balitax-test.com/declaration-api",
        "--web-port", "8090",
        "--users = 500",
        "--spawn - rate = 50",
        "--run-time = 5m",
        "--headless"  # ← 非 Web 模式，直接运行
    ])
    if result.returncode != 0:
        print("❌ Locust 压测启动失败")
        sys.exit(1)


def run_pytest():
    REPORT_DIR = "reports/allure-results"
    os.makedirs(REPORT_DIR, exist_ok=True)

    print("🧪 正在运行性能测试...")
    result = subprocess.run([
        "pytest",
        "--alluredir", REPORT_DIR,
        "tests/test_api_performance.py"
    ])
    if result.returncode != 0:
        print("❌ 性能测试执行失败")
        sys.exit(1)

    # Step 3: 查看 Allure 报告
    print("📊 正在生成并打开 Allure 报告...")
    result = subprocess.run(["allure", "open", REPORT_DIR], check=False)
    if result.returncode != 0:
        print("❌ 无法打开 Allure 报告")
        sys.exit(1)


if __name__ == '__main__':
    # parser = argparse.ArgumentParser(description="选择运行模式")
    # parser.add_argument("--mode", choices=["locust", "pytest"], required=True, help="运行模式: locust / pytest")
    #
    # args = parser.parse_args()
    #
    # if args.mode == "locust":
    start_locust()
    # elif args.mode == "pytest":
    #     run_pytest()
