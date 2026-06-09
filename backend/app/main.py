# app/main.py
from fastapi import FastAPI
from app.api.alerts import router as alerts_router

app = FastAPI(title="AI Incident Assistant")

app.include_router(alerts_router, prefix="/api")