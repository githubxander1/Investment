from flask import Blueprint, render_template

# 创建admin Blueprint
from flask import Blueprint
from .api import admin_api_bp
import os

# 获取当前文件目录
current_dir = os.path.dirname(os.path.abspath(__file__))
# 设置静态文件夹路径
static_folder = os.path.join(current_dir, '../../frontend')

admin_bp = Blueprint('admin', __name__, template_folder='../../frontend/pages/admin', static_folder=static_folder, static_url_path='/frontend')

@admin_bp.route('/admin')
def admin():
    return render_template('admin.html')

# 暴露api Blueprint
__all__ = ['admin_bp', 'admin_api_bp']