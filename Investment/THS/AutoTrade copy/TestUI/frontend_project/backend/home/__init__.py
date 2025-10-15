from flask import Blueprint, render_template

# 创建home Blueprint
from flask import Blueprint
from .api import home_api_bp

home_bp = Blueprint('home', __name__, template_folder='../../frontend/pages/home')

@home_bp.route('/')
def index():
    return render_template('index.html')

# 暴露api Blueprint
__all__ = ['home_bp', 'home_api_bp']