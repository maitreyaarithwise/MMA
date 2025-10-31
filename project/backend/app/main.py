from fastapi import FastAPI
from app.api.api import api_router

app = FastAPI(
    title="Market Making Trading Dashboard API",
    description="API for market making trading dashboard with Pinnacle odds integration",
    version="1.0.0"
)

app.include_router(api_router)

@app.get("/")
async def root():
    return {"message": "Market Making Trading Dashboard API"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

