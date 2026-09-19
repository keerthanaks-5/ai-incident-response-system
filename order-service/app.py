from flask import Flask
from prometheus_flask_exporter import PrometheusMetrics
import random
import logging

app = Flask(__name__)
metrics = PrometheusMetrics(app)
logging.basicConfig(level=logging.INFO)

@app.route("/order")
def order():
    if random.random() > 0.3:
        logging.info("📋 Order placed successfully")
        return {"status": "success", "message": "Order placed"}, 200
    else:
        logging.error("❌ Order failed - item out of stock")
        return {"status": "error", "message": "Order failed"}, 500

@app.route("/health")
def health():
    return {"status": "healthy", "service": "order"}, 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5002)