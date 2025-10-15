import os
from flask import Flask
from home import home_bp, home_api_bp

# 创建Flask应用
app = Flask(__name__)

# 配置静态文件目录
app.static_folder = os.path.join(os.path.dirname(__file__), '../frontend')
app.static_url_path = '/frontend'

# 注册Blueprint
app.register_blueprint(home_bp)
app.register_blueprint(home_api_bp)

# 配置数据库路径 - 使用admin_project的数据库
app.config['DATABASE'] = os.path.join(os.path.dirname(__file__), '../../admin_project/backend/data/items.db')

if __name__ == '__main__':
    # 打印完整数据库路径以便调试
    print(f"数据库路径: {app.config['DATABASE']}")
    # 检查数据库文件是否存在
    if not os.path.exists(app.config['DATABASE']):
        print(f"警告: 数据库文件不存在: {app.config['DATABASE']}")
        print("请确保admin_project/backend/data目录下存在items.db文件，不要新建数据库")
    # 运行应用
    app.run(debug=True, port=5000)