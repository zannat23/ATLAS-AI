from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
import sys
sys.path.append(".")
from src.resource.locator import search_resources, detect_intent

router = APIRouter()

class ResourceRequest(BaseModel):
    query:         str   = None
    resource_type: str   = None
    lat:           float = 18.5204
    lon:           float = 73.8567
    limit:         int   = 5

@router.get("/")
async def resources_root():
    return {
        "module": "Crisis Resource Locator",
        "status": "active",
        "types":  ["hospital","water","shelter","ngo","food"]
    }

@router.post("/search")
async def search(req: ResourceRequest):
    """Search for nearby resources."""
    try:
        resource_type = req.resource_type

        # Auto-detect from query if no type given
        if not resource_type and req.query:
            resource_type = detect_intent(req.query)

        results = search_resources(
            resource_type=resource_type,
            query=req.query,
            lat=req.lat,
            lon=req.lon,
            limit=req.limit
        )
        return {
            "status":        "success",
            "query":         req.query,
            "detected_type": resource_type,
            "count":         len(results),
            "results":       results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/types")
async def get_types():
    """Get all resource types."""
    return {
        "types": [
            {"id":"hospital","label":"🏥 Hospital",  "desc":"Medical help"},
            {"id":"water",   "label":"💧 Water",     "desc":"Drinking water"},
            {"id":"shelter", "label":"🏠 Shelter",   "desc":"Safe shelter"},
            {"id":"food",    "label":"🍱 Food",      "desc":"Free meals"},
            {"id":"ngo",     "label":"🤝 NGO",       "desc":"Aid organizations"},
        ]
    }