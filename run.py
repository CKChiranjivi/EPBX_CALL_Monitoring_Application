import socket
import mysql.connector
from datetime import datetime
import subprocess
import sys
import os

# ================= START DASHBOARD SERVER =================

base_dir = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))

dashboard_script = os.path.join(base_dir, "dashboard_server.py")

subprocess.Popen(
    [sys.executable, dashboard_script],
    creationflags=subprocess.CREATE_NO_WINDOW
)

# ================= SOCKET CONFIG =================

HOST = "10.0.32.11"
PORT = 2300

USER = "smdr"
PASSWORD = "pccsmdr"

# ================= MYSQL =================

db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Amneal@123",
    database="epbx_logs"
)

cursor = db.cursor()

# ================= SOCKET =================

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((HOST, PORT))

print("Connected to EPBX")

stage = 0

while True:

    data = sock.recv(4096)

    if not data:
        continue

    text = data.decode(errors="ignore")

    for line in text.splitlines():

        line = line.strip()

        if not line:
            continue

        print("SERVER:", line)

        # ================= LOGIN =================

        if stage == 0:
            sock.send(b"smdr\r\n")
            stage = 1
            continue

        elif stage == 1:
            sock.send((USER + "\r\n").encode())
            stage = 2
            continue

        elif stage == 2:
            sock.send((PASSWORD + "\r\n").encode())
            stage = 3
            continue

        # ================= CALL DATA =================

        else:

            try:

                # Skip junk lines
                if line.startswith("-") or "SMDR" in line:
                    continue

                parts = line.split()

                # ================= INCOMING =================

                if len(parts) >= 8 and "<" in parts[4]:

                    call_date = datetime.strptime(parts[0], "%d/%m/%y").date()
                    call_time = datetime.strptime(parts[1], "%I:%M%p").time()

                    extension = parts[2]
                    line_no = parts[3]

                    call_type = parts[4][1]
                    phone_number = parts[4][3:]

                    ring_time = parts[5]
                    duration = parts[6]
                    trunk = parts[7]

                # ================= OUTGOING =================

                elif len(parts) >= 5 and parts[3].isdigit() and "<" not in line:

                    call_date = datetime.strptime(parts[0], "%d/%m/%y").date()
                    call_time = datetime.strptime(parts[1], "%I:%M%p").time()

                    extension = parts[2]
                    line_no = parts[3]

                    call_type = "O"
                    phone_number = ''.join(filter(str.isdigit, parts[4]))

                    ring_time = None

                    if len(parts) >= 6:
                        duration = parts[-1]
                    else:
                        duration = None

                    trunk = None

                # ================= INTERNAL =================

                elif "EXT" in line:

                    call_date = datetime.strptime(parts[0], "%d/%m/%y").date()
                    call_time = datetime.strptime(parts[1], "%I:%M%p").time()

                    extension = parts[2]
                    line_no = None
                    call_type = "EXT"

                    phone_number = parts[3].replace("EXT", "")

                    ring_time = None
                    duration = None
                    trunk = None

                else:
                    continue

                # ================= INSERT =================

                sql = """
                INSERT INTO call_logs
                (call_date, call_time, extension, line_no, call_type, phone_number, ring_time, duration, trunk)
                VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
                """

                val = (
                    call_date,
                    call_time,
                    extension,
                    line_no,
                    call_type,
                    phone_number,
                    ring_time,
                    duration,
                    trunk
                )

                cursor.execute(sql, val)
                db.commit()

                print("Saved:", call_type, phone_number)

            except Exception as e:
                print("Parse/DB Error:", e)