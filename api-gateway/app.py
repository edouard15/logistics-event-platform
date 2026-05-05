from fastapi import FastAPI, HTTPException
import requests
import time
import logging

from prometheus_client import Counter, Histogram

app = FastAPI()

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

REQUEST_COUNT = Counter("http_requests_total", "Total requests")
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Latency")


@app.get("/track/{id}")
def track(id: str):
    start = time.time()
    REQUEST_COUNT.inc()

    try:
        response = requests.get(
            f"http://tracking-service:8000/track/{id}",
            timeout=5,
        )
    except requests.RequestException:
        raise HTTPException(status_code=500, detail="Tracking failed")

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Tracking failed")

    REQUEST_LATENCY.observe(time.time() - start)
    return response.json()


@app.post("/orders/{id}")
def create_order(id: str):
    start = time.time()
    REQUEST_COUNT.inc()

    try:
        response = requests.post(
            f"http://order-service:8000/orders/{id}",
            timeout=5,
        )
    except requests.RequestException:
        raise HTTPException(status_code=500, detail="Order failed")

    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Order failed")

    REQUEST_LATENCY.observe(time.time() - start)
    return response.json()
