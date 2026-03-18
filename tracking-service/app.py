from fastapi import FastAPI

app = FastAPI()

@app.get("/track/{shipment_id}")
def track(shipment_id: str):
    return {"shipment_id": shipment_id, "status": "In Transit"}
