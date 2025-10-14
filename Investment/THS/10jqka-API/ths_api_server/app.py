import os
import sys
import json
import subprocess
import time

# 尝试导入Flask，如果失败则安装较新版本
try:
    from flask import Flask, request, jsonify
except ImportError:
    print("安装兼容的Flask版本...")
    subprocess.run([sys.executable, "-m", "pip", "install", "flask==2.2.5", "--upgrade"])
    from flask import Flask, request, jsonify

app = Flask(__name__)

# 获取ths_api_server目录
api_server_dir = os.path.dirname(os.path.abspath(__file__))
# 获取10jqka-API项目根目录
ths_project_dir = os.path.dirname(api_server_dir)
# 设置Java类路径 - 使用双反斜杠避免转义问题
java_classpath = f"{ths_project_dir}\\lib\\snappy-java-1.1.10.1.jar;{ths_project_dir}\\bin;."
# 设置Java主类
java_main_class = "Main"
# 设置Java可执行文件路径
java_executable = "java"

# 检查passport.dat是否存在
def check_passport_file():
    """检查10jqka-API项目目录下是否存在passport.dat文件"""
    passport_path = os.path.join(ths_project_dir, "passport.dat")
    return os.path.exists(passport_path)

# 运行Java程序登录同花顺
def run_java_program():
    """运行Java程序登录同花顺"""
    try:
        # Java项目目录就是ths_project_dir
        java_project_dir = ths_project_dir
        
        # 检查passport.dat是否存在
        passport_exists = check_passport_file()
        
        # 运行Java程序
        process = subprocess.Popen(
            [java_executable, "-cp", java_classpath, java_main_class],
            cwd=java_project_dir,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=True  # 在Windows上需要shell=True来正确处理类路径中的分号
        )
        
        # 读取输出
        output = []
        start_time = time.time()
        timeout = 30  # 30秒超时
        
        while time.time() - start_time < timeout:
            if process.poll() is not None:
                break
            
            line = process.stdout.readline()
            if line:
                output.append(line.strip())
                print(line.strip())
                
                # 检查是否需要输入验证码
                if "输入短信验证码:" in line:
                    return {
                        "success": False,
                        "need_verification": True,
                        "message": "需要输入短信验证码",
                        "process_id": process.pid
                    }
                
                # 检查是否登录成功
                if "登录成功" in line:
                    # 等待一会儿确保passport.dat生成
                    time.sleep(2)
                    return {
                        "success": True,
                        "message": "登录成功",
                        "passport_exists": passport_exists
                    }
            
            time.sleep(0.1)
        
        # 如果超时，杀死进程
        process.kill()
        return {
            "success": False,
            "message": "登录超时",
            "output": output
        }
        
    except Exception as e:
        return {
            "success": False,
            "message": f"运行Java程序失败: {str(e)}"
        }

# API路由
@app.route('/api/ths/login', methods=['GET'])
def ths_login():
    """同花顺登录API"""
    result = run_java_program()
    return jsonify(result)

@app.route('/api/ths/check_passport', methods=['GET'])
def check_passport():
    """检查passport.dat是否存在"""
    exists = check_passport_file()
    return jsonify({
        "success": True,
        "exists": exists,
        "path": os.path.join(ths_project_dir, "passport.dat")
    })

@app.route('/api/ths/health', methods=['GET'])
def health_check():
    """健康检查API"""
    return jsonify({
        "success": True,
        "status": "running",
        "timestamp": time.strftime('%Y-%m-%d %H:%M:%S')
    })

if __name__ == '__main__':
    # 使用waitress作为生产服务器
    try:
        from waitress import serve
        print("使用Waitress作为生产服务器")
        serve(app, host='0.0.0.0', port=5000)
    except ImportError:
        print("使用Flask开发服务器")
        app.run(debug=True, host='0.0.0.0', port=5000)