from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
import random
import logging

app = Flask(__name__)
metrics = PrometheusMetrics(app)
logging.basicConfig(level=logging.INFO)

@app.route("/payment")
def payment():
    if random.random() > 0.4:
        logging.info("💳 Payment processed successfully")
        return {"status": "success", "message": "Payment processed"}, 200
    else:
        logging.error("❌ Payment failed - timeout")
        return {"status": "error", "message": "Payment timeout"}, 503

@app.route("/health")
def health():
    return {"status": "healthy", "service": "payment"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)