import os

def list_files(startpath):
    """
    递归地列出给定路径下的所有文件和子目录。

    参数:
        startpath (str): 开始遍历的目录路径。
    """
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * (level)
        print(f'{indent}{os.path.basename(root)}/')
        subindent = ' ' * 4 * (level + 1)
        for f in files:
            print(f'{subindent}{f}')

# 使用示例
if __name__ == "__main__":
    # 指定要列出的目录路径
    directory_path = r'D:\1test\PycharmProject_gitee\others\项目实战\schedule'
    list_files(directory_path)
