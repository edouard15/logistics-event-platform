from fastapi import FastAPI
import requests

app = FastAPI()

@app.get("/track/{id}")
def track(id: str):
    return requests.get(f"http://tracking-service:8000/track/{id}").json()

@app.post("/orders/{id}")
def create_order(id: str):
    return requests.post(f"http://order-service:8000/orders/{id}").json()
