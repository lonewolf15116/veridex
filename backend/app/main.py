from fastapi import FastAPI
from app.api.v1.routes_alchemy import router as alchemy_router

app = FastAPI(title="Alchemind")

app.include_router(alchemy_router, prefix="/api/v1")

@app.get("/health")
def health():
    return {"status": "ok"}