from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime, timedelta
import sqlite3

app = Flask(__name__)

# 连接数据库
def get_db_connection():
    conn = sqlite3.connect('database.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/calendar_events')
def calendar_events():
    conn = get_db_connection()
    today = datetime.now().strftime('%Y-%m-%d')
    events = conn.execute('SELECT * FROM schedules WHERE date BETWEEN ? AND ?',
                          (f'{int(datetime.now().year)}-01-01', f'{int(datetime.now().year)}-12-31')).fetchall()
    conn.close()
    # 将查询结果转换为 FullCalendar 可识别的格式
    events_list = [{'title': event['title'], 'start': event['date'] + 'T' + event['time']} for event in events]
    return jsonify(events_list)

# 获取所有日程
def get_schedules():
    conn = get_db_connection()
    schedules = conn.execute('SELECT * FROM schedules ORDER BY date DESC, time DESC').fetchall()
    conn.close()
    return schedules

# 获取指定日程
def get_schedule(schedule_id):
    conn = get_db_connection()
    schedule = conn.execute('SELECT * FROM schedules WHERE id = ?', (schedule_id,)).fetchone()
    conn.close()
    return schedule

# 更新日程
def update_schedule(schedule_id, title, date, time, content):
    conn = get_db_connection()
    conn.execute('UPDATE schedules SET title = ?, date = ?, time = ?, content = ? WHERE id = ?',
                 (title, date, time, content, schedule_id))
    conn.commit()
    conn.close()

# @app.route("/edit_schedule/<int:schedule_id>")
def edit_schedule(schedule_id):
    schedule = get_schedule(schedule_id)
    if schedule is None:
        return render_template("edit_schedule.html", schedule=None)
    return render_template("edit_schedule.html", schedule=schedule)

# @app.route("/edit_schedule", methods=["POST"])
def submit_edit_schedule():
    schedule_id = request.form["schedule_id"]
    title = request.form["title"]
    date = request.form["date"]
    time = request.form["time"]
    content = request.form["content"]
    update_schedule(schedule_id, title, date, time, content)
    return redirect(url_for("index"))

# 添加日程
def add_schedule(title, date, time, content):
    conn = get_db_connection()
    conn.execute('INSERT INTO schedules (title, date, time, content) VALUES (?, ?, ?, ?)',
                 (title, date, time, content))
    conn.commit()
    conn.close()

# 删除日程
def delete_schedule(schedule_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM schedules WHERE id = ?', (schedule_id,))
    conn.commit()
    conn.close()

# @app.route("/add_schedule", methods=["POST"])
def add_schedule():
    if request.method == "POST":
        title = request.form["title"]
        date = request.form["date"]
        time = request.form["time"]
        content = request.form["content"]
        add_schedule(title, date, time, content)
        return redirect(url_for("index"))
    else:
        return redirect(url_for("index"))

# @app.route("/delete_schedule/<int:schedule_id>")
def delete_schedule(schedule_id):
    delete_schedule(schedule_id)
    return redirect(url_for("index"))

# @app.route("/search", methods=["POST"])
def search():
    keyword = request.form["keyword"]
    conn = get_db_connection()
    schedules = conn.execute('SELECT * FROM schedules WHERE title LIKE ? OR content LIKE ? ORDER BY date DESC, time DESC',
                             ('%' + keyword + '%', '%' + keyword + '%')).fetchall()
    conn.close()
    return render_template("search.html", schedules=schedules)

# @app.route("/stats")
def stats():
    schedules = get_schedules()
    tags = {}
    for schedule in schedules:
        content = schedule["content"]
        for tag in content.split():
            if tag.startswith("#"):
                tag = tag.strip("#")
                tags[tag] = tags.get(tag, 0) + 1
    return render_template("stats.html", schedules=schedules, tags=tags)

# @app.route("/")
def index():
    today = datetime.now().date()
    schedules = get_schedules()
    return render_template("index.html", today=today, schedules=schedules)

if __name__ == "__main__":
    # 创建数据库和表
    conn = get_db_connection()
    conn.execute('''CREATE TABLE IF NOT EXISTS schedules (
                      id INTEGER PRIMARY KEY AUTOINCREMENT,
                      title TEXT NOT NULL,
                      date TEXT NOT NULL,
                      time TEXT NOT NULL,
                      content TEXT NOT NULL)''')
    conn.commit()
    conn.close()
    app.run(debug=True)
