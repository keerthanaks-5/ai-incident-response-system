from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
import random
import logging

app = Flask(__name__)
metrics = PrometheusMetrics(app)
logging.basicConfig(level=logging.INFO)

@app.route("/login")
def login():
    if random.random() > 0.2:
        logging.info("✅ User logged in successfully")
        return {"status": "success", "message": "User logged in"}, 200
    else:
        logging.error("❌ Login failed - invalid credentials")
        return {"status": "error", "message": "Login failed"}, 401

@app.route("/health")
def health():
    return {"status": "healthy", "service": "login"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)