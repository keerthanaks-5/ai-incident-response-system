# 🏥 AI-Powered Incident Response System

[![Python](https://img.shields.io/badge/Python-3.11-blue)](https://python.org)
[![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED)](https://docker.com)
[![Prometheus](https://img.shields.io/badge/Monitoring-Prometheus-E6522C)](https://prometheus.io)
[![Grafana](https://img.shields.io/badge/Dashboard-Grafana-F46800)](https://grafana.com)
[![Slack](https://img.shields.io/badge/Alerts-Slack-4A154B)](https://slack.com)

An end-to-end **DevOps + AI** project that monitors live microservices,
detects anomalies using machine learning, and automatically alerts the
team via Slack — without any manually defined threshold rules.

> Built as a Final Year MCA Capstone Project

---

## 📌 What This Project Does

Traditional monitoring systems require engineers to manually write rules
like "alert if error rate exceeds 10%". This system replaces that with
an **AI model that learns what normal looks like** and automatically
flags anything unusual — even failure types nobody anticipated.

When an anomaly is detected, the system automatically:
- 🚨 Sends a formatted alert to Slack
- 📋 Logs the incident to a persistent JSON store
- 🤖 Executes an automated runbook
- 📊 Updates the live web dashboard

---

## 🏗️ System Architecture

Microservices (Flask)
↓ expose /metrics
Prometheus → scrapes every 15 seconds
↓
├──→ Grafana → live graphs
│
└──→ AI Detector (Isolation Forest)
↓ anomaly detected
├──→ Save to incidents.json
├──→ Send Slack alert
└──→ Execute runbook
↓
Custom Web Dashboard
(login + health + incidents + Grafana)


---

## 🛠️ Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| Application | Python 3.11 + Flask | Microservices and web dashboard |
| Containerization | Docker + Docker Compose | Package and orchestrate all components |
| Metrics Collection | Prometheus | Scrapes /metrics every 15 seconds |
| Visualization | Grafana | Live time-series graphs |
| Machine Learning | scikit-learn (Isolation Forest) | Unsupervised anomaly detection |
| Alerting | Slack Incoming Webhooks | Real-time incident notifications |
| Frontend | HTML5 + CSS3 + Jinja2 | Web dashboard interface |

---

## 📁 Project Structure

incident-response/
├── docker-compose.yml ← Orchestrates all 5 containers
├── prometheus.yml ← Prometheus scraping config
├── README.md ← This file
│
├── login-service/
│ ├── app.py ← Login Flask microservice
│ └── Dockerfile
│
├── order-service/
│ ├── app.py ← Order Flask microservice
│ └── Dockerfile
│
├── payment-service/
│ ├── app.py ← Payment Flask microservice
│ └── Dockerfile
│
├── anomaly-detector/
│ └── detector.py ← AI anomaly detection engine
│
└── dashboard-app/
├── app.py ← Dashboard Flask application
├── templates/
│ ├── login.html
│ ├── home.html
│ └── dashboard.html
└── static/
└── style.css


---

## 🚀 Quick Start

### Prerequisites
- Docker Desktop installed and running
- Python 3.10 or above
- A Slack workspace with an Incoming Webhook URL

### 1. Clone the repository
```bash
git clone https://github.com/keerthanaks-5/ai-incident-response-system.git
cd ai-incident-response-system
```

### 2. Add your Slack Webhook URL
Open `anomaly-detector/detector.py` and replace:
```python
SLACK_WEBHOOK_URL = "YOUR_SLACK_WEBHOOK_URL_HERE"
```
with your actual Slack webhook URL.

### 3. Start all Docker containers
```bash
docker-compose up -d
```

This starts 5 containers:
- login-service → port 5001
- order-service → port 5002
- payment-service → port 5003
- prometheus → port 9090
- grafana → port 3000

### 4. Install Python dependencies
```bash
pip install flask requests scikit-learn numpy
```

### 5. Start the AI Detector
Open a new terminal:
```bash
cd anomaly-detector
python detector.py
```

### 6. Start the Dashboard App
Open another terminal:
```bash
cd dashboard-app
python app.py
```

### 7. Open in browser

http://localhost:5050

Login with: **admin / admin123**

---

## 📊 Port Reference

| Component | Port | URL |
|---|---|---|
| Login Service | 5001 | http://localhost:5001 |
| Order Service | 5002 | http://localhost:5002 |
| Payment Service | 5003 | http://localhost:5003 |
| Prometheus | 9090 | http://localhost:9090 |
| Grafana | 3000 | http://localhost:3000 |
| Dashboard App | 5050 | http://localhost:5050 |

---

## 🤖 How the AI Works

The anomaly detector uses **Isolation Forest** — an unsupervised machine
learning algorithm that learns normal traffic patterns from a rolling
window of the last 50 metric readings.

Every 10 seconds it:
1. Pulls the current total request count from Prometheus
2. Adds it to the rolling window
3. Trains an Isolation Forest model on the window
4. Checks if the latest reading is statistically unusual
5. If anomalous → triggers the full incident response pipeline

**Key advantage:** No hardcoded thresholds. The AI adapts automatically
as normal traffic patterns change over time.

---

## 🚨 Automated Incident Response Pipeline

When an anomaly is detected:

🔍 Anomaly Detected
↓
📋 Step 1: Log incident to incidents.json
↓
🔍 Step 2: Check all service health endpoints
↓
💬 Step 3: Send Slack alert with full context
↓
🔇 5-minute cooldown (prevents alert spam)
↓
📊 Dashboard updates with new incident row


**Sample Slack Alert:**

🚨 Incident Alert
Time: 02:38:43
Metric: Total HTTP Requests
Value: 233.0
Status: Anomaly detected by AI monitoring system


---

## 📱 Web Dashboard Features

| Feature | Description |
|---|---|
| 🔐 Login Page | Session-based authentication |
| 🏠 Home Page | System overview and tech stack |
| 🟢 Service Health | Live green/red status for all 3 services |
| 📋 Incident History | Last 10 anomalies from incidents.json |
| 📊 Live Grafana Graph | Embedded real-time monitoring panel |

---

## 🔮 Future Scope

- **Multi-metric detection** — analyze error rates, CPU, memory together
- **Auto-remediation** — automatically restart failed services
- **Deep learning models** — LSTM or Autoencoder for time-series anomalies
- **Cloud deployment** — AWS/GCP with Kubernetes orchestration
- **PagerDuty integration** — enterprise on-call escalation workflows
- **Root cause analysis** — trace anomalies to originating service

---

## 👤 Author

**Keerthana**
Final Year MCA | Cloud & DevOps

---

## 📚 References

- Liu et al. (2008) — Isolation Forest Algorithm
- Prometheus Documentation — https://prometheus.io/docs
- Grafana Documentation — https://grafana.com/docs
- scikit-learn IsolationForest — https://scikit-learn.org
- Docker Documentation — https://docs.docker.com

## 📸 Screenshots

### 🔐 Login Page
![Login Page](login%20page.png)

### 🏠 Home Page
![Home Page](home%20page.png)

### 🟢 Dashboard — Service Health
![Dashboard Health](dashboard%20health.png)

### 📋 Dashboard — Incident Table
![Incident Table](incident%20table.png)

### 📊 Grafana Live Graph
![Grafana Graph](grafana%20graph.png)

### 🚨 Slack Alert
![Slack Alert](slack%20alerting.png)

### 📡 Prometheus Targets
![Prometheus Targets](prometheus%20targets.png)