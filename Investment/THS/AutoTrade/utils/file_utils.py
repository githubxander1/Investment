# utils/file_utils.py
import os

def ensure_dir_exists(path: str):
    """确保目录存在"""
    os.makedirs(path, exist_ok=True)
