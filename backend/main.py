from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import voice, medical, resources

# ── App setup ─────────────────────────────────────
app = FastAPI(
    title="ATLAS AI API",
    description="Offline Multilingual Crisis Assistance System",
    version="1.0.0"
)

# ── CORS — allows React to call this API ──────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000",
                   "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Routers ───────────────────────────────────────
app.include_router(voice.router,     prefix="/api/voice",     tags=["Voice"])
app.include_router(medical.router,   prefix="/api/medical",   tags=["Medical"])
app.include_router(resources.router, prefix="/api/resources", tags=["Resources"])

# ── Health check ──────────────────────────────────
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