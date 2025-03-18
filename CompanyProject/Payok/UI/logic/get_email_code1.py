# 要实现登录内网服务器Jumpserver并执行后续操作，你可以分以下几个步骤进行：

import requests
import paramiko


# 登录Jumpserver
import logging

logging.basicConfig(level=logging.DEBUG)

def login_jumpserver():
   logging.debug("开始登录...")
   login_url = 'http://192.168.0.228/core/auth/login/'
   data = {
       'username': 'xiaozehua',
       'password': '8qudcQifW7cjydglydm{'
   }
   session = requests.Session()

   # 获取CSRF Token
   csrf_response = session.get(login_url)
   csrf_token = re.search(r'<input type="hidden" name="csrfmiddlewaretoken" value="([^"]+)"', csrf_response.text).group(1)
   data['csrfmiddlewaretoken'] = csrf_token

   headers = {
       'X-CSRFToken': csrf_token,
       'Referer': login_url
   }

   response = session.post(login_url, data=data, headers=headers)
   # logging.debug(f"Response status code: {response.status_code}")
   # logging.debug(f"Response content: {response.text}")
   if response.status_code == 200:
       logging.info("登录Jumpserver成功")
       return session
   else:
       logging.error("登录Jumpserver失败")
       return None




# 通过SSH连接到目标服务器执行命令
def execute_commands_on_target(session):
   target_host = '192.168.0.224'
   target_port = 2222
   target_username = 'xiaozehua'
   target_password = '8qudcQifW7cjydglydm{'

   ssh = paramiko.SSHClient()
   ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
   try:
       ssh.connect(target_host, port=target_port, username=target_username, password=target_password)
       commands = [
           'cd /data/logs/tomcat/merchart',
           'grep "发邮件结束 getVerificationCode 登录邮箱" *'
       ]
       for command in commands:
           stdin, stdout, stderr = ssh.exec_command(command)
           result = stdout.read().decode()
           error = stderr.read().decode()
           if result:
               print(f"命令 {command} 执行结果：")
               print(result)
           if error:
               print(f"命令 {command} 执行错误：")
               print(error)
   except paramiko.AuthenticationException:
       print("认证失败，请验证你的凭证")#
   except paramiko.SSHException as e:
       print(f"不能建立SSH连接: {e}")#
   except Exception as e:
       print(f"错误: {e}")
   finally:
       ssh.close()



import re


def extract_verification_code(log_file_path):
    with open(log_file_path, 'r') as file:
        for line in file:
            match = re.search(r'邮箱验证码为:(\d+)', line)
            if match:
                return match.group(1)
    return None


if __name__ == "__main__":
   try:
       session = login_jumpserver()
       if session:
           execute_commands_on_target(session)
       else:
           print("Failed to log in to Jumpserver.")
   except Exception as e:
       print(f"An unexpected error occurred: {e}")