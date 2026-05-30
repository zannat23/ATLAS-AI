from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil, os, sys
sys.path.append(".")

router = APIRouter()

# Load classifier once at startup
from src.medical.classifier import classify_wound

@router.get("/")
async def medical_root():
    return {
        "module": "Medical Triage",
        "status": "active",
        "classes": ['bruise','burn_mild','burn_severe',
                    'infection','laceration','normal']
    }

@router.post("/classify")
async def classify(file: UploadFile = File(...)):
    """Upload a wound image and get classification + first aid"""
    try:
        os.makedirs("outputs", exist_ok=True)
        temp_path = f"outputs/temp_{file.filename}"

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = classify_wound(temp_path)
        os.remove(temp_path)

        return {
            "status":     "success",
            "wound_type": result["wound_type"],
            "confidence": result["confidence"],
            "severity":   result["severity"],
            "first_aid":  result["first_aid"],
            "all_probs":  result["all_probs"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))