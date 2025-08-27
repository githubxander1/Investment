# 简单Python前后端项目（带数据库）

这个项目是一个非常简单的前后端示例，用于学习目的。后端使用Python Flask框架，前端使用HTML、CSS和JavaScript，并添加了SQLite数据库支持。

## 功能
- 查看项目列表
- 添加新项目
- 删除项目
- 数据持久化存储（使用SQLite数据库）

## 项目结构
```
TestUI/
├── backend/
│   ├── app.py       # Flask后端代码
│   └── items.db     # SQLite数据库文件（运行后自动创建）
├── frontend/
│   ├── index.html   # 前端HTML页面
│   ├── style.css    # 前端CSS样式
│   └── app.js       # 前端JavaScript代码
├── README.md        # 项目说明
└── requirements.txt # Python依赖包
```

## 运行步骤

1. 安装依赖
```bash
pip install -r requirements.txt
```

2. 启动后端服务器
```bash
cd backend
python app.py
```
   - 首次运行时会自动创建数据库文件并插入测试数据

3. 打开浏览器，访问 http://localhost:5000

## 技术栈
- 后端: Python, Flask, SQLite
- 前端: HTML, CSS, JavaScript

## 学习目标
- 了解前后端分离的基本概念
- 学习使用Flask创建RESTful API
- 学习前端如何与后端API交互
- 学习如何在Flask中使用SQLite数据库
- 了解基本的数据库操作（创建表、插入、查询、删除）

## 扩展建议
- 添加数据更新功能
- 实现用户认证
- 尝试使用其他数据库（如MySQL或PostgreSQL）
- 添加更多的前端交互效果