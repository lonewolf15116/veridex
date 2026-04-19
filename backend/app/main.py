import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.v1.routes_critique import router as critique_router

app = FastAPI(title="Veridex")

# Allowed frontend origins. Localhost stays for local dev.
# Production origins are the live Vercel URL and the apex/www on the real domain.
_DEFAULT_ORIGINS = [
    "http://localhost:3000",
    "https://veridex.fyi",
    "https://www.veridex.fyi",
]

# Optional: override / extend via env var (comma-separated).
# e.g. CORS_ALLOWED_ORIGINS="https://veridex-staging.vercel.app"
_env_origins = [o.strip() for o in os.getenv("CORS_ALLOWED_ORIGINS", "").split(",") if o.strip()]
ALLOWED_ORIGINS = _DEFAULT_ORIGINS + _env_origins

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(critique_router, prefix="/api/v1")


@app.get("/health")
def health():
    return {"status": "ok"}
