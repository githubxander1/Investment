import sqlite3

from flask import Flask, request, jsonify, render_template

app = Flask(__name__)
app.config.from_pyfile('config.py')


def get_db():
    conn = sqlite3.connect(app.config['DATABASE'])
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/api/location', methods=['POST'])
def receive_location():
    data = request.json
    required = ['device_id', 'lat', 'lng', 'timestamp']

    # 数据校验
    if not all(k in data for k in required):
        return jsonify({"error": "缺少必要参数"}), 400

    try:
        lat = float(data['lat'])
        lng = float(data['lng'])
        if not (-90 <= lat <= 90) or not (-180 <= lng <= 180):
            raise ValueError
    except:
        return jsonify({"error": "坐标值不合法"}), 400

    # 存储到数据库
    conn = get_db()
    try:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS locations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id TEXT,
                lat REAL,
                lng REAL,
                timestamp INTEGER
            )
        ''')

        conn.execute('''
            INSERT INTO locations 
            (device_id, lat, lng, timestamp)
            VALUES (?, ?, ?, ?)
        ''', (data['device_id'], lat, lng, data['timestamp']))

        conn.commit()
        return jsonify({"status": "success"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@app.route('/map/<device_id>')
def show_map(device_id):
    return render_template('map.html',
                           ak=app.config['BAIDU_MAP_AK'],
                           device_id=device_id
                           )


@app.route('/api/points/<device_id>')
def get_points(device_id):
    conn = get_db()
    points = conn.execute('''
        SELECT lat, lng, timestamp 
        FROM locations 
        WHERE device_id = ?
        ORDER BY timestamp
    ''', (device_id,)).fetchall()

    return jsonify([dict(p) for p in points])

@app.route('/api/secure_location', methods=['POST'])
def secure_receive():
    encrypted = request.data
    cipher = Fernet(app.config['SECRET_KEY'])
    try:
        data = json.loads(cipher.decrypt(encrypted))
        # ...处理数据...
    except:
        return jsonify({"error": "解密失败"}), 400

#历史轨迹
@app.route('/history/<device_id>')
def show_history(device_id):
    conn = get_db()
    points = conn.execute('''
        SELECT strftime('%Y-%m-%d %H:%M', datetime(timestamp, 'unixepoch')) as time,
               lat, lng 
        FROM locations 
        WHERE device_id = ?
    ''', (device_id,)).fetchall()

    return render_template('history.html',
                           points=points,
                           device_id=device_id
                           )
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)