from fastapi import FastAPI, HTTPException
import time
import logging
import os

from prometheus_client import Counter, Histogram, start_http_server
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.jaeger.thrift import JaegerExporter

app = FastAPI()
orders = {}

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

REQUEST_COUNT = Counter("http_requests_total", "Total requests")
REQUEST_LATENCY = Histogram("http_request_duration_seconds", "Latency")

tracer = None


def init_observability():
    global tracer

    try:
        start_http_server(int(os.getenv("METRICS_PORT", "8000")))
    except OSError:
        pass

    trace.set_tracer_provider(TracerProvider())
    tracer = trace.get_tracer(__name__)

    try:
        exporter = JaegerExporter(
            agent_host_name=os.getenv(
                "JAEGER_HOST", "jaeger-agent"
            ),
            agent_port=int(os.getenv("JAEGER_PORT", "6831")),
        )

        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(exporter)
        )
    except Exception:
        pass


@app.on_event("startup")
def startup():
    init_observability()


@app.post("/orders/{order_id}")
def create_order(order_id: str):
    start = time.time()
    REQUEST_COUNT.inc()

    orders[order_id] = "created"

    if tracer:
        with tracer.start_as_current_span("create_order"):
            logger.info("order_created %s", order_id)

    REQUEST_LATENCY.observe(time.time() - start)

    return {"order_id": order_id, "status": "created"}


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    start = time.time()
    REQUEST_COUNT.inc()

    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")

    if tracer:
        with tracer.start_as_current_span("get_order"):
            logger.info("order_fetched %s", order_id)

    REQUEST_LATENCY.observe(time.time() - start)

    return {"order_id": order_id, "status": orders[order_id]}
