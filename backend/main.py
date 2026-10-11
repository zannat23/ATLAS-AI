from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import os
from backend.routers import voice, medical, resources

app = FastAPI(
    title="ATLAS AI API",
    description="Offline Multilingual Crisis Assistance System",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

os.makedirs("outputs", exist_ok=True)
app.mount("/outputs", StaticFiles(directory="outputs"), name="outputs")

app.include_router(voice.router,     prefix="/api/voice",     tags=["Voice"])
app.include_router(medical.router,   prefix="/api/medical",   tags=["Medical"])
app.include_router(resources.router, prefix="/api/resources", tags=["Resources"])

@app.get("/")
async def root():
    return {
        "status": "✅ ATLAS API is running",
        "version": "1.0.0",
        "modules": ["voice", "medical", "resources"]
    }

@app.get("/health")
async def health():
    return {"status": "healthy", "gpu": True}