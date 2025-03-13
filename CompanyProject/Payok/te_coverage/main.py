import subprocess
import os

def run_tests():
    try:
        # 打印当前工作目录
        print(f"Current working directory: {os.getcwd()}")

        # 运行 pytest 并收集覆盖率信息
        subprocess.run(['python', '-m', 'coverage', 'run', '-m', 'pytest', '--alluredir=allure-results'], check=True)

        # 生成覆盖率报告
        subprocess.run(['python', '-m', 'coverage', 'report'], check=True)
        subprocess.run(['python', '-m', 'coverage', 'html'], check=True)

        # 生成 Allure 报告
        if os.path.exists('allure-results'):
            subprocess.run(['allure', 'generate', 'allure-results', '-o', 'allure-report', '--clean'], check=True)
            subprocess.run(['allure', 'open', 'allure-report'], check=True)
        else:
            print("allure-results directory not found. Skipping Allure report generation.")
    except FileNotFoundError as e:
        print(f"Error: Command not found. Please ensure 'coverage', 'pytest', and 'allure' are installed and in PATH.")
        print(e)
    except subprocess.CalledProcessError as e:
        print(f"Error occurred while running subprocess: {e}")

if __name__ == "__main__":
    run_tests()
