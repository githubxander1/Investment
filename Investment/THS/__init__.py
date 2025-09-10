# # THS项目初始化文件
# import os
# import sys
# import logging
#
# # 配置日志
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # 将utils目录添加到Python路径中
# utils_path = os.path.join(os.path.dirname(__file__), 'utils')
# if utils_path not in sys.path:
#     sys.path.append(utils_path)
#
# # THS项目初始化文件
# import os
# import sys
# import logging
#
# # 配置日志
# logging.basicConfig(level=logging.INFO)
# logger = logging.getLogger(__name__)
#
# # 将utils目录添加到Python路径中
# utils_path = os.path.join(os.path.dirname(__file__), 'utils')
# if utils_path not in sys.path:
#     sys.path.append(utils_path)
#
# # 初始化全局SSL配置
# try:
#     # 直接导入并应用SSL配置
#     from .utils.ssl_config import patched_request
#     import requests
#
#     # 确保requests使用我们的证书配置
#     requests.Session.request = patched_request
#     logger.info("成功配置全局SSL证书")
# except ImportError as e:
#     # 如果无法导入ssl_config，则使用默认的requests
#     logger.warning(f"无法导入SSL配置: {e}")
# except Exception as e:
#     logger.error(f"配置全局SSL证书时出错: {e}")