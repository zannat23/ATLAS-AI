from fastapi import APIRouter

router = APIRouter()

@router.get("/")
async def resources_root():
    return {
        "module": "Crisis Resource Locator",
        "status": "coming soon",
        "features": [
            "Nearby hospitals",
            "Water points",
            "Refugee camps",
            "NGO locations"
        ]
    }