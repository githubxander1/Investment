# trade_main.py
import argparse
import subprocess
import sys
import os
from pathlib import Path
from element_scraper import scrape_page_elements
from generate_page_object import generate_page_object
from generate_test_case import generate_test_case
# from utils.template_loader import generate_page_object
# from utils.ai_generator import generate_test_data

# 确保目录存在
Path("pages").mkdir(exist_ok=True)
Path("data").mkdir(exist_ok=True)
Path("reports/allure-results").mkdir(parents=True, exist_ok=True)


def generate_page(url: str, page_name: str):
    """生成页面对象文件"""
    try:
        print(f"🔄 正在爬取页面元素: {url}")
        elements = scrape_page_elements(url)

        print(f"⚙️ 正在生成页面对象: {page_name}Page")
        page_class = generate_page_object(page_name)

        output_path = f"pages/{page_name.lower()}_page.py"
        with open(output_path, "w") as f:
            f.write(page_class)
        print(f"✅ 页面对象已保存至: {output_path}")

    except Exception as e:
        print(f"❌ 生成失败: {str(e)}")
        sys.exit(1)


def generate_data(page_name: str):
    """生成测试数据文件"""
    try:
        # 模拟从已有页面文件加载元素（实际需解析页面类）
        print(f"🔄 正在分析 {page_name} 页面结构...")
        elements = [
            {"tag": "input", "id": "username", "name": "", "type": "text"},
            {"tag": "input", "id": "password", "name": "", "type": "password"},
            {"tag": "button", "id": "login-btn", "name": "", "type": "submit"}
        ]

        print("🤖 正在通过AI生成测试数据...")
        # generate_test_data(elements)
        # print(f"✅ 测试数据已保存至: data/{page_name.lower()}_data.yaml")

    except Exception as e:
        print(f"❌ 数据生成失败: {str(e)}")
        sys.exit(1)


def run_tests():
    """执行测试并生成报告"""
    try:
        print("🚀 开始执行自动化测试...")
        subprocess.run([
            "pytest", "testcases/",
            "--alluredir=reports/allure-results",
            "--clean-alluredir"
        ], check=True)

        print("\n📊 生成Allure测试报告...")
        subprocess.run([
            "allure", "generate", "reports/allure-results",
            "-o", "reports/allure-report",
            "--clean"
        ], check=True)

        print(f"\n✨ 执行完成！报告路径: {os.path.abspath('reports/allure-report/index.html')}")

    except subprocess.CalledProcessError as e:
        print(f"❌ 测试执行失败: {e}")
        sys.exit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="自动化测试框架主控程序")
    subparsers = parser.add_subparsers(dest="command")

    # 生成页面对象命令
    page_parser = subparsers.add_parser("generate-page", help="生成页面对象")
    page_parser.add_argument("--url", required=True, help="目标页面URL")
    page_parser.add_argument("--name", required=True, help="页面名称（如 Login）")

    # 生成测试数据命令
    data_parser = subparsers.add_parser("generate-data", help="生成测试数据")
    data_parser.add_argument("--page", required=True, help="页面名称（如 Login）")

    # 执行测试命令
    subparsers.add_parser("run-tests", help="执行所有测试")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    if args.command == "generate-page":
        generate_page(args.url, args.name)
    elif args.command == "generate-data":
        generate_data(args.page)
    elif args.command == "run-tests":
        run_tests()
    else:
        print("⚠️ 未知命令")
        parser.print_help()
