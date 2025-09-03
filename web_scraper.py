#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
网络爬虫模块 - 用于从互联网上抓取视频和图片素材
注意：此模块仅供学习交流使用，请遵守各网站的使用条款和版权规定
"""

import requests
import os
import time
import random
from typing import List, Optional
from urllib.parse import urljoin, urlparse
from bs4 import BeautifulSoup


class WebScraper:
    """网络爬虫类"""
    
    def __init__(self, save_dir: str = "./scraped_materials"):
        """
        初始化爬虫
        :param save_dir: 保存目录
        """
        self.save_dir = save_dir
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        
        # 创建保存目录
        os.makedirs(save_dir, exist_ok=True)
        os.makedirs(os.path.join(save_dir, "images"), exist_ok=True)
        os.makedirs(os.path.join(save_dir, "videos"), exist_ok=True)
    
    def _download_file(self, url: str, save_path: str) -> bool:
        """
        下载文件
        :param url: 文件URL
        :param save_path: 保存路径
        :return: 是否成功
        """
        try:
            response = self.session.get(url, timeout=30, stream=True)
            response.raise_for_status()
            
            with open(save_path, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            
            print(f"✅ 下载成功: {os.path.basename(save_path)}")
            return True
        except Exception as e:
            print(f"❌ 下载失败 {url}: {str(e)}")
            return False
    
    def search_free_images(self, keywords: str, max_results: int = 10) -> List[str]:
        """
        从免费图库搜索图片（示例实现）
        :param keywords: 搜索关键词
        :param max_results: 最大结果数
        :return: 图片URL列表
        """
        # 这里仅作示例，实际使用时需要根据目标网站调整
        image_urls = []
        
        # 模拟搜索结果
        print(f"🔍 搜索图片关键词: {keywords}")
        
        # 示例URL（实际使用时需要从真实网站抓取）
        sample_urls = [
            "https://picsum.photos/1920/1080",
            "https://picsum.photos/1280/720",
            "https://picsum.photos/800/600"
        ]
        
        for i in range(min(max_results, len(sample_urls))):
            # 使用Lorem Picsum生成随机图片
            image_urls.append(f"{sample_urls[i%len(sample_urls)]}?random={random.randint(1, 1000)}")
            time.sleep(0.1)  # 避免请求过快
        
        return image_urls
    
    def download_images(self, urls: List[str], prefix: str = "scraped") -> List[str]:
        """
        下载图片
        :param urls: 图片URL列表
        :param prefix: 文件名前缀
        :return: 成功下载的文件路径列表
        """
        saved_paths = []
        images_dir = os.path.join(self.save_dir, "images")
        
        for i, url in enumerate(urls):
            try:
                # 生成文件名
                parsed_url = urlparse(url)
                ext = os.path.splitext(parsed_url.path)[1] or ".jpg"
                filename = f"{prefix}_{i+1:03d}{ext}"
                save_path = os.path.join(images_dir, filename)
                
                # 下载文件
                if self._download_file(url, save_path):
                    saved_paths.append(save_path)
                
                # 避免请求过快
                time.sleep(random.uniform(0.5, 1.5))
                
            except Exception as e:
                print(f"❌ 处理图片失败 {url}: {str(e)}")
        
        return saved_paths
    
    def search_video_sites(self, keywords: str) -> List[str]:
        """
        搜索视频网站（仅返回示例数据）
        :param keywords: 搜索关键词
        :return: 视频页面URL列表
        """
        print(f"🔍 搜索视频关键词: {keywords}")
        
        # 示例视频网站（实际使用时需要解析网站内容）
        video_sites = [
            "https://www.videvo.net/",
            "https://www.videezy.com/",
            "https://coverr.co/",
            "https://mixkit.co/"
        ]
        
        return video_sites
    
    def get_trending_videos(self, site_url: str, category: str = "all") -> List[dict]:
        """
        获取热门视频（示例实现）
        :param site_url: 网站URL
        :param category: 分类
        :return: 视频信息列表
        """
        print(f"📈 获取 {site_url} 的热门视频...")
        
        # 示例数据
        sample_videos = [
            {
                "title": "Nature Landscape",
                "url": "https://sample-videos.com/zip.php?file=video1.zip",
                "duration": "0:30",
                "resolution": "1920x1080"
            },
            {
                "title": "City Time-lapse",
                "url": "https://sample-videos.com/zip.php?file=video2.zip",
                "duration": "0:45",
                "resolution": "1280x720"
            }
        ]
        
        return sample_videos
    
    def download_video(self, video_info: dict, prefix: str = "scraped") -> Optional[str]:
        """
        下载视频（示例实现）
        :param video_info: 视频信息
        :param prefix: 文件名前缀
        :return: 保存路径或None
        """
        try:
            video_url = video_info.get("url")
            if not video_url:
                return None
            
            videos_dir = os.path.join(self.save_dir, "videos")
            title = video_info.get("title", "untitled")
            filename = f"{prefix}_{title.replace(' ', '_')}.mp4"
            save_path = os.path.join(videos_dir, filename)
            
            if self._download_file(video_url, save_path):
                return save_path
        except Exception as e:
            print(f"❌ 下载视频失败: {str(e)}")
        
        return None


def integrate_with_jianying(materials_dir: str = "./scraped_materials") -> dict:
    """
    与剪映集成
    :param materials_dir: 素材目录
    :return: 可用于剪映的素材信息
    """
    images_dir = os.path.join(materials_dir, "images")
    videos_dir = os.path.join(materials_dir, "videos")
    
    materials = {
        "images": [],
        "videos": []
    }
    
    # 收集图片
    if os.path.exists(images_dir):
        for file in os.listdir(images_dir):
            if file.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                materials["images"].append(os.path.join(images_dir, file))
    
    # 收集视频
    if os.path.exists(videos_dir):
        for file in os.listdir(videos_dir):
            if file.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
                materials["videos"].append(os.path.join(videos_dir, file))
    
    return materials


# 使用示例
if __name__ == "__main__":
    # 创建爬虫实例
    scraper = WebScraper("./downloaded_materials")
    
    # 搜索并下载图片
    print("开始下载图片素材...")
    image_urls = scraper.search_free_images("nature landscape", max_results=5)
    saved_images = scraper.download_images(image_urls, "nature")
    print(f"图片下载完成: {len(saved_images)} 张")
    
    # 搜索视频网站
    print("\n搜索视频素材来源...")
    video_sites = scraper.search_video_sites("music video")
    print(f"找到视频网站: {len(video_sites)} 个")
    
    # 获取热门视频
    if video_sites:
        trending_videos = scraper.get_trending_videos(video_sites[0])
        print(f"获取到 {len(trending_videos)} 个热门视频")
    
    # 与剪映集成
    print("\n整合素材用于剪映...")
    materials = integrate_with_jianying("./downloaded_materials")
    print(f"可用于剪映的素材: {len(materials['images'])} 张图片, {len(materials['videos'])} 个视频")