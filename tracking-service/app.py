from fastapi import FastAPI, HTTPException
import time
import logging
import os

from prometheus_client import Counter, Histogram, start_http_server

app = FastAPI()
logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

REQUEST_COUNT = Counter("http_requests_total", "Total requests")
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Latency")


def init_observability():
    try:
        start_http_server(int(os.getenv("METRICS_PORT", "8000")))
    except OSError:
        pass


@app.on_event("startup")
def startup():
    init_observability()


@app.get("/track/{shipment_id}")
def track(shipment_id: str):
    start = time.time()
    REQUEST_COUNT.inc()

    if not shipment_id:
        raise HTTPException(status_code=400, detail="Invalid shipment ID")

    logger.info("tracking %s", shipment_id)

    REQUEST_LATENCY.observe(time.time() - start)

    return {"shipment_id": shipment_id, "status": "In Transit"}
