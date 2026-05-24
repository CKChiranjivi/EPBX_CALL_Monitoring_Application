from flask import Flask, render_template
from flask_socketio import SocketIO
import mysql.connector
import time
import threading
from flask import request, jsonify

app = Flask(__name__)
socketio = SocketIO(
    app,
    cors_allowed_origins="*",
    async_mode="threading"
)

# ================= FILTER API =================

@app.route("/analytics")
def analytics():

    from_date = request.args.get("from")
    to_date = request.args.get("to")
    ext = request.args.get("ext")
    phone = request.args.get("phone")
    call_type = request.args.get("type")

    try:

        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="Amneal@123",
            database="epbx_logs"
        )

        cursor = db.cursor(dictionary=True)

        query = "SELECT * FROM call_logs WHERE 1=1"

        params = []

        # FROM DATE
        if from_date:
            query += " AND call_date >= %s"
            params.append(from_date)

        # TO DATE
        if to_date:
            query += " AND call_date <= %s"
            params.append(to_date)

        # EXTENSION
        if ext:
            query += " AND extension = %s"
            params.append(ext)

        # PHONE
        if phone:
            query += " AND phone_number LIKE %s"
            params.append(f"%{phone}%")

        # TYPE
        if call_type:
            query += " AND call_type = %s"
            params.append(call_type)

        # ORDER
        query += " ORDER BY id DESC"

        cursor.execute(query, params)

        rows = cursor.fetchall()

        # CONVERT DATE/TIME
        for row in rows:

            row["call_date"] = (
                str(row["call_date"])
                if row["call_date"] else ""
            )

            row["call_time"] = (
                str(row["call_time"])
                if row["call_time"] else ""
            )

            row["created_at"] = (
                str(row["created_at"])
                if row["created_at"] else ""
            )

        cursor.close()
        db.close()

        return jsonify(rows)

    except Exception as e:

        return jsonify({
            "error": str(e)
        })

@app.route("/")
def index():
    return render_template("dashboard.html")


def send_calls():

    last_id = 0

    while True:
        try:
            db = mysql.connector.connect(
                host="localhost",
                user="root",
                password="Amneal@123",
                database="epbx_logs"
            )

            cursor = db.cursor(dictionary=True)

            cursor.execute(
                "SELECT * FROM call_logs WHERE id > %s ORDER BY id ASC",
                (last_id,)
            )

            rows = cursor.fetchall()

            for row in rows:

                # convert date/time objects to string
                row["call_date"] = str(row["call_date"]) if row["call_date"] else ""
                row["call_time"] = str(row["call_time"]) if row["call_time"] else ""
                row["created_at"] = str(row["created_at"]) if row["created_at"] else ""

                print("Sending:", row)

                socketio.emit("call_event", row)

                last_id = row["id"]

            cursor.close()
            db.close()

        except Exception as e:
            print("Error:", e)

        time.sleep(2)


# start background thread
thread = threading.Thread(target=send_calls)
thread.daemon = True
thread.start()


if __name__ == "__main__":
    socketio.run(app, host="0.0.0.0", port=5000, debug=True)