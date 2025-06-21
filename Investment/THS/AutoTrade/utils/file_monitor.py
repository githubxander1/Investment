# utils/file_monitor.py
import os
import hashlib
import logging

logger = logging.getLogger(__name__)

def check_files_modified(file_paths, last_hashes=None, last_mod_times=None):
    current_hashes = {}
    current_mod_times = {}
    modified = False

    for path in file_paths:
        current_mod_times[path] = os.path.getmtime(path)
        current_hash = get_file_hash(path)
        current_hashes[path] = current_hash

        prev_hash = last_hashes.get(path) if last_hashes else None
        prev_time = last_mod_times.get(path) if last_mod_times else None

        # 判断条件1：哈希不同 → 内容变化
        if prev_hash and current_hash != prev_hash:
            modified = True
        # 判断条件2：修改时间不同且哈希相同（可能文件内容没变但时间变了）→ 强制刷新
        elif prev_time and abs(current_mod_times[path] - prev_time) > 1:
            modified = True

    return modified, current_hashes, current_mod_times

def get_file_hash(file_path: str) -> str | None:
    """计算文件内容的MD5哈希值"""
    if not os.path.exists(file_path):
        logger.warning(f"文件不存在: {file_path}")
        return None
    hash_md5 = hashlib.md5()
    with open(file_path, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def check_files_modified_by_hash(file_paths, last_hashes=None) -> tuple[bool, dict]:
    """基于内容哈希检查文件是否被修改"""
    current_hashes = {}
    modified = False

    for file_path in file_paths:
        current_hash = get_file_hash(file_path)
        current_hashes[file_path] = current_hash

        prev_hash = last_hashes.get(file_path)
        if prev_hash is not None and current_hash != prev_hash:
            logger.info(f"[变动] 检测到文件内容变动: {file_path}")
            modified = True

    return modified, current_hashes

# if __name__ == '__main__':
#     file_paths = [Strategy_portfolio_today,Combination_portfolio_today]
#     for file_path in file_paths:
#         get_file_hash(file_path)
#         update_file_status(file_path)
