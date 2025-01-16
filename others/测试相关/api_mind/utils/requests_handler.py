import requests
class RequestsHandler:
    def __init__(self):
        """session管理器"""
        self.session = requests.session()

    def visit(self, url, method, params=None, data=None, json=None, headers=None):
        # self.logger.info(f"Sending {method} request to {url}")
        # self.logger.debug(f"Params: {params}, Data: {data}, JSON: {json}, Headers: {headers}")
        try:
            response = self.session.request(url=url, method=method, params=params, data=data, json=json,
                                            headers=headers)
            response.raise_for_status()  # Raise an HTTPError for bad responses (4xx and 5xx)
            try:
                # 返回 JSON 结果
                # self.logger.debug(f"Response JSON: {response.json()}")
                return response
            except ValueError:
                # 如果响应不是 JSON 格式，返回原始响应内容
                # self.logger.debug(f"Response Content: {response.content}")
                return response.content
        except requests.exceptions.HTTPError as http_err:
            # self.logger.error(f"HTTP error occurred: {http_err}")
            return {"error": str(http_err)}
        except requests.exceptions.ConnectionError as conn_err:
            # self.logger.error(f"Connection error occurred: {conn_err}")
            return {"error": str(conn_err)}
        except requests.exceptions.Timeout as timeout_err:
            # self.logger.error(f"Timeout error occurred: {timeout_err}")
            return {"error": str(timeout_err)}
        except requests.exceptions.RequestException as req_err:
            # self.logger.error(f"An error occurred: {req_err}")
            return {"error": str(req_err)}

    def close_session(self):
        # self.logger.info("Closing session")
        self.session.close()