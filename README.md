# :telephone_receiver: EPBX Call Monitoring & Analytics Dashboard

A professional real-time EPBX Call Monitoring & Analytics Dashboard developed using Python, Flask, Flask-SocketIO, MySQL, HTML, CSS, and JavaScript.

This project was developed to simplify EPBX call monitoring, troubleshooting, analytics, and reporting inside enterprise environments. Instead of manually checking server logs and SMDR records, this dashboard provides a centralized real-time monitoring platform for IT administrators and support teams.

---

# :rocket: Project Overview

The system connects directly with the EPBX server through socket communication, captures SMDR (Station Message Detail Recording) logs, stores them in MySQL, and displays them in a professional live dashboard.

The application supports:
- Real-time live call monitoring
- Search and filters
- CSV/PDF report generation
- Dark/Light mode
- Real-time Socket.IO updates
- Enterprise dashboard UI

---

# :sparkles: Features

## :satellite: Real-Time Live Monitoring

- Displays live EPBX call activities instantly
- Real-time updates using Flask-SocketIO
- Automatically refreshes without page reload
- Shows latest 200 live call records

---

## :telephone: Call Information Tracking

Dashboard displays:
- Call ID
- Date
- Time
- Extension Number
- Call Type (`I`, `O`, `Ext`)
- Phone Number
- Call Duration

---

## :mag: Smart Filters & Search

Filter records using:
- Date Range
- Extension Number
- Phone Number
- Call Type

---

## :page_facing_up: Professional Report Generation

### :file_folder: CSV Export
- Export filtered call records to CSV

### :page_with_curl: PDF Report Generation
- Company logo support
- Company branding
- Generated date/time
- Serial number (S/N)
- Professional enterprise report format

---

## :art: Interactive Dashboard UI

- Responsive design
- Professional monitoring interface
- Dark / Light mode
- Real-time animations
- Enterprise-style layout

---

## :gear: Backend Automation

- Automatic EPBX socket connection
- Automatic SMDR parsing
- Automatic database insertion
- Background monitoring service

---

# :hammer_and_wrench: Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend Logic |
| Flask | Web Framework |
| Flask-SocketIO | Real-Time Communication |
| MySQL | Database |
| HTML | Frontend Structure |
| CSS | Styling |
| JavaScript | Frontend Logic |
| jsPDF | PDF Generation |
| AutoTable | PDF Table Formatting |

---

# :open_file_folder: Project Structure

```text
project/
¦
+-- run.py
+-- dashboard_server.py
¦
+-- templates/
¦   +-- dashboard.html
¦
+-- static/
¦   +-- style.css
¦   +-- script.js
¦   +-- logo.png
¦
+-- README.md
---

# :floppy_disk: Database Structure

Database Name:

```sql
epbx_logs
```

Table Name:

```sql
call_logs
```

---

## :clipboard: Table Structure

| Column Name    | Data Type   | Description                |
| -------------- | ----------- | -------------------------- |
| id             | INT         | Auto Increment Primary Key |
| call_date      | DATE        | Call Date                  |
| call_time      | TIME        | Call Time                  |
| extension      | VARCHAR(10) | Extension Number           |
| line_no        | VARCHAR(10) | EPBX Line Number           |
| call_type      | VARCHAR(10) | I / O / EXT                |
| phone_number   | VARCHAR(25) | Phone Number               |
| ring_time      | VARCHAR(10) | Ring Time                  |
| duration       | VARCHAR(10) | Call Duration              |
| trunk          | VARCHAR(10) | Trunk Information          |
| created_at     | TIMESTAMP   | Record Timestamp           |
| call_direction | VARCHAR(10) | Call Direction             |

---

# :building_construction: SQL Table Creation Script

```sql
CREATE TABLE call_logs (

    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,

    call_date DATE,

    call_time TIME,

    extension VARCHAR(10),

    line_no VARCHAR(10),

    call_type VARCHAR(10),

    phone_number VARCHAR(25),

    ring_time VARCHAR(10),

    duration VARCHAR(10),

    trunk VARCHAR(10),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    call_direction VARCHAR(10)

);
```

---

# :computer: Installation & Setup

## 1 Clone Repository

```bash
git clone https://github.com/your-username/epbx-call-dashboard.git
```

---

## 2 Install Required Libraries

```bash
pip install flask
pip install flask-socketio
pip install mysql-connector-python
```

---

## 3 Configure MySQL Credentials

Update MySQL configuration in:

* `run.py`
* `dashboard_server.py`

```python
host="localhost",
user="root",
password="YOUR_PASSWORD",
database="epbx_logs"
```

---

## 4 Configure EPBX Details

Inside `run.py`

```python
HOST = "YOUR_EPBX_IP"
PORT = 2300

USER = "USERNAME"
PASSWORD = "PASSWORD"
```

---

## 5 Run Application

```bash
python run.py
```

---

# :globe_with_meridians: Open Dashboard

Open browser:

```text
http://localhost:5000
```

---

# :bar_chart: Dashboard Functionalities

:white_check_mark: Real-time call monitoring
:white_check_mark: Live dashboard updates
:white_check_mark: Search & filters
:white_check_mark: CSV export
:white_check_mark: Professional PDF reports
:white_check_mark: Dark/Light mode
:white_check_mark: Responsive dashboard
:white_check_mark: Last 200 live calls display

---

# :chart_with_upwards_trend: Future Scope

Planned future enhancements:

* User Authentication
* Role-Based Access Control
* Graphical Analytics Dashboard
* Missed Call Analysis
* Department-wise Reports
* Email Alert System
* Multi-site EPBX Monitoring
* Cloud Deployment
* AI-based Call Analytics
* Call Recording Integration
* REST API Integration
* Call Traffic Visualization

---

# :moneybag: Benefits to Organization

This application helps organizations by:

:white_check_mark: Reducing manual call log monitoring effort
:white_check_mark: Improving troubleshooting speed
:white_check_mark: Reducing operational downtime
:white_check_mark: Increasing IT support efficiency
:white_check_mark: Centralizing monitoring operations
:white_check_mark: Automating report generation
:white_check_mark: Reducing repetitive administrative tasks
:white_check_mark: Saving operational and support costs

---

# :man_technologist: Developed By

**Mr. C.K. Chiranjivi**

© 2026 All Rights Reserved.

```
```
