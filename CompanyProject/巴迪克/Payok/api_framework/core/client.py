class APIClient:
    """统一请求客户端"""
    def __init__(self, base_url):
        self.session = requests.Session()
        self.base_url = base_url
        
    def send_request(self, method, endpoint, **kwargs):
        response = self.session.request(
            method=method,
            url=f"{self.base_url}/{endpoint}",
            **kwargs
        )
        response.raise_for_status()
        return response.json()