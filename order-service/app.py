from fastapi import FastAPI, HTTPException

app = FastAPI()
orders = {}


@app.post("/orders/{order_id}")
def create_order(order_id: str):
    orders[order_id] = "created"
    return {
        "order_id": order_id,
        "status": "created",
    }


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if order_id not in orders:
        raise HTTPException(status_code=404, detail="Order not found")

    return {
        "order_id": order_id,
        "status": orders[order_id],
    }
