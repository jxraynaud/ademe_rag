from fastapi import FastAPI
from app.api.models import CarbEquiv
from app.services.carb_equiv_service import process_carb_equiv

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Greetings from the server!"}

@app.post("/carb_equiv")
def create_carb_equiv(carb_equiv: CarbEquiv):
    processed_data = process_carb_equiv(carb_equiv)
    return {"payload_processed": processed_data}
