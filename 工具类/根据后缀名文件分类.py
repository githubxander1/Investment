import os
import shutil

def move_files_by_extension(path):
    # 列出文件名
    file_list = os.listdir(path)

    # 提取后缀名并新建类型文件夹
    for f in file_list:
        try:
            type = f.split('.')[-1]
            folder_path = os.path.join(path, type)
            if not os.path.exists(folder_path):
                os.mkdir(folder_path)

            # 设置每个文件的存储路径和位置
            file_path = os.path.join(path, f)
            print("要移动的文件:", file_path)
            target_path = os.path.join(folder_path, f)
            print("移动的位置:", target_path)

            shutil.move(file_path, target_path)
        except Exception as e:
            print(f"处理文件 {f} 时出现错误: {e}")

# 示例调用
move_files_by_extension(r'C:/Users/Administrator/Downloads')
