import os
import hashlib
import shutil
import time

def get_file_md5(filepath):
    """计算文件的MD5值并返回。"""
    hash_md5 = hashlib.md5()
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
    except IOError as e:
        print(f"无法读取文件 {filepath}: {e}")
        return None
    return hash_md5.hexdigest()

def move_duplicates(duplicates, destination):
    """移动重复文件到指定目录，并处理文件名冲突。"""
    if not os.path.exists(destination):
        os.makedirs(destination)
    for file_list in duplicates.values():
        # 根据文件创建时间，保留较旧的文件，移动较新的文件
        file_list.sort(key=lambda x: os.path.getctime(x))
        original_file = file_list[0]
        for duplicate_file in file_list[1:]:
            file_name = os.path.basename(duplicate_file)
            target_path = os.path.join(destination, file_name)
            # 处理文件名冲突
            counter = 1
            while os.path.exists(target_path):
                base, extension = os.path.splitext(file_name)
                new_file_name = f"{base}_{counter}{extension}"
                target_path = os.path.join(destination, new_file_name)
                counter += 1
            # 移动重复文件
            shutil.move(duplicate_file, target_path)
            print(f"Moved '{duplicate_file}' to '{target_path}'")

# 主程序
if __name__ == "__main__":
    directory = input("请输入要搜索的目录路径：")
    if not os.path.isdir(directory):
        print("提供的路径不是一个有效的目录，请重新输入。")
        exit(1)
    destination = os.path.join(directory, "duplicates")
    files_md5 = {}

    # 遍历目录并计算每个文件的MD5
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            file_md5 = get_file_md5(file_path)
            if file_md5:
                if file_md5 in files_md5:
                    # 如果MD5已存在，添加到重复文件列表
                    files_md5[file_md5].append(file_path)
                else:
                    # 否则，创建一个新列表来存储文件路径
                    files_md5[file_md5] = [file_path]

    # 移动重复文件
    duplicates = {k: v for k, v in files_md5.items() if len(v) > 1}
    if duplicates:
        print("以下为重复文件，将被移动到指定目录：")
        move_duplicates(duplicates, destination)
    else:
        print("没有找到重复文件。")
