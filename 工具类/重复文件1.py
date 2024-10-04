import os
import shutil
from difflib import SequenceMatcher

# 计算两个字符串的相似度
def get_similarity_ratio(s1, s2):
    return SequenceMatcher(None, s1, s2).ratio()

# 移动重复文件到指定目录，保留最后修改的文件
def move_duplicates(file_groups, destination):
    if not os.path.exists(destination):
        os.makedirs(destination)

    for file_list in file_groups.values():
        if len(file_list) > 1:
            # 按最后修改时间排序文件列表
            file_list.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            original_file = file_list[0]

            # 移动除了最后修改的文件之外的所有文件
            for file_to_move in file_list[1:]:
                file_name = os.path.basename(file_to_move)
                target_path = os.path.join(destination, file_name)

                # 处理文件名冲突
                counter = 1
                while os.path.exists(target_path):
                    base, extension = os.path.splitext(file_name)
                    new_file_name = f"{base}_{counter}{extension}"
                    target_path = os.path.join(destination, new_file_name)
                    counter += 1

                # 移动重复文件
                shutil.move(file_to_move, target_path)

# 查找指定目录下的相同或相似文件名
def find_similar_files(path_to_search, similarity_threshold=0.8):
    file_groups = {}
    for root, dirs, files in os.walk(path_to_search):
        for file in files:
            file_path = os.path.join(root, file)
            file_name = os.path.basename(file_path)

            # 检查文件名是否已经存在于字典中
            found = False
            for existing_file in file_groups.keys():
                if get_similarity_ratio(file_name, existing_file) >= similarity_threshold:
                    file_groups[existing_file].append(file_path)
                    found = True
                    break

            if not found:
                file_groups[file_name] = [file_path]

    return file_groups

# 显示所有重复文件的信息
def display_duplicates(file_groups):
    repeated_files = []
    to_move_files = []

    for file_list in file_groups.values():
        if len(file_list) > 1:
            # 按最后修改时间排序文件列表
            file_list.sort(key=lambda x: os.path.getmtime(x), reverse=True)
            original_file = file_list[0]
            repeated_files.append(original_file)
            to_move_files.extend(file_list[1:])

    # 显示被重复的文件列表
    if repeated_files:
        print("以下为被重复的文件列表：")
        for file_path in repeated_files:
            print(f" - {file_path} (最后修改时间: {datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')})")

    # 显示要移动的文件列表
    if to_move_files:
        print("以下为要移动的文件列表：")
        for file_path in to_move_files:
            print(f" - {file_path} (最后修改时间: {datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')})")

    if not repeated_files and not to_move_files:
        print("没有找到重复文件。")

if __name__ == "__main__":
    path_to_search = input("请输入要搜索的目录路径：")
    if not os.path.isdir(path_to_search):
        print("提供的路径不是一个有效的目录，请重新输入。")
        exit(1)

    destination = os.path.join(path_to_search, "duplicates")
    similarity_threshold = float(input("请输入文件名相似度阈值（0.0 到 1.0 之间，默认为 0.8）：") or 0.8)

    file_groups = find_similar_files(path_to_search, similarity_threshold)

    if file_groups:
        display_duplicates(file_groups)

        if input("是否继续执行并移动重复文件？(y/n): ").lower() == 'y':
            move_duplicates(file_groups, destination)
            print(f"重复文件已从 {path_to_search} 移动到 {destination}")
        else:
            print("操作已取消。")
    else:
        print("没有找到重复文件。")
