from fastapi import FastAPI, HTTPException
import requests

app = FastAPI()


@app.get("/track/{id}")
def track(id: str):
    response = requests.get(f"http://tracking-service:8000/track/{id}")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Tracking failed")
    return response.json()


@app.post("/orders/{id}")
def create_order(id: str):
    response = requests.post(f"http://order-service:8000/orders/{id}")
    if response.status_code != 200:
        raise HTTPException(status_code=500, detail="Order failed")
    return response.json()
