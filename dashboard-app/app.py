from flask import Flask, render_template, request, redirect, session, url_for
import json
import os
import requests

app = Flask(__name__)
app.secret_key = "demo-secret-key-change-in-production"

# Hardcoded demo credentials (NOT secure - for class demo purposes only)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "admin123"

SERVICES = {
    "login-service": "http://localhost:5001/health",
    "order-service": "http://localhost:5002/health",
    "payment-service": "http://localhost:5003/health"
}

INCIDENTS_FILE = "incidents.json"


def get_service_status():
    """Check health of each microservice"""
    status = {}
    for name, url in SERVICES.items():
        try:
            response = requests.get(url, timeout=2)
            status[name] = "healthy" if response.status_code == 200 else "unhealthy"
        except Exception:
            status[name] = "unreachable"
    return status


def get_recent_incidents():
    """Read incidents saved by the AI detector"""
    if os.path.exists(INCIDENTS_FILE):
        try:
            with open(INCIDENTS_FILE, "r") as f:
                incidents = json.load(f)
            return list(reversed(incidents))[:10]  # most recent first
        except (json.JSONDecodeError, FileNotFoundError):
            return []
    return []


@app.route("/")
def index():
    if "logged_in" in session:
        return redirect(url_for("home"))
    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("home"))
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))


@app.route("/home")
def home():
    if "logged_in" not in session:
        return redirect(url_for("login"))
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    if "logged_in" not in session:
        return redirect(url_for("login"))
    
    status = get_service_status()
    incidents = get_recent_incidents()
    return render_template("dashboard.html", status=status, incidents=incidents)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5050, debug=True)