from fastapi import FastAPI

app = FastAPI()
orders = {}

@app.post("/orders/{order_id}")
def create_order(order_id: str):
    orders[order_id] = "created"
    return {"order_id": order_id, "status": "created"}

@app.get("/orders/{order_id}")
def get_order(order_id: str):
    return {"order_id": order_id, "status": orders.get(order_id, "not found")}
