import requests
import json
import time

# API服务器地址
base_url = "http://localhost:5000"

class ThsApiClient:
    """同花顺API客户端"""
    
    def __init__(self, base_url=base_url):
        self.base_url = base_url
        self.session = requests.Session()
        
    def health_check(self):
        """检查API服务器健康状态"""
        url = f"{self.base_url}/api/ths/health"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "success": False,
                "message": f"健康检查失败: {str(e)}"
            }
    
    def check_passport(self):
        """检查passport.dat文件是否存在"""
        url = f"{self.base_url}/api/ths/check_passport"
        try:
            response = self.session.get(url)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {
                "success": False,
                "message": f"检查passport.dat失败: {str(e)}"
            }
    
    def login(self):
        """登录同花顺API"""
        url = f"{self.base_url}/api/ths/login"
        try:
            # 使用stream=True来处理长响应
            response = self.session.get(url, stream=True, timeout=60)
            response.raise_for_status()
            
            # 逐行读取响应内容
            result = {}
            for line in response.iter_lines():
                if line:
                    line_str = line.decode('utf-8')
                    print(f"API响应: {line_str}")
                    # 尝试解析JSON
                    try:
                        result = json.loads(line_str)
                        break
                    except json.JSONDecodeError:
                        # 不是完整的JSON响应，继续读取
                        continue
            
            return result if result else {
                "success": True,
                "message": "登录请求已发送"
            }
        except requests.Timeout:
            return {
                "success": False,
                "message": "登录请求超时"
            }
        except Exception as e:
            return {
                "success": False,
                "message": f"登录失败: {str(e)}"
            }

# 测试函数
def main():
    """测试同花顺API客户端"""
    print("=== 同花顺API客户端测试 ===")
    
    # 创建客户端实例
    client = ThsApiClient()
    
    # 测试健康检查
    print("\n1. 健康检查:")
    health_result = client.health_check()
    print(json.dumps(health_result, ensure_ascii=False, indent=2))
    
    # 测试检查passport.dat
    print("\n2. 检查passport.dat文件:")
    passport_result = client.check_passport()
    print(json.dumps(passport_result, ensure_ascii=False, indent=2))
    
    # 根据passport.dat是否存在决定是否登录
    if passport_result.get("exists", False):
        print("\n3. 由于passport.dat已存在，测试登录功能（应自动登录）:")
    else:
        print("\n3. 由于passport.dat不存在，测试登录功能（可能需要手动输入验证码）:")
    
    login_result = client.login()
    print(json.dumps(login_result, ensure_ascii=False, indent=2))
    
    # 再次检查passport.dat
    print("\n4. 再次检查passport.dat文件:")
    passport_result_after = client.check_passport()
    print(json.dumps(passport_result_after, ensure_ascii=False, indent=2))
    
    print("\n=== 测试完成 ===")

if __name__ == "__main__":
    main()