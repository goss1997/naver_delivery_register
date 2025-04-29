import os
import sys
from dotenv import load_dotenv

# .env 파일 로드 및 PYTHONPATH 반영
load_dotenv()
sys.path.append(os.getenv("PYTHONPATH", "./app"))

from fastapi import FastAPI
from schemas.schemas import DeliveryRegisterRequest, DeliveryRegisterResponse
from services.delivery_service import register_delivery

app = FastAPI()

@app.post("/register-delivery", response_model=DeliveryRegisterResponse)
async def register_delivery_api(request: DeliveryRegisterRequest):
    success, message = register_delivery(request)
    return DeliveryRegisterResponse(success=success, message=message)
