FROM python:3.11-slim

WORKDIR /app

COPY app.py .

RUN pip install flask prometheus-flask-exporter

CMD ["python", "app.py"]