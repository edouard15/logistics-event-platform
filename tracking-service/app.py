from fastapi import FastAPI, HTTPException

app = FastAPI()


@app.get("/track/{shipment_id}")
def track(shipment_id: str):
    if not shipment_id:
        raise HTTPException(status_code=400, detail="Invalid shipment ID")

    return {
        "shipment_id": shipment_id,
        "status": "In Transit",
    }
