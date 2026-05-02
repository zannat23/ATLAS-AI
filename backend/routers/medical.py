from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def medical_root():
    return {
        "module": "Medical Triage",
        "status": "coming soon",
        "features": [
            "Wound classification",
            "Severity scoring",
            "First aid instructions",
            "QR triage card"
        ]
    }