from fastapi import APIRouter, UploadFile, File, HTTPException
from pydantic import BaseModel
import sys, os, shutil
sys.path.append(".")
from src.voice.pipeline import transcribe, translate, speak

router = APIRouter()

# ── Request/Response models ────────────────────────
class TranslateRequest(BaseModel):
    text: str
    src_lang: str = "hi"
    tgt_lang: str = "eng_Latn"

class TranslateResponse(BaseModel):
    original_text:  str
    translated_text: str
    src_lang:       str
    tgt_lang:       str

class FullPipelineRequest(BaseModel):
    text:            str
    src_lang:        str = "hi"
    target_language: str = "Hindi"

# ── Endpoints ──────────────────────────────────────
@router.get("/")
async def voice_root():
    return {"module": "Voice Bridge", "status": "active"}

@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    """
    Upload an audio file → get transcription + language
    """
    try:
        # Save uploaded file temporarily
        temp_path = f"outputs/temp_{file.filename}"
        os.makedirs("outputs", exist_ok=True)

        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Transcribe
        result = transcribe(temp_path)

        # Clean up temp file
        os.remove(temp_path)

        return {
            "status":   "success",
            "text":     result["text"],
            "language": result["language"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/translate", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest):
    """
    Translate text from one language to another
    """
    try:
        translated = translate(
            request.text,
            src_lang=request.src_lang,
            tgt_lang=request.tgt_lang
        )
        return TranslateResponse(
            original_text   = request.text,
            translated_text = translated,
            src_lang        = request.src_lang,
            tgt_lang        = request.tgt_lang
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/full-pipeline")
async def full_pipeline(request: FullPipelineRequest):
    """
    Full ATLAS pipeline — text in any language → response in target language
    """
    try:
        target_codes = {
            "Hindi":   ("hin_Deva", "hi"),
            "Arabic":  ("ara_Arab", "ar"),
            "Bengali": ("ben_Beng", "bn"),
            "Urdu":    ("urd_Arab", "ur"),
            "French":  ("fra_Latn", "fr"),
            "German":  ("deu_Latn", "de"),
            "Spanish": ("spa_Latn", "es"),
            "English": ("eng_Latn", "en"),
        }

        # Translate to English first
        english_text = translate(
            request.text,
            src_lang=request.src_lang,
            tgt_lang="eng_Latn"
        )

        # Generate response
        response_english = f"I understand. You said: {english_text}. ATLAS is here to help."

        # Translate to target language
        nllb_code, tts_code = target_codes.get(
            request.target_language, ("eng_Latn", "en"))

        response_translated = translate(
            response_english,
            src_lang="en",
            tgt_lang=nllb_code
        )

        # Generate audio
        audio_path = "outputs/atlas_response.mp3"
        speak(response_translated,
              language=tts_code,
              filename=audio_path)

        return {
            "status":             "success",
            "original_text":      request.text,
            "english_text":       english_text,
            "response_english":   response_english,
            "response_translated": response_translated,
            "audio_path":         audio_path,
            "target_language":    request.target_language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))