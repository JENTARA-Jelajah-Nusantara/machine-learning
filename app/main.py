from fastapi import FastAPI
from app.routes import get_travel_spots_router, predict_router

app = FastAPI()

app.include_router(get_travel_spots_router, prefix="/api")
app.include_router(predict_router, prefix="/api")