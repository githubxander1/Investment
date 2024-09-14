from flask import Flask, request, send_from_directory, render_template, jsonify, url_for
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)

# 设置上传文件夹
app.config['UPLOAD_FOLDER'] = 'uploads'

# 确保上传文件夹存在
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])
def human_readable_size(size):
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} PB"
# 处理默认路由
@app.route('/')#定义默认路由。
def index():
    return render_template('index1.html')#使用 render_template 渲染 index.html 页面

# 处理上传文件
@app.route('/upload_file', methods=['POST'])
def upload_file():
    file = request.files.get('file')#使用 request.files.get('file') 获取上传的文件。
    if file:
        filename = secure_filename(file.filename)#使用 secure_filename 确保文件名安全
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        return jsonify({'success': True, 'filename': filename})
    else:
        return jsonify({'success': False, 'message': 'No file part'})

# 处理上传文本
@app.route('/upload_text', methods=['POST'])
def upload_text():
    text = request.form.get('text')#获取上传的文本
    # text = request.form['text']#获取上传的文本
    if text:
        filename = "uploaded_text_{}.txt".format(len(os.listdir(app.config['UPLOAD_FOLDER'])) + 1)#使用当前上传文件夹中的文件数量生成唯一的文件名
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        with open(file_path, 'w') as f:
            f.write(text)
        return jsonify({'success': True,'content': text})
    else:
        return jsonify({'success': False, 'message': 'No text provided'})

# 获取已上传文件列表
@app.route('/get_files')
def get_files():
    files = []
    for filename in sorted(os.listdir(app.config['UPLOAD_FOLDER']), reverse=True):#按文件名降序排序
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file_info = {  #将文件名、大小和上传时间添加到文件列表中
            'name': filename,
            'size': os.path.getsize(file_path),
            # 'size': human_readable_size(os.path.getsize(file_path)),  # 显示更友好的文件大小
            'type': 'text/plain' if filename.endswith('.txt') else 'other',
            'upload_time': datetime.fromtimestamp(os.path.getmtime(file_path)).strftime('%Y-%m-%d %H:%M:%S')
        }
        if file_info['type'] == 'text/plain':
            with open(file_path, 'r') as f:
                file_info['content'] = f.read()
        files.append(file_info)
    return jsonify(files)

# 展示已上传文件
@app.route('/uploads/<filename>')#定义动态路由
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)#发送指定文件

# 删除文件
@app.route('/delete/<filename>', methods=['DELETE'])
def delete_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        os.remove(file_path)
        return jsonify({'success': True})
    else:
        return jsonify({'success': False, 'message': 'File not found'})

# 处理 favicon 请求
@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'), 'favicon.ico', mimetype='image/vnd.microsoft.icon')
    #os.path.join(app.root_path, 'static'): 构建了静态文件目录的绝对路径。
    # app.root_path指向Flask应用的根目录，与之拼接上'static'就得到了存放静态资源（如CSS、JavaScript、图片等）的目录。
    # 'favicon.ico': 指定要发送的文件名，即favicon图标文件。
    # mimetype='image/vnd.microsoft.icon': 设置响应的内容类型为ICO图像的MIME类型，确保浏览器能正确识别并处理这个响应。
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)


    # 辅助函数：将文件大小转换为更友好的格式
