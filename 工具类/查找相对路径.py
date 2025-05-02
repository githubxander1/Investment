import os


def find_file_relative_path(current_dir, root_dir, target_dir) -> str:
    """
    通用文件查找方法
    :param relative_path: 相对于项目根目录的路径，如 "common/data/合同.pdf"
    :return: 绝对路径
    """
    # 获取项目根目录（假设脚本在项目子目录中）
    # current_dir = os.path.dirname(os.path.abspath(__file__))
    # print(f'当前文件路径: {current_dir}')
    # root_dir = os.path.abspath(os.path.join(current_dir, "../../.."))  # 根据实际层级调整
    # print(f'项目根目录: {root_dir}')
    # target_dir = 'D:\Xander\Pycharm_gitee\CompanyProject\巴迪克\common\data\合同.pdf'
    # print(f'目标文件路径: {target_file}')

    #'当前文件路径'要查找'目标文件路径'时的相对路径写法：
    relative_path = os.path.relpath(target_dir, current_dir)
    print(f'相对路径: {relative_path}')


    # # 构建完整路径
    # full_path = os.path.join(root_dir, relative_path)
    #
    # if not os.path.exists(full_path):
    #     raise FileNotFoundError(f"文件不存在: {full_path}")

    return relative_path

if __name__ == '__main__':
    # BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    # print(BASE_DIR)
    # target_file = 'D:\Xander\Pycharm_gitee\CompanyProject\巴迪克\common\data\合同.pdf'
    # # print(target_file)
    # DATA_DIR = os.path.join(BASE_DIR, '../../common', 'data')
    # pdf_file_path = os.path.join(DATA_DIR, "合同.pdf")

    current_dir = os.path.dirname(os.path.abspath(__file__))
    print(f'当前文件路径: {current_dir}')
    root_dir = os.path.abspath(os.path.join(current_dir, "../"))  # 根据实际层级调整
    print(f'项目根目录: {root_dir}')
    target_dir = 'D:\Xander\Pycharm_gitee\CompanyProject\巴迪克\common\data\合同.pdf'
    print(f'目标文件路径: {target_dir}')

    find_file_relative_path(current_dir,root_dir,target_dir)