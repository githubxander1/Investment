from utils.config_loader import config

class TestPaylabsAPI:
    # 从配置获取基础URL
    BASE_URL = config.current_env['base_url']

    def test_login(self):
        login_url = f"{self.BASE_URL}/paylabs-user-login.html"
        # ...
