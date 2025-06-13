import requests
import pytest
import allure

# 定义测试类
class TestPaylabsAPI:

    # 定义基础 URL
    BASE_URL = "http://paylabs-test.com/merchant"

    @allure.feature("Paylabs 登录接口测试")
    @allure.story("登录流程测试")
    def test_paylabs_login(self):
        """
        测试 Paylabs 登录接口
        """
        # 定义登录页面 URL
        login_url = f"{self.BASE_URL}/logic-user-login.html"
        try:
            # 发送 GET 请求获取登录页面
            response = requests.get(login_url)
            # 检查响应状态码是否为 200
            assert response.status_code == 200
            allure.attach(str(response.text), "登录页面响应内容", allure.attachment_type.TEXT)
        except requests.RequestException as e:
            allure.attach(str(e), "请求异常信息", allure.attachment_type.TEXT)
            pytest.fail(f"请求登录页面失败: {e}")

    @allure.feature("Paylabs 登录接口测试")
    @allure.story("验证码验证测试")
    def test_verify_move_block(self):
        """
        测试验证码验证接口
        """
        # 假设存在一个验证码验证接口
        verify_url = f"{self.BASE_URL}/verify-move-block"
        try:
            # 发送 POST 请求进行验证码验证
            response = requests.post(verify_url)
            # 检查响应状态码是否为 200
            assert response.status_code == 200
            allure.attach(str(response.text), "验证码验证响应内容", allure.attachment_type.TEXT)
        except requests.RequestException as e:
            allure.attach(str(e), "请求异常信息", allure.attachment_type.TEXT)
            pytest.fail(f"请求验证码验证接口失败: {e}")

    @allure.feature("Paylabs 登录接口测试")
    @allure.story("登录按钮点击测试")
    def test_login_button_click(self):
        """
        测试登录按钮点击对应的接口
        """
        # 假设存在一个登录按钮点击对应的接口
        login_button_url = f"{self.BASE_URL}/btnLogin"
        try:
            # 发送 POST 请求模拟点击登录按钮
            response = requests.post(login_button_url)
            # 检查响应状态码是否为 200
            assert response.status_code == 200
            allure.attach(str(response.text), "登录按钮点击响应内容", allure.attachment_type.TEXT)
        except requests.RequestException as e:
            allure.attach(str(e), "请求异常信息", allure.attachment_type.TEXT)
            pytest.fail(f"请求登录按钮点击接口失败: {e}")

    @allure.feature("Paylabs 登录接口测试")
    @allure.story("谷歌验证码输入测试")
    def test_google_code_input(self):
        """
        测试谷歌验证码输入接口
        """
        # 假设存在一个谷歌验证码输入接口
        google_code_url = f"{self.BASE_URL}/googleCode"
        try:
            # 发送 POST 请求模拟输入谷歌验证码
            response = requests.post(google_code_url)
            # 检查响应状态码是否为 200
            assert response.status_code == 200
            allure.attach(str(response.text), "谷歌验证码输入响应内容", allure.attachment_type.TEXT)
        except requests.RequestException as e:
            allure.attach(str(e), "请求异常信息", allure.attachment_type.TEXT)
            pytest.fail(f"请求谷歌验证码输入接口失败: {e}")

    @allure.feature("Paylabs 登录接口测试")
    @allure.story("谷歌登录按钮点击测试")
    def test_google_login_button_click(self):
        """
        测试谷歌登录按钮点击对应的接口
        """
        # 假设存在一个谷歌登录按钮点击对应的接口
        google_login_button_url = f"{self.BASE_URL}/btnGoogleLogin"
        try:
            # 发送 POST 请求模拟点击谷歌登录按钮
            response = requests.post(google_login_button_url)
            # 检查响应状态码是否为 200
            assert response.status_code == 200
            allure.attach(str(response.text), "谷歌登录按钮点击响应内容", allure.attachment_type.TEXT)
        except requests.RequestException as e:
            allure.attach(str(e), "请求异常信息", allure.attachment_type.TEXT)
            pytest.fail(f"请求谷歌登录按钮点击接口失败: {e}")

if __name__ == '__main__':
    pytest.main(["-s", "test_paylabs_login.py"])