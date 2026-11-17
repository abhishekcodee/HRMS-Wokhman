"""
Standalone Biometric Attendance Sync Agent for Self-Hosted Frappe HRMS.

Run this script on your local office network or biometric server (e.g. ZKTeco, eSSL, Realtime).
Pushes employee punch logs directly to your independent HRMS instance without third-party services.
"""

import sys
import time
import requests
from datetime import datetime

# ================= CONFIGURATION =================
HRMS_BASE_URL = "http://localhost"  # Or your internal URL: https://hrms.yourcompany.local
API_KEY = "YOUR_FRAPPE_API_KEY"      # Generate from User > API Access in Frappe Desk
API_SECRET = "YOUR_FRAPPE_API_SECRET"
SYNC_INTERVAL_SECONDS = 60
# =================================================

HEADERS = {
    "Authorization": f"token {API_KEY}:{API_SECRET}",
    "Content-Type": "application/json",
    "Accept": "application/json",
}

def push_checkin(employee_id: str, timestamp: datetime, log_type: str = "IN", device_id: str = "BIOMETRIC_01"):
    """
    Submits an Employee Checkin record to self-hosted HRMS.
    """
    url = f"{HRMS_BASE_URL}/api/resource/Employee Checkin"
    payload = {
        "employee": employee_id,
        "time": timestamp.strftime("%Y-%m-%d %H:%M:%S"),
        "log_type": log_type,  # "IN" or "OUT"
        "device_id": device_id,
    }

    try:
        response = requests.post(url, headers=HEADERS, json=payload, timeout=10)
        if response.status_code in (200, 201):
            print(f"[{datetime.now()}] [SUCCESS] Logged {log_type} for Employee {employee_id} at {payload['time']}")
            return True
        elif response.status_code == 409:
            print(f"[{datetime.now()}] [INFO] Duplicate log ignored for {employee_id} at {payload['time']}")
            return True
        else:
            print(f"[{datetime.now()}] [ERROR] HTTP {response.status_code}: {response.text}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"[{datetime.now()}] [CONNECTION ERROR] Failed to connect to HRMS: {e}")
        return False

def sample_sync_loop():
    print(f"Starting Biometric Sync Daemon connecting to {HRMS_BASE_URL}...")
    # Replace this simulation with reading from your biometric SDK (e.g. pyzk, zk, or local SQL database)
    while True:
        # Example test check-in:
        # push_checkin(employee_id="HR-EMP-00001", timestamp=datetime.now(), log_type="IN", device_id="DOOR_GATE_1")
        time.sleep(SYNC_INTERVAL_SECONDS)

if __name__ == "__main__":
    sample_sync_loop()
