#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
综合视频制作工具
整合素材下载、视频编辑和剪映MCP操作
"""

import os
import sys
import json
import time
from typing import List, Dict, Optional

# 添加项目路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# 导入自定义模块
try:
    from pie import (
        download_pixabay_videos,
        download_pixabay_images,
        search_pexels_videos,
        download_pexels_video
    )
    from web_scraper import WebScraper, integrate_with_jianying
except ImportError as e:
    print(f"❌ 模块导入失败: {e}")
    sys.exit(1)

# 剪映MCP相关导入（如果可用）
try:
    # 注意：这里需要根据实际的剪映MCP接口进行调整
    from mcp_jianying import (
        mcp_create_draft,
        mcp_create_track,
        mcp_add_video_segment,
        mcp_add_audio_segment,
        mcp_add_text_segment,
        mcp_export_draft
    )
    JIANYING_AVAILABLE = True
except ImportError:
    JIANYING_AVAILABLE = False
    print("⚠️ 剪映MCP模块不可用，将仅演示素材处理功能")


class VideoMaker:
    """视频制作类"""
    
    def __init__(self, config_file: str = "video_config.json"):
        """
        初始化视频制作器
        :param config_file: 配置文件路径
        """
        self.config_file = config_file
        self.config = self._load_config()
        self.scraper = WebScraper("./materials")
        
    def _load_config(self) -> Dict:
        """
        加载配置文件
        :return: 配置字典
        """
        default_config = {
            "api_keys": {
                "pixabay": "",
                "pexels": ""
            },
            "default_settings": {
                "video_width": 1920,
                "video_height": 1080,
                "fps": 30,
                "max_videos": 10,
                "max_images": 20
            }
        }
        
        if os.path.exists(self.config_file):
            try:
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    config = json.load(f)
                # 合并默认配置和用户配置
                for key, value in default_config.items():
                    if key not in config:
                        config[key] = value
                    elif isinstance(value, dict):
                        for sub_key, sub_value in value.items():
                            if sub_key not in config[key]:
                                config[key][sub_key] = sub_value
                return config
            except Exception as e:
                print(f"⚠️ 配置文件加载失败，使用默认配置: {e}")
        
        # 保存默认配置
        self._save_config(default_config)
        return default_config
    
    def _save_config(self, config: Dict) -> None:
        """
        保存配置文件
        :param config: 配置字典
        """
        try:
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"❌ 配置文件保存失败: {e}")
    
    def download_materials(self, topic: str) -> Dict[str, List[str]]:
        """
        为特定主题下载素材
        :param topic: 主题
        :return: 素材路径字典
        """
        print(f"📥 开始为主题「{topic}」下载素材...")
        
        # 创建主题目录
        topic_dir = os.path.join("./materials", topic)
        video_dir = os.path.join(topic_dir, "videos")
        image_dir = os.path.join(topic_dir, "images")
        
        for directory in [topic_dir, video_dir, image_dir]:
            os.makedirs(directory, exist_ok=True)
        
        materials = {
            "videos": [],
            "images": []
        }
        
        # 从Pixabay下载
        api_keys = self.config.get("api_keys", {})
        
        if api_keys.get("pixabay"):
            print("🔍 从Pixabay下载素材...")
            
            # 下载视频
            pixabay_videos = download_pixabay_videos(
                api_key=api_keys["pixabay"],
                q=topic,
                save_dir=video_dir,
                per_page=5,
                video_size="small"
            )
            materials["videos"].extend(pixabay_videos)
            
            # 下载图片
            pixabay_images = download_pixabay_images(
                api_key=api_keys["pixabay"],
                q=topic,
                save_dir=image_dir,
                per_page=10
            )
            materials["images"].extend(pixabay_images)
        
        # 从Pexels下载视频
        if api_keys.get("pexels"):
            print("🔍 从Pexels下载视频...")
            pexels_videos = search_pexels_videos(
                api_key=api_keys["pexels"],
                query=topic,
                per_page=3
            )
            
            for video_data in pexels_videos:
                saved_path = download_pexels_video(video_data, video_dir)
                if saved_path:
                    materials["videos"].append(saved_path)
        
        # 使用网络爬虫补充素材
        print("🕷️  使用网络爬虫补充素材...")
        scraped_images = self.scraper.search_free_images(topic, max_results=5)
        saved_images = self.scraper.download_images(scraped_images, f"{topic}_web")
        materials["images"].extend(saved_images)
        
        print(f"✅ 素材下载完成！共下载视频{len(materials['videos'])}个，图片{len(materials['images'])}张")
        return materials
    
    def create_video_draft(self, topic: str, materials: Dict[str, List[str]]) -> Optional[str]:
        """
        创建视频草稿
        :param topic: 视频主题
        :param materials: 素材路径
        :return: 草稿ID或None
        """
        if not JIANYING_AVAILABLE:
            print("⚠️ 剪映MCP不可用，跳过视频草稿创建")
            return None
        
        try:
            print("📄 创建视频草稿...")
            
            # 创建草稿
            draft_result = mcp_create_draft(
                draft_name=f"{topic}MV",
                width=self.config["default_settings"]["video_width"],
                height=self.config["default_settings"]["video_height"],
                fps=self.config["default_settings"]["fps"]
            )
            draft_id = draft_result.get("draft_id") if isinstance(draft_result, dict) else draft_result
            
            if not draft_id:
                print("❌ 草稿创建失败")
                return None
            
            print(f"✅ 草稿创建成功: {draft_id}")
            
            # 创建轨道
            print(" トラック 创建视频轨道...")
            video_track_result = mcp_create_track(
                draft_id=draft_id,
                track_type="video",
                track_name="视频轨道"
            )
            
            video_track_id = video_track_result["data"]["track_id"] if isinstance(video_track_result, dict) else None
            
            if not video_track_id:
                print("❌ 视频轨道创建失败")
                return draft_id
            
            # 添加视频素材
            print("🎞️ 添加视频素材...")
            start_time = 0
            max_duration = 30  # 总时长限制为30秒
            
            for i, video_path in enumerate(materials["videos"]):
                if start_time >= max_duration:
                    break
                    
                if os.path.exists(video_path):
                    # 简化处理，假设每个视频片段5秒
                    segment_duration = min(5, max_duration - start_time)
                    end_time = start_time + segment_duration
                    
                    try:
                        mcp_add_video_segment(
                            track_id=video_track_id,
                            material=video_path,
                            target_start_end=f"{start_time}s-{end_time}s"
                        )
                        start_time = end_time
                        print(f"➕ 添加视频: {os.path.basename(video_path)} ({segment_duration}秒)")
                    except Exception as e:
                        print(f"⚠️ 视频添加失败 {video_path}: {e}")
                
                time.sleep(0.1)  # 避免请求过快
            
            # 添加图片素材作为补充
            print("🖼️ 添加图片素材...")
            for i, image_path in enumerate(materials["images"]):
                if start_time >= max_duration:
                    break
                    
                if os.path.exists(image_path):
                    # 每张图片显示3秒
                    segment_duration = min(3, max_duration - start_time)
                    end_time = start_time + segment_duration
                    
                    try:
                        mcp_add_video_segment(
                            track_id=video_track_id,
                            material=image_path,
                            target_start_end=f"{start_time}s-{end_time}s"
                        )
                        start_time = end_time
                        print(f"➕ 添加图片: {os.path.basename(image_path)} ({segment_duration}秒)")
                    except Exception as e:
                        print(f"⚠️ 图片添加失败 {image_path}: {e}")
                
                time.sleep(0.1)
            
            return draft_id
            
        except Exception as e:
            print(f"❌ 视频草稿创建过程中出错: {e}")
            return None
    
    def add_background_music(self, draft_id: str, music_path: str) -> bool:
        """
        添加背景音乐
        :param draft_id: 草稿ID
        :param music_path: 音乐文件路径
        :return: 是否成功
        """
        if not JIANYING_AVAILABLE:
            return False
        
        try:
            # 创建音频轨道
            audio_track_result = mcp_create_track(
                draft_id=draft_id,
                track_type="audio",
                track_name="背景音乐"
            )
            
            audio_track_id = audio_track_result["data"]["track_id"]
            
            # 添加音频
            mcp_add_audio_segment(
                track_id=audio_track_id,
                material=music_path,
                target_start_end="0s-30s"  # 假设音乐时长30秒
            )
            
            print("🎵 背景音乐添加成功")
            return True
        except Exception as e:
            print(f"❌ 背景音乐添加失败: {e}")
            return False
    
    def add_subtitles(self, draft_id: str, subtitles: List[Dict]) -> bool:
        """
        添加字幕
        :param draft_id: 草稿ID
        :param subtitles: 字幕列表 [{"text": "字幕内容", "start": 0, "end": 5}]
        :return: 是否成功
        """
        if not JIANYING_AVAILABLE:
            return False
        
        try:
            # 创建文本轨道
            text_track_result = mcp_create_track(
                draft_id=draft_id,
                track_type="text",
                track_name="字幕轨道"
            )
            
            text_track_id = text_track_result["data"]["track_id"]
            
            # 添加字幕
            for subtitle in subtitles:
                mcp_add_text_segment(
                    track_id=text_track_id,
                    text=subtitle["text"],
                    target_start_end=f"{subtitle['start']}s-{subtitle['end']}s",
                    style={"size": 8.0, "color": [1.0, 1.0, 1.0], "align": 1},
                    clip_settings={"transform_y": -0.7}
                )
            
            print("💬 字幕添加成功")
            return True
        except Exception as e:
            print(f"❌ 字幕添加失败: {e}")
            return False
    
    def export_video(self, draft_id: str, output_path: str) -> bool:
        """
        导出视频
        :param draft_id: 草稿ID
        :param output_path: 输出路径
        :return: 是否成功
        """
        if not JIANYING_AVAILABLE:
            print("⚠️ 剪映MCP不可用，无法导出视频")
            return False
        
        try:
            print("📤 开始导出视频...")
            result = mcp_export_draft(
                draft_id=draft_id,
                jianying_draft_path=output_path
            )
            
            if result.get("success"):
                print(f"✅ 视频导出成功: {result.get('data', {}).get('output_path', '未知路径')}")
                return True
            else:
                print(f"❌ 视频导出失败: {result.get('message', '未知错误')}")
                return False
        except Exception as e:
            print(f"❌ 导出过程中出错: {e}")
            return False
    
    def make_video(self, topic: str, subtitles: Optional[List[Dict]] = None) -> bool:
        """
        制作完整视频
        :param topic: 视频主题
        :param subtitles: 字幕数据
        :return: 是否成功
        """
        print(f"🎬 开始制作视频: {topic}")
        
        # 1. 下载素材
        materials = self.download_materials(topic)
        
        if not materials["videos"] and not materials["images"]:
            print("❌ 未获取到任何素材，无法制作视频")
            return False
        
        # 2. 创建草稿
        draft_id = self.create_video_draft(topic, materials)
        
        if not draft_id:
            print("❌ 视频草稿创建失败")
            return False
        
        # 3. 添加字幕（如果有）
        if subtitles:
            self.add_subtitles(draft_id, subtitles)
        
        # 4. 导出视频
        output_dir = f"./output/{topic}"
        os.makedirs(output_dir, exist_ok=True)
        
        success = self.export_video(draft_id, output_dir)
        
        if success:
            print(f"🎉 视频制作完成！请在 {output_dir} 查看结果")
        else:
            print("⚠️ 视频导出失败，请手动在剪映中打开草稿")
        
        return success


def main():
    """主函数"""
    # 创建视频制作器实例
    video_maker = VideoMaker()
    
    # 示例：制作周杰伦《本草纲目》MV
    topic = "周杰伦本草纲目"
    
    # 字幕示例
    subtitles = [
        {"text": "周杰伦 - 本草纲目", "start": 0, "end": 5},
        {"text": "如果华佗再世 崇洋都被医治", "start": 5, "end": 10},
        {"text": "外邦来学汉字 激发我民族意识", "start": 10, "end": 15},
        {"text": "马钱子决明子苍耳子 还有莲子", "start": 15, "end": 20},
        {"text": "黄药子苦豆子 红花七叶子", "start": 20, "end": 25},
        {"text": "本草纲目", "start": 25, "end": 30}
    ]
    
    # 执行视频制作
    success = video_maker.make_video(topic, subtitles)
    
    if success:
        print("✅ 视频制作流程完成")
    else:
        print("❌ 视频制作流程出现错误")


if __name__ == "__main__":
    main()