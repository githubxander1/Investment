import os
from flask import Flask, request, jsonify, session, make_response, render_template
import hashlib

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', 'default_secret_key')

# 用户信息
userinfo = {
    '1001': ['张三', '123'],
    '1002': ['张三', '1235'],
    '1003': ['张三', '1234']
}

# 对密码进行哈希处理
for key in userinfo:
    userinfo[key][1] = hashlib.sha256(userinfo[key][1].encode()).hexdigest()

# 获取 cookie 值的辅助函数
def get_cookie_value(cookie_name):
    return request.cookies.get(cookie_name)

# 主页
@app.route('/')
def home():
    username = get_cookie_value('cookie_name')
    logged_in = username is not None
    return render_template('index.html', logged_in=logged_in, username=username)

# 登录页面
@app.route('/login')
def login_page():
    response = request.args.get('response', '{}')
    return render_template('login.html', response=response)

# 注册页面
@app.route('/register')
def register_page():
    response = request.args.get('response', '{}')
    return render_template('register.html', response=response)


# 动态路由
@app.route('/students/<string:stno>', methods=['GET'])
def get_student_info(stno):
    if stno in userinfo:
        return jsonify({stno: userinfo.get(stno)})
    else:
        return jsonify(f'{stno}不存在')

# 获取用户信息
@app.route('/getuser', methods=['GET'])
def getuser():
    try:
        name = get_cookie_value('cookie_name')
        if name is not None:
            id = request.args.get('id')
            if id is None:
                return jsonify({'code': 1000, 'msg': 'must be required'})
            elif not id.isdigit():
                return jsonify({'code': 1001, 'msg': 'must be a number'})
            else:
                return jsonify({'code': 200, 'msg': 'user is logged in'})
        else:
            return jsonify({'code': 1002, 'msg': 'please login first'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)})

# 登录
@app.route('/user/login', methods=['POST'])
def login():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return jsonify({'code': 1001, 'msg': 'parameter error'})

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if username in userinfo and userinfo[username][1] == hashed_password:
            mr = make_response(render_template('index.html', logged_in=True, username=username))
            mr.set_cookie(key='cookie_name', value=username, max_age=5)
            return mr
        else:
            return jsonify({'code': 1002, 'msg': 'account or password error'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)})

# 注册
@app.route('/user/register', methods=['POST'])
def register():
    try:
        username = request.form.get('username')
        password = request.form.get('password')
        if not username or not password:
            return jsonify({'code': 1001, 'msg': 'parameter error'})

        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        if username not in userinfo:
            userinfo[username] = [username, hashed_password]
            return jsonify({'code': 200, 'msg': 'registration success'})
        else:
            return jsonify({'code': 1003, 'msg': 'username already exists'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)})

# 注销
@app.route('/user/logout', methods=['GET'])
def logout():
    try:
        name = get_cookie_value('cookie_name')
        if name is not None:
            mr = make_response(render_template('index.html', logged_in=False, username=None))
            mr.delete_cookie('cookie_name')
            return mr
        else:
            return jsonify({'code': 1002, 'msg': 'not logged in'})
    except Exception as e:
        return jsonify({'code': 500, 'msg': str(e)})

# 列表页面
@app.route('/list', methods=['GET'])
def list_students():
    username = get_cookie_value('cookie_name')
    logged_in = username is not None
    students = [(key, userinfo[key]) for key in userinfo]
    return render_template('list.html', students=students, logged_in=logged_in, username=username)

# 处理 404 错误
@app.errorhandler(404)
def page_not_found(error):
    return jsonify({'code': 404, 'msg': 'Not Found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
