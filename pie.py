import requests
import os
from typing import Optional, List
from requests.exceptions import RequestException
import json
from urllib.parse import quote


def _create_save_dir(save_dir: str) -> None:
    """
    辅助函数：创建保存目录（若不存在）
    :param save_dir: 本地保存目录路径
    """
    if not os.path.exists(save_dir):
        os.makedirs(save_dir, exist_ok=True)
        print(f"已创建保存目录：{save_dir}")


def _download_media(media_url: str, save_path: str) -> bool:
    """
    辅助函数：下载单个媒体文件（图片/视频）到本地
    :param media_url: 媒体文件的远程URL
    :param save_path: 本地保存路径（含文件名）
    :return: 下载成功返回True，失败返回False
    """
    try:
        # 发送GET请求获取媒体流（设置超时避免长期阻塞）
        response = requests.get(media_url, stream=True, timeout=15)
        response.raise_for_status()  # 若状态码非200，抛出HTTP错误

        # 写入文件（二进制模式，适用于图片/视频）
        with open(save_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=1024 * 1024):  # 1MB分块下载
                if chunk:
                    f.write(chunk)

        print(f"✅ 成功下载：{os.path.basename(save_path)}")
        return True

    except RequestException as e:
        print(f"❌ 下载失败（URL: {media_url}）：{str(e)}")
        return False


def download_pixabay_images(
        api_key: str,
        q: str,
        save_dir: str = "./pixabay_images",
        per_page: int = 10,
        page: int = 1,
        image_type: str = "photo",
        orientation: str = "all"
) -> List[str]:
    """
    从Pixabay API搜索并下载图片
    :param api_key: Pixabay API密钥（必填，从Pixabay账号获取）
    :param q: 搜索关键词（如"yellow flowers"，URL编码由函数自动处理）
    :param save_dir: 本地保存目录（默认：./pixabay_images）
    :param per_page: 每页下载数量（3-200，默认10，遵循API限制）
    :param page: 分页页码（默认1，用于获取多页结果）
    :param image_type: 图片类型（all/photo/illustration/vector，默认photo）
    :param orientation: 图片方向（all/horizontal/vertical，默认all）
    :return: 成功下载的本地文件路径列表
    """
    # 1. 初始化配置
    _create_save_dir(save_dir)
    success_paths = []
    api_url = "https://pixabay.com/api/"  # 图片API端点

    # 2. 构造API请求参数（严格遵循Pixabay API文档）
    params = {
        "key": api_key,
        "q": q,
        "image_type": image_type,
        "orientation": orientation,
        "per_page": per_page,
        "page": page,
        "pretty": "false"  # 生产环境禁用缩进，提高效率
    }

    try:
        # 3. 发送API请求（获取图片列表）
        response = requests.get(api_url, params=params, timeout=10)
        response.raise_for_status()  # 捕获HTTP错误（如429速率限制、400参数错误）
        api_data = response.json()

        # 4. 解析API响应（检查是否有结果）
        total_hits = api_data.get("totalHits", 0)
        if total_hits == 0:
            print(f"⚠️ 未找到关键词「{q}」的图片结果")
            return success_paths

        print(f"📥 找到{total_hits}张图片，开始下载第{page}页（共{per_page}张）...")

        # 5. 遍历图片结果，提取URL并下载
        for idx, hit in enumerate(api_data["hits"], 1):
            # 提取图片URL（webformatURL：640px中等尺寸，24小时有效，符合API规范）
            img_url = hit.get("webformatURL")
            if not img_url:
                print(f"⚠️ 跳过第{idx}张图片：未获取到有效URL")
                continue

            # 生成本地保存路径（避免文件名重复，加序号）
            img_filename = f"pixabay_img_{hit['id']}_{idx}.jpg"  # 用图片ID确保唯一性
            save_path = os.path.join(save_dir, img_filename)

            # 下载图片并记录成功路径
            if _download_media(img_url, save_path):
                success_paths.append(save_path)

    except RequestException as e:
        print(f"❌ API请求失败：{str(e)}")
        # 特殊提示：速率限制（429错误）
        if response.status_code == 429:
            reset_time = response.headers.get("X-RateLimit-Reset", "未知")
            print(f"⚠️ 已超过API速率限制（100次/60秒），请{reset_time}秒后重试")

    return success_paths


def download_pixabay_videos(
    api_key: str,
    q: str,
    save_dir: str = "./pixabay_videos",
    per_page: int = 5,
    page: int = 1,
    video_type: str = "film",
    video_size: str = "medium"
) -> List[str]:
    """
    从Pixabay API搜索并下载视频
    :param api_key: Pixabay API密钥（必填）
    :param q: 搜索关键词（如"ocean wave"）
    :param save_dir: 本地保存目录（默认：./pixabay_videos）
    :param per_page: 每页下载数量（3-200，默认5，视频文件较大建议少选）
    :param page: 分页页码（默认1）
    :param video_type: 视频类型（all/film/animation，默认film）
    :param video_size: 视频尺寸（large/medium/small/tiny，默认medium，API文档推荐）
    :return: 成功下载的本地文件路径列表
    """
    # 1. 初始化配置
    _create_save_dir(save_dir)
    success_paths = []
    api_url = "https://pixabay.com/api/videos/"  # 视频API端点
    valid_sizes = ["large", "medium", "small", "tiny"]

    # 检查视频尺寸是否合法
    if video_size not in valid_sizes:
        print(f"⚠️ 无效视频尺寸「{video_size}」，自动使用默认值「medium」")
        video_size = "medium"

    # 2. 构造API请求参数
    params = {
        "key": api_key,
        "q": q,
        "video_type": video_type,
        "per_page": per_page,
        "page": page,
        "pretty": "false"
    }

    try:
        # 3. 发送API请求
        response = requests.get(api_url, params=params, timeout=15)
        # 关键优化：打印400错误的具体响应内容（API会明确说明错误原因）
        if response.status_code == 400:
            print(f"❌ 视频API参数错误，详情：{response.text}")  # 重点！看这里的错误提示
            return success_paths

        response.raise_for_status()  # 捕获其他HTTP错误（如401权限、429速率）
        api_data = response.json()

        # 4. 解析响应
        total_hits = api_data.get("totalHits", 0)
        if total_hits == 0:
            print(f"⚠️ 未找到关键词「{q}」的视频结果")
            return success_paths

        print(f"📥 找到{total_hits}个视频，开始下载第{page}页（共{per_page}个，尺寸：{video_size}）...")

        # 5. 遍历视频结果，提取对应尺寸的URL并下载
        for idx, hit in enumerate(api_data["hits"], 1):
            # 提取指定尺寸的视频URL（视频API返回多尺寸字典）
            video_info = hit.get("videos", {}).get(video_size)
            if not video_info or not video_info.get("url"):
                print(f"⚠️ 跳过第{idx}个视频：未获取到「{video_size}」尺寸的URL")
                continue

            video_url = video_info["url"]

            # 生成本地保存路径（用视频ID确保唯一性）
            video_filename = f"pixabay_video_{hit['id']}_{idx}.mp4"
            save_path = os.path.join(save_dir, video_filename)

            # 下载视频并记录成功路径
            if _download_media(video_url, save_path):
                success_paths.append(save_path)

    except RequestException as e:
        print(f"❌ 视频API请求失败：{str(e)}")
        # 速率限制提示
        if 'response' in locals() and response.status_code == 429:
            reset_time = response.headers.get("X-RateLimit-Reset", "未知")
            print(f"⚠️ 已超过API速率限制，請{reset_time}秒后重试")

    return success_paths


def search_pexels_videos(
    api_key: str,
    query: str,
    per_page: int = 5,
    page: int = 1,
    orientation: str = "landscape"
) -> List[dict]:
    """
    从Pexels搜索视频素材
    :param api_key: Pexels API密钥
    :param query: 搜索关键词
    :param per_page: 每页数量（默认5）
    :param page: 页码（默认1）
    :param orientation: 视频方向（landscape, portrait, square）
    :return: 视频信息列表
    """
    url = "https://api.pexels.com/videos/search"
    headers = {
        "Authorization": api_key
    }
    params = {
        "query": query,
        "per_page": per_page,
        "page": page,
        "orientation": orientation
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("videos", [])
    except Exception as e:
        print(f"❌ Pexels视频搜索失败：{str(e)}")
        return []


def download_pexels_video(video_data: dict, save_dir: str = "./pexels_videos") -> Optional[str]:
    """
    下载Pexels视频
    :param video_data: Pexels视频数据
    :param save_dir: 保存目录
    :return: 保存路径或None
    """
    _create_save_dir(save_dir)
    
    # 获取视频链接（选择最高质量）
    video_files = video_data.get("video_files", [])
    if not video_files:
        print("⚠️ 视频数据中未找到视频文件")
        return None
    
    # 选择第一个视频文件（通常是最高质量）
    video_url = video_files[0].get("link")
    if not video_url:
        print("⚠️ 未找到有效的视频链接")
        return None
    
    # 生成文件名
    video_id = video_data.get("id", "unknown")
    save_path = os.path.join(save_dir, f"pexels_video_{video_id}.mp4")
    
    # 下载视频
    if _download_media(video_url, save_path):
        return save_path
    return None


def search_unsplash_images(
    api_key: str,
    query: str,
    per_page: int = 10,
    page: int = 1
) -> List[dict]:
    """
    从Unsplash搜索图片素材
    :param api_key: Unsplash API密钥
    :param query: 搜索关键词
    :param per_page: 每页数量
    :param page: 页码
    :return: 图片信息列表
    """
    url = "https://api.unsplash.com/search/photos"
    headers = {
        "Authorization": f"Client-ID {api_key}"
    }
    params = {
        "query": query,
        "per_page": per_page,
        "page": page
    }
    
    try:
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("results", [])
    except Exception as e:
        print(f"❌ Unsplash图片搜索失败：{str(e)}")
        return []


def download_unsplash_image(image_data: dict, save_dir: str = "./unsplash_images") -> Optional[str]:
    """
    下载Unsplash图片
    :param image_data: Unsplash图片数据
    :param save_dir: 保存目录
    :return: 保存路径或None
    """
    _create_save_dir(save_dir)
    
    # 获取图片链接（选择全尺寸）
    image_url = image_data.get("urls", {}).get("full")
    if not image_url:
        image_url = image_data.get("urls", {}).get("regular")
    
    if not image_url:
        print("⚠️ 未找到有效的图片链接")
        return None
    
    # 生成文件名
    image_id = image_data.get("id", "unknown")
    save_path = os.path.join(save_dir, f"unsplash_image_{image_id}.jpg")
    
    # 下载图片
    if _download_media(image_url, save_path):
        return save_path
    return None


def search_youtube_videos(
    api_key: str,
    query: str,
    max_results: int = 5
) -> List[dict]:
    """
    从YouTube搜索视频（仅获取信息，不下载）
    :param api_key: YouTube Data API密钥
    :param query: 搜索关键词
    :param max_results: 最大结果数
    :return: 视频信息列表
    """
    url = "https://www.googleapis.com/youtube/v3/search"
    params = {
        "key": api_key,
        "q": query,
        "part": "snippet",
        "type": "video",
        "maxResults": max_results
    }
    
    try:
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        data = response.json()
        return data.get("items", [])
    except Exception as e:
        print(f"❌ YouTube视频搜索失败：{str(e)}")
        return []


# ------------------- 测试示例 -------------------
if __name__ == "__main__":
    # 1. 替换为你的Pixabay API密钥（从https://pixabay.com/api/docs/获取）
    PIXABAY_API_KEY = "52039769-cde28ab07929ebcb29572fc53"  # 文档示例密钥，建议用自己的

    # 2. 测试下载图片（关键词：黄色花朵，保存到./pixabay_images）
    print("=" * 50)
    print("开始测试下载图片...")
    # image_paths = download_pixabay_images(
    #     api_key=PIXABAY_API_KEY,
    #     q="yellow flowers",  # 搜索关键词
    #     per_page=3,  # 下载3张
    #     image_type="photo"  # 只下载照片
    # )
    # print(f"图片下载完成，成功路径：{image_paths}")

    # 3. 测试下载视频（关键词：海洋波浪，保存到./pixabay_videos）
    print("\n" + "=" * 50)
    print("开始测试下载视频...")
    video_paths = download_pixabay_videos(
        api_key=PIXABAY_API_KEY,
        q="ocean wave",  # 搜索关键词
        per_page=3,  # 下载2个（视频文件较大）
        video_size="small"  # 下载小尺寸（速度快）
    )
    print(f"视频下载完成，成功路径：{video_paths}")