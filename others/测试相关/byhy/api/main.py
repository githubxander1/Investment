# main.py
import json
import os
import zipfile

import allure
import pytest
from dotenv import load_dotenv

# 加载 .env 文件
load_dotenv()

if __name__ == '__main__':
    allure_report_filepath = os.path.join(os.path.dirname(__file__), "reports", "allure-results")

    # 运行测试并生成 Allure 结果
    pytest.main(["-vs", 'tests', "--alluredir", allure_report_filepath])

    # 生成 Allure 报告
    allure_report_html = os.path.join(os.path.dirname(__file__), "reports", "allure-report")
    os.system(f"allure generate {allure_report_filepath} -o {allure_report_html} --clean")

    # 压缩 Allure 报告目录
    allure_report_zip = os.path.join(os.path.dirname(__file__), "reports", "allure-report.zip")
    with zipfile.ZipFile(allure_report_zip, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(allure_report_html):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, allure_report_html)
                zipf.write(file_path, arcname)

    # 发送 Allure 报告到电子邮件
    subject = "Allure Test Report"
    body = "Please find the attached Allure Test Report."
    to_email = "2695418206@qq.com"
    attachment_path = allure_report_zip

    # send_email(subject, body, to_email, attachment_path)
