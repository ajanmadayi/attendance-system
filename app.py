from flask import Flask, request, Response
import sqlite3
from datetime import datetime

app = Flask(__name__)

DB_NAME = "attendance.db"


# -------------------------------
# DATABASE INIT
# -------------------------------
def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute('''
    CREATE TABLE IF NOT EXISTS attendance_logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        device_sn TEXT,
        user_id TEXT,
        timestamp TEXT,
        UNIQUE(device_sn, user_id, timestamp)
    )
    ''')

    conn.commit()
    conn.close()


# -------------------------------
# SAVE LOG
# -------------------------------
def save_log(sn, user_id, timestamp):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    try:
        c.execute('''
        INSERT INTO attendance_logs (device_sn, user_id, timestamp)
        VALUES (?, ?, ?)
        ''', (sn, user_id, timestamp))

        conn.commit()
        print(f"✅ Saved: {user_id} at {timestamp}")

    except:
        print("⚠️ Duplicate skipped")

    conn.close()


# -------------------------------
# PARSE ATTLOG DATA
# -------------------------------
def parse_attlog(data):
    logs = []

    lines = data.strip().split("\n")

    for line in lines:
        parts = line.strip().split("\t")

        if len(parts) >= 2:
            user_id = parts[0]
            timestamp = parts[1]
            logs.append((user_id, timestamp))

    return logs


# -------------------------------
# DEVICE ENDPOINT (ADMS)
# -------------------------------
# -------------------------------
# DEVICE ENDPOINT (ADMS)
# -------------------------------
@app.route('/iclock/cdata', methods=['GET', 'POST'])
def iclock():

    print("\n==============================")
    print("📡 DEVICE CONNECTED")

    sn = request.args.get('SN')
    table = request.args.get('table')

    print("Device SN:", sn)
    print("Table:", table)

    # 🔐 ALLOW ONLY YOUR DEVICE
    if sn != "PGG2243500151":
        print("❌ Unauthorized device:", sn)
        return "Unauthorized", 403

    raw_data = request.data.decode('utf-8')
    print("RAW DATA:\n", raw_data)

    if table == "ATTLOG" and raw_data:
        logs = parse_attlog(raw_data)

        for user_id, timestamp in logs:
            save_log(sn, user_id, timestamp)

    return "OK"

# -------------------------------
# DOWNLOAD CSV
# -------------------------------
@app.route('/download_csv')
def download_csv():

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT device_sn, user_id, timestamp 
        FROM attendance_logs 
        ORDER BY timestamp ASC
    """)

    rows = cursor.fetchall()
    conn.close()

    def generate():
        yield "Device SN,User ID,Timestamp\n"
        for row in rows:
            yield ",".join(map(str, row)) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=attendance.csv"}
    )


# -------------------------------
# DOWNLOAD CSV BY DATE
# -------------------------------
@app.route('/download_csv_by_date')
def download_csv_by_date():

    date = request.args.get('date')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT device_sn, user_id, timestamp 
        FROM attendance_logs 
        WHERE date(timestamp) = ?
        ORDER BY timestamp ASC
    """, (date,))

    rows = cursor.fetchall()
    conn.close()

    def generate():
        yield "Device SN,User ID,Timestamp\n"
        for row in rows:
            yield ",".join(map(str, row)) + "\n"

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment; filename=attendance_{date}.csv"}
    )


# -------------------------------
# DASHBOARD (MAIN PAGE)
# -------------------------------
@app.route('/')
def home():
    return """
    <html>
    <head>
        <title>Attendance Dashboard</title>
    </head>
    <body style="text-align:center; padding-top:100px; font-family:Arial;">

        <h1>✅ Attendance Dashboard</h1>

        <a href="/download_csv" style="padding:15px; background:blue; color:white; text-decoration:none;">
            Download Full CSV
        </a>

        <br><br>

        <form action="/download_csv_by_date">
            <input type="date" name="date" required>
            <button type="submit">Download by Date</button>
        </form>

        <br><br>

        <p>System is connected to biometric machine ✅</p>

    </body>
    </html>
    """


# -------------------------------
# TEST ROUTE
# -------------------------------
@app.route('/test')
def test():
    return "✅ Test Route Working"


# -------------------------------
# START SERVER
# -------------------------------
if __name__ == "__main__":
    init_db()
    app.run(host="0.0.0.0", port=10000)