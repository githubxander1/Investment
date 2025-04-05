import os
import shutil

def move_files_by_extension(path):
    # 遍历目录及其子目录
    for root, dirs, files in os.walk(path):
        for f in files:
            try:
                # 提取后缀名并新建类型文件夹
                file_ext = f.split('.')[-1]
                folder_path = os.path.join(path, file_ext)
                if not os.path.exists(folder_path):
                    os.mkdir(folder_path)

                # 设置每个文件的存储路径和位置
                file_path = os.path.join(root, f)
                print("要移动的文件:", file_path)
                target_path = os.path.join(folder_path, f)
                print("移动的位置:", target_path)

                # 移动文件
                shutil.move(file_path, target_path)
            except Exception as e:
                print(f"处理文件 {f} 时出现错误: {e}")

def move_office_docs_to_folder(path, target_foldler_name='办公文档'):
    #常用办公文档格式
    office_extension = {'txt', 'doc','docx', 'xlsx','xlx', 'xmind', 'md', 'ppt'}

    # 遍历文件目录
    for root, dirs, files in os.walk(path):
        for f in files:
            try:
                # type = f.split('.')[-1]
                if dirs in office_extension:
                    # 创建分类文件夹
                    folder_path = os.path.join(path, dirs)
                    if not os.path.exists(folder_path):
                        os.mkdir(folder_path)

                    # 设置每个文件的存储路径和位置
                    folder_path = os.path.join(root, f)
                    print(f'要移动的文件：{folder_path}')
                    target_path = os.path.join(target_foldler_name, f)
                    print(f'移动位置：{target_foldler_name}')

                    # 移动文件
                    shutil.move(folder_path, target_path)
            except Exception as e:
                print(f'处理文件{f}时异常{e}')

# 示例调用
move_files_by_extension(r'C:\Users\Administrator\Downloads')
# move_office_docs_to_folder(r'C:/Users/Administrator/Downloads/文档')
