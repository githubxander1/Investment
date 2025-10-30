import os
import pandas as pd
from datetime import datetime
import logging
from typing import List, Optional
import sys
import importlib

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 动态导入两个代理爬虫模块
try:
    import free_proxy
    import proxynova
    from proxy_utils import decode_js_ip, is_valid_ip, verify_proxy_curl_style
except ImportError as e:
    logging.error(f"导入代理模块失败: {e}")
    raise

class ProxyManager:
    """代理管理器，用于整合多个代理源并提供统一接口"""
    
    def __init__(self, proxy_data_dir: str = "./proxy_data"):
        """
        初始化代理管理器
        
        Args:
            proxy_data_dir: 代理数据保存目录
        """
        self.proxy_data_dir = proxy_data_dir
        self.sources = ["free_proxy", "proxynova"]
        
        # 确保数据目录存在
        if not os.path.exists(self.proxy_data_dir):
            os.makedirs(self.proxy_data_dir)
            
        # 初始化日志
        self._init_logger()
        
    def _init_logger(self):
        """初始化日志系统"""
        log_format = "%(asctime)s - %(levelname)s - %(module)s:%(funcName)s - %(message)s"
        logging.basicConfig(
            level=logging.INFO,
            format=log_format,
            handlers=[
                logging.StreamHandler(),
                logging.FileHandler(os.path.join(self.proxy_data_dir, "proxy_manager.log"), encoding="utf-8")
            ]
        )
        
    def get_proxies_from_source(self, source: str, max_workers: int = 10, verify_timeout: float = 5.0) -> pd.DataFrame:
        """
        从指定源获取代理
        
        Args:
            source: 代理源名称 ("free_proxy" 或 "proxynova")
            max_workers: 验证代理的最大并发线程数
            verify_timeout: 验证超时时间
            
        Returns:
            pd.DataFrame: 代理数据
        """
        try:
            if source == "free_proxy":
                # 从free-proxy-list.net获取代理
                df = free_proxy.crawl_free_proxies(
                    target_url="https://free-proxy-list.net",
                    save_dir=self.proxy_data_dir,
                    verify_proxies=True,
                    max_workers=max_workers,
                    verify_timeout=verify_timeout
                )
                return df
            elif source == "proxynova":
                # 从proxynova获取代理
                df = proxynova.crawl_proxies(
                    # url="https://www.proxynova.com/proxy-server-list/",
                    url="https://www.proxynova.com/proxy-server-list/country-cn/",
                    save_dir=self.proxy_data_dir,
                    verify_proxies=True,
                    max_workers=max_workers,
                    verify_timeout=verify_timeout
                )
                return df
            else:
                logging.warning(f"未知的代理源: {source}")
                return pd.DataFrame()
        except Exception as e:
            logging.error(f"从 {source} 获取代理失败: {e}")
            return pd.DataFrame()
            
    def get_proxies(self, max_workers: int = 10, verify_timeout: float = 5.0, 
                   fallback: bool = True) -> pd.DataFrame:
        """
        获取代理，支持自动切换源
        
        Args:
            max_workers: 验证代理的最大并发线程数
            verify_timeout: 验证超时时间
            fallback: 是否启用备用源（一个源失败时切换到另一个）
            
        Returns:
            pd.DataFrame: 代理数据
        """
        logging.info("🔄 开始获取代理数据...")
        
        # 尝试从主源获取
        primary_source = self.sources[0]
        logging.info(f"📡 尝试从主源 {primary_source} 获取代理...")
        proxies_df = self.get_proxies_from_source(
            source=primary_source, 
            max_workers=max_workers, 
            verify_timeout=verify_timeout
        )
        
        # 如果主源失败且启用了备用源，则尝试备用源
        if fallback and (proxies_df is None or proxies_df.empty):
            logging.warning(f"主源 {primary_source} 获取代理失败，尝试备用源...")
            for source in self.sources[1:]:
                logging.info(f"📡 尝试从备用源 {source} 获取代理...")
                proxies_df = self.get_proxies_from_source(
                    source=source, 
                    max_workers=max_workers, 
                    verify_timeout=verify_timeout
                )
                if proxies_df is not None and not proxies_df.empty:
                    logging.info(f"✅ 成功从备用源 {source} 获取到 {len(proxies_df)} 个代理")
                    break
                    
        # 如果所有源都失败
        if proxies_df is None or proxies_df.empty:
            logging.error("❌ 所有代理源都未能获取到有效代理")
            return pd.DataFrame()
            
        logging.info(f"✅ 成功获取到 {len(proxies_df)} 个有效代理")
        
        # 保存合并后的代理数据
        today_date = datetime.now().strftime("%Y%m%d")
        merged_file_path = os.path.join(
            self.proxy_data_dir, 
            f"merged_proxies_valid_{today_date}.csv"
        )
        proxies_df.to_csv(merged_file_path, index=False, encoding="utf-8-sig")
        logging.info(f"💾 合并后的代理数据已保存到: {merged_file_path}")
        
        return proxies_df
        
    def get_latest_proxies(self) -> Optional[pd.DataFrame]:
        """
        获取最新的代理数据（从已保存的文件中）
        
        Returns:
            pd.DataFrame: 最新的代理数据，如果不存在则返回None
        """
        # 查找最新的合并文件
        try:
            files = [f for f in os.listdir(self.proxy_data_dir) if f.startswith("merged_proxies_valid_") and f.endswith(".csv")]
            if not files:
                logging.warning("未找到合并后的代理文件")
                return None
                
            # 按文件名排序，获取最新的
            files.sort(reverse=True)
            latest_file = files[0]
            file_path = os.path.join(self.proxy_data_dir, latest_file)
            
            df = pd.read_csv(file_path)
            logging.info(f"📁 从 {latest_file} 加载了 {len(df)} 个代理")
            return df
        except Exception as e:
            logging.error(f"加载最新代理数据失败: {e}")
            return None

def main():
    """主函数，用于测试代理管理器"""
    # 创建代理管理器
    manager = ProxyManager("./proxy_data")
    
    # 获取代理
    proxies = manager.get_proxies(max_workers=10, verify_timeout=5.0, fallback=True)
    
    if not proxies.empty:
        print(f"✅ 成功获取到 {len(proxies)} 个有效代理:")
        print(proxies.head())
    else:
        print("❌ 未能获取到任何有效代理")
        
    # 显示最新代理数据
    latest_proxies = manager.get_latest_proxies()
    if latest_proxies is not None:
        print(f"\n📁 最新代理数据包含 {len(latest_proxies)} 个代理")

if __name__ == "__main__":
    main()