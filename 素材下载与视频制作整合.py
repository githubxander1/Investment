#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
素材下载与剪映MCP整合脚本
此脚本演示如何下载素材并直接用于剪映视频制作
"""

import os
import sys
import time
from typing import List, Optional

# 添加项目路径以便导入模块
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入素材下载模块
try:
    from pie import (
        download_pixabay_videos,
        download_pixabay_images,
        search_pexels_videos,
        download_pexels_video,
        search_unsplash_images,
        download_unsplash_image
    )
except ImportError:
    print("⚠️ 请确保pie.py文件在正确位置")
    sys.exit(1)

# 尝试导入剪映MCP模块
try:
    import mcp_jianying
    JIANYING_AVAILABLE = True
except ImportError:
    JIANYING_AVAILABLE = False
    print("⚠️ 剪映MCP模块不可用，将仅演示素材下载功能")


def download_materials_for_topic(topic: str, api_keys: dict) -> dict:
    """
    为特定主题下载素材
    :param topic: 主题关键词
    :param api_keys: 各平台API密钥字典
    :return: 下载的素材路径字典
    """
    print(f"📥 开始为主题「{topic}」下载素材...")
    
    materials = {
        "videos": [],
        "images": []
    }
    
    # 创建保存目录
    video_dir = f"./materials/{topic}/videos"
    image_dir = f"./materials/{topic}/images"
    
    os.makedirs(video_dir, exist_ok=True)
    os.makedirs(image_dir, exist_ok=True)
    
    # 1. 从Pixabay下载视频
    if "pixabay" in api_keys:
        print("🔍 从Pixabay搜索视频...")
        pixabay_videos = download_pixabay_videos(
            api_key=api_keys["pixabay"],
            q=topic,
            save_dir=video_dir,
            per_page=3,
            video_size="small"
        )
        materials["videos"].extend(pixabay_videos)
    
    # 2. 从Pixabay下载图片
    if "pixabay" in api_keys:
        print("🔍 从Pixabay搜索图片...")
        pixabay_images = download_pixabay_images(
            api_key=api_keys["pixabay"],
            q=topic,
            save_dir=image_dir,
            per_page=5
        )
        materials["images"].extend(pixabay_images)
    
    # 3. 从Pexels下载视频
    if "pexels" in api_keys:
        print("🔍 从Pexels搜索视频...")
        pexels_videos = search_pexels_videos(
            api_key=api_keys["pexels"],
            query=topic,
            per_page=3
        )
        
        for video_data in pexels_videos:
            saved_path = download_pexels_video(video_data, video_dir)
            if saved_path:
                materials["videos"].append(saved_path)
    
    # 4. 从Unsplash下载图片
    if "unsplash" in api_keys:
        print("🔍 从Unsplash搜索图片...")
        unsplash_images = search_unsplash_images(
            api_key=api_keys["unsplash"],
            query=topic,
            per_page=5
        )
        
        for image_data in unsplash_images:
            saved_path = download_unsplash_image(image_data, image_dir)
            if saved_path:
                materials["images"].append(saved_path)
    
    print(f"✅ 素材下载完成！共下载视频{len(materials['videos'])}个，图片{len(materials['images'])}张")
    return materials


def create_video_with_materials(topic: str, materials: dict) -> Optional[str]:
    """
    使用下载的素材创建视频
    :param topic: 视频主题
    :param materials: 素材路径字典
    :return: 视频草稿ID或None
    """
    if not JIANYING_AVAILABLE:
        print("⚠️ 剪映MCP不可用，跳过视频制作步骤")
        return None
    
    try:
        # 创建草稿
        draft_result = mcp_jianying.mcp_create_draft(
            draft_name=f"{topic}视频",
            width=1920,
            height=1080,
            fps=30
        )
        draft_id = draft_result["draft_id"]
        print(f"📄 创建草稿成功: {draft_id}")
        
        # 创建视频轨道
        video_track_result = mcp_jianying.mcp_create_track(
            draft_id=draft_id,
            track_type="video",
            track_name="主视频轨道"
        )
        video_track_id = video_track_result["data"]["track_id"]
        
        # 创建音频轨道
        audio_track_result = mcp_jianying.mcp_create_track(
            draft_id=draft_id,
            track_type="audio",
            track_name="音频轨道"
        )
        audio_track_id = audio_track_result["data"]["track_id"]
        
        # 添加视频素材
        start_time = 0
        for i, video_path in enumerate(materials["videos"][:5]):  # 最多添加5个视频
            if os.path.exists(video_path):
                # 获取视频时长（简化处理，实际应使用媒体信息库）
                duration = 5  # 假设每个视频5秒
                
                mcp_jianying.mcp_add_video_segment(
                    track_id=video_track_id,
                    material=video_path,
                    target_start_end=f"{start_time}s-{start_time + duration}s"
                )
                
                start_time += duration
                print(f"🎞️ 添加视频片段: {os.path.basename(video_path)}")
                time.sleep(0.5)  # 避免请求过快
        
        # 添加图片素材
        for i, image_path in enumerate(materials["images"][:5]):  # 最多添加5张图片
            if os.path.exists(image_path):
                mcp_jianying.mcp_add_video_segment(
                    track_id=video_track_id,
                    material=image_path,
                    target_start_end=f"{start_time}s-{start_time + 3}s"
                )
                
                start_time += 3
                print(f"🖼️ 添加图片片段: {os.path.basename(image_path)}")
                time.sleep(0.5)
        
        print(f"✅ 视频制作完成，草稿ID: {draft_id}")
        return draft_id
        
    except Exception as e:
        print(f"❌ 视频制作失败: {str(e)}")
        return None


def main():
    """
    主函数：演示完整流程
    """
    # 配置API密钥（请替换为您的实际密钥）
    api_keys = {
        "pixabay": "YOUR_PIXABAY_API_KEY",
        "pexels": "YOUR_PEXELS_API_KEY",
        "unsplash": "YOUR_UNSPLASH_API_KEY"
    }
    
    # 视频主题
    topic = "周杰伦本草纲目"
    
    print("=" * 60)
    print(f"🎬 开始制作「{topic}」主题视频")
    print("=" * 60)
    
    # 步骤1: 下载素材
    materials = download_materials_for_topic(topic, api_keys)
    
    if not materials["videos"] and not materials["images"]:
        print("⚠️ 未下载到任何素材，退出程序")
        return
    
    # 步骤2: 制作视频
    draft_id = create_video_with_materials(topic, materials)
    
    if draft_id:
        print(f"🎉 视频草稿创建成功！草稿ID: {draft_id}")
        print("💡 请打开剪映专业版导入草稿进行进一步编辑")
    else:
        print("ℹ️  已完成素材下载，可手动导入剪映使用")


if __name__ == "__main__":
    main()