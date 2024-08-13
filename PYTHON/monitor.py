import socket
import smtplib
from email.mime.text import MIMEText
from datetime import datetime
import sqlite3
import time

# Configuration
SERVICES_TO_MONITOR = [
    {'host': '127.0.0.1', 'port': 80, 'name': 'HTTP Service'},
    {'host': '127.0.0.1', 'port': 22, 'name': 'SSH Service'}
]

CHECK_INTERVAL = 60  # seconds
ALERT_EMAIL = 'admin@example.com'
SMTP_SERVER = 'smtp.example.com'
SMTP_PORT = 587
SMTP_USERNAME = 'your_email@example.com'
SMTP_PASSWORD = 'your_password'

# Database Setup
conn = sqlite3.connect('monitoring.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS logs 
                  (service_name TEXT, status TEXT, timestamp DATETIME)''')
conn.commit()

def send_email_alert(service_name):
    msg = MIMEText(f'Service {service_name} is down.')
    msg['Subject'] = f'Alert: {service_name} Down'
    msg['From'] = SMTP_USERNAME
    msg['To'] = ALERT_EMAIL
    
    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
        server.starttls()
        server.login(SMTP_USERNAME, SMTP_PASSWORD)
        server.sendmail(SMTP_USERNAME, ALERT_EMAIL, msg.as_string())

def log_status(service_name, status):
    timestamp = datetime.now()
    cursor.execute('INSERT INTO logs (service_name, status, timestamp) VALUES (?, ?, ?)',
                   (service_name, status, timestamp))
    conn.commit()

def check_service(host, port, service_name):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.settimeout(5)
        try:
            s.connect((host, port))
            log_status(service_name, 'UP')
            return True
        except (socket.timeout, socket.error):
            log_status(service_name, 'DOWN')
            send_email_alert(service_name)
            return False

def monitor_services():
    while True:
        for service in SERVICES_TO_MONITOR:
            service_name = service['name']
            host = service['host']
            port = service['port']
            print(f'Checking {service_name}...')
            check_service(host, port, service_name)
        time.sleep(CHECK_INTERVAL)

if __name__ == '__main__':
    monitor_services()
