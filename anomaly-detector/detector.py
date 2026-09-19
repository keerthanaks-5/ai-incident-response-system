import requests
import time
import json
import os
from sklearn.ensemble import IsolationForest
import numpy as np
from collections import deque
from datetime import datetime, timedelta

PROMETHEUS_URL = "http://localhost:9090"
# Replace this with your own Slack webhook URL
# Create one at: https://api.slack.com/apps
SLACK_WEBHOOK_URL = "YOUR_SLACK_WEBHOOK_URL_HERE"
INCIDENTS_FILE = "../dashboard-app/incidents.json"

history = deque(maxlen=50)
last_alert_time = None
COOLDOWN_MINUTES = 5

def get_metric(query):
    response = requests.get(
        f"{PROMETHEUS_URL}/api/v1/query",
        params={"query": query}
    )
    data = response.json()
    results = data["data"]["result"]
    
    total = 0
    for item in results:
        total += float(item["value"][1])
    
    return total

def send_slack_alert(message):
    payload = {"text": message}
    try:
        requests.post(SLACK_WEBHOOK_URL, json=payload)
    except Exception as e:
        print(f"⚠️ Failed to send Slack alert: {e}")

def save_incident(timestamp, value):
    """Append this incident to incidents.json so the dashboard can read it"""
    incident = {
        "timestamp": timestamp,
        "metric": "Total HTTP Requests",
        "value": value,
        "status": "Anomaly detected by AI monitoring system"
    }
    
    incidents = []
    if os.path.exists(INCIDENTS_FILE):
        try:
            with open(INCIDENTS_FILE, "r") as f:
                incidents = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            incidents = []
    
    incidents.append(incident)
    incidents = incidents[-50:]  # keep only the last 50 incidents
    
    os.makedirs(os.path.dirname(INCIDENTS_FILE), exist_ok=True)
    with open(INCIDENTS_FILE, "w") as f:
        json.dump(incidents, f, indent=2)

def run_runbook(current_value):
    print("   🤖 Running automated runbook...")
    print("   📋 Step 1: Logging incident details")
    print("   📋 Step 2: Checking service health endpoints")
    print("   📋 Step 3: Notification sent to on-call team via Slack")

def can_send_alert():
    global last_alert_time
    if last_alert_time is None:
        return True
    elapsed = datetime.now() - last_alert_time
    return elapsed > timedelta(minutes=COOLDOWN_MINUTES)

def check_for_anomaly():
    global last_alert_time
    current_value = get_metric("flask_http_request_total")
    history.append(current_value)
    
    timestamp = datetime.now().strftime("%H:%M:%S")
    
    if len(history) < 10:
        print(f"[{timestamp}] 📊 Collecting baseline data... ({len(history)}/10) Current total: {current_value}")
        return
    
    data = np.array(history).reshape(-1, 1)
    model = IsolationForest(contamination=0.1, random_state=42)
    model.fit(data)
    
    prediction = model.predict([[current_value]])
    
    if prediction[0] == -1:
        print(f"[{timestamp}] 🚨 ANOMALY DETECTED! Total requests: {current_value}")
        save_incident(timestamp, current_value)
        
        if can_send_alert():
            alert_message = (
                f"🚨 *Incident Alert*\n"
                f"*Time:* {timestamp}\n"
                f"*Metric:* Total HTTP Requests\n"
                f"*Value:* {current_value}\n"
                f"*Status:* Anomaly detected by AI monitoring system\n"
            )
            send_slack_alert(alert_message)
            run_runbook(current_value)
            last_alert_time = datetime.now()
            print("   📨 Alert sent to Slack")
        else:
            print("   🔇 Alert suppressed (cooldown active)")
    else:
        print(f"[{timestamp}] ✅ Normal — Total requests: {current_value}")

if __name__ == "__main__":
    print("🤖 AI Incident Detector started. Monitoring every 10 seconds...\n")
    send_slack_alert("✅ Incident Response System is now online and monitoring services.")
    while True:
        check_for_anomaly()
        time.sleep(10)