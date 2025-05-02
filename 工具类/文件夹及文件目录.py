import os

def list_files(startpath, exclude_list=None):
    """
    递归地列出给定路径下的所有文件和子目录，并排除指定的文件夹及其子文件夹。

    参数:
        startpath (str): 开始遍历的目录路径。
        exclude_list (list): 需要排除的文件夹路径列表。
    """
    if exclude_list is None:
        exclude_list = []

    for root, dirs, files in os.walk(startpath):
        # 排除指定的文件夹及其子文件夹
        dirs[:] = [d for d in dirs if not should_exclude(os.path.join(root, d), exclude_list)]

        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            # 排除指定的文件夹及其子文件夹中的文件
            if should_exclude(os.path.join(root, f), exclude_list):
                continue

            print(f'{subindent}{f}')

def should_exclude(path, exclude_list):
    """ 判断路径是否应该被排除 """
    for exclude_path in exclude_list:
        if path.startswith(exclude_path):
            return True
    return False

# 使用示例
if __name__ == "__main__":
    # 指定要列出的目录路径
    directory_path = r'/CompanyProject/巴迪克'
    # exclude_list = [
    #     r'D:\1document\1test\PycharmProject_gitee\zothers\Projects\schedule\node_modules'
    # ]

    list_files(directory_path)
