from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
import shutil, os, sys, uuid, json, importlib
sys.path.append(".")

router = APIRouter()

# Load classifier once at startup
from src.medical.classifier import classify_wound
from src.medical.first_aid_kb import (
    WOUND_FIRST_AID, SYMPTOM_GUIDES, get_tailored_first_aid
)
from src.medical import indic_support
from src.medical.lang_table import LANG_TABLE, INDIC_NLLB_BACKUP, slugify, pick_gtts

# ------------------------------------------------------------------
# Settings
# ------------------------------------------------------------------
# Cache (build_translations.py se bana) me jawab na mile to live model chalaye?
# False = sirf cache (tez, offline). True = cache miss par heavy model load hoga (slow).
LIVE_FALLBACK = False

CACHE_DIR = os.path.join("cache", "first_aid")
AUDIO_DIR = "outputs"  # live-generated audio yahan jati hai

# ------------------------------------------------------------------
# Voice module (NLLB translate + gTTS speak) - sirf live fallback ke liye
# ------------------------------------------------------------------
VOICE_MODULE = "src.voice.pipeline"
voice = None
try:
    voice = importlib.import_module(VOICE_MODULE)
    print(f"[medical] Using voice module: {VOICE_MODULE}")
except Exception as _e:
    print(f"[medical] Voice module import failed: {_e}")

try:
    from gtts.lang import tts_langs
    GTTS_OK = set(tts_langs().keys())
except Exception:
    GTTS_OK = None


# ------------------------------------------------------------------
# Cache lookup
# ------------------------------------------------------------------
def load_cache_for(slug: str) -> dict:
    """translations/<slug>.json + overrides/<slug>.json (overrides jeette hain)."""
    merged = {}
    for folder in ("translations", "overrides"):
        path = os.path.join(CACHE_DIR, folder, f"{slug}.json")
        if not os.path.exists(path):
            continue
        try:
            with open(path, encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"[medical] cache read failed ({path}): {e}")
            continue
        merged.update({k: v for k, v in data.items() if isinstance(v, str) and v.strip()})
    return merged


def find_cached_audio(slug: str, condition: str):
    for ext in ("wav", "mp3"):
        if os.path.exists(os.path.join(CACHE_DIR, "audio", slug, f"{condition}.{ext}")):
            return f"/api/medical/cached-audio/{slug}/{condition}.{ext}"
    return None


def try_cache(slug: str, condition: str, english_steps: list):
    """Poora jawab cache me ho to (steps, text, audio_url) deta hai, warna None."""
    tr = load_cache_for(slug)
    if not tr or not all(s["instruction"] in tr for s in english_steps):
        return None
    steps = []
    for s in english_steps:
        note = s.get("item_note")
        steps.append({
            "instruction": tr[s["instruction"]],
            "instruction_en": s["instruction"],
            # note cache me na ho to English hi dikhao
            "item_note": tr.get(note, note) if note else None,
        })
    text = "\n".join(f"{i + 1}. {s['instruction']}" for i, s in enumerate(steps))
    return steps, text, find_cached_audio(slug, condition)


# ------------------------------------------------------------------
# Live (model-based) path - cache miss par
# ------------------------------------------------------------------
def apply_translation(english_steps: list, translate_fn) -> list:
    """translate_fn(list[str]) -> list[str]. Steps aur item notes dono translate hote hain."""
    texts = [s["instruction"] for s in english_steps]
    note_idx = [i for i, s in enumerate(english_steps) if s.get("item_note")]
    texts += [english_steps[i]["item_note"] for i in note_idx]
    out = translate_fn(texts)
    n = len(english_steps)
    notes = dict(zip(note_idx, out[n:]))
    return [
        {
            "instruction": out[i],
            "instruction_en": english_steps[i]["instruction"],
            "item_note": notes.get(i),
        }
        for i in range(n)
    ]


def nllb_translate_fn(nllb_code):
    return lambda texts: [voice.translate(t, "en", nllb_code) for t in texts]


def live_path(key: str, target_language: str, english_steps: list):
    """Returns (steps, translated_text, audio_url, warning)."""
    steps, translated_text, audio_url, warning = english_steps, None, None, None

    if key in indic_support.INDIC_LANGS:
        tgt_code, has_tts = indic_support.INDIC_LANGS[key]
        translated = False
        try:
            steps = apply_translation(
                english_steps, lambda t: indic_support.translate_en_to_indic(t, tgt_code)
            )
            translated = True
        except Exception as e:
            print(f"[medical] IndicTrans2 failed: {e}")
            if voice is not None and key in INDIC_NLLB_BACKUP:
                try:
                    steps = apply_translation(english_steps, nllb_translate_fn(INDIC_NLLB_BACKUP[key]))
                    translated = True
                    warning = "IndicTrans2 unavailable, used the backup translator."
                except Exception as e2:
                    print(f"[medical] NLLB fallback failed: {e2}")
        if not translated:
            return english_steps, None, None, f"Could not translate to {target_language}. Showing English."

        translated_text = "\n".join(f"{i + 1}. {s['instruction']}" for i, s in enumerate(steps))
        try:
            if has_tts and indic_support.USE_INDIC_TTS:
                name = f"medical_{uuid.uuid4().hex}.wav"
                indic_support.indic_tts([s["instruction"] for s in steps], f"{AUDIO_DIR}/{name}")
                audio_url = f"/api/medical/audio/{name}"
            elif key == "punjabi" and voice is not None:
                name = f"medical_{uuid.uuid4().hex}.mp3"
                if voice.speak(translated_text, "pa", f"{AUDIO_DIR}/{name}"):
                    audio_url = f"/api/medical/audio/{name}"
            else:
                warning = (warning + " " if warning else "") + \
                    f"Audio is not available for {target_language}; text is shown."
        except Exception as e:
            print(f"[medical] Indic TTS failed: {e}")
            warning = (warning + " " if warning else "") + \
                f"Audio could not be generated for {target_language}."
        return steps, translated_text, audio_url, warning

    if key in LANG_TABLE:
        nllb_code, gtts_candidates = LANG_TABLE[key]
        if voice is None:
            return english_steps, None, None, "Translation module not available. Showing English."
        try:
            steps = apply_translation(english_steps, nllb_translate_fn(nllb_code))
            translated_text = "\n".join(f"{i + 1}. {s['instruction']}" for i, s in enumerate(steps))
            gcode = pick_gtts(gtts_candidates, GTTS_OK)
            if gcode:
                name = f"medical_{uuid.uuid4().hex}.mp3"
                if voice.speak(translated_text, gcode, f"{AUDIO_DIR}/{name}"):
                    audio_url = f"/api/medical/audio/{name}"
                else:
                    warning = f"Audio could not be generated for {target_language}."
            else:
                warning = f"Audio is not available for {target_language}; text is shown."
            return steps, translated_text, audio_url, warning
        except Exception as e:
            print(f"[medical] Translation failed: {e}")
            return english_steps, None, None, f"Could not translate to {target_language}. Showing English."

    return english_steps, None, None, f"'{target_language}' is not supported. Showing English."


# ------------------------------------------------------------------
# Routes
# ------------------------------------------------------------------
class SymptomGuideRequest(BaseModel):
    condition: str
    available_items: Optional[list] = None


@router.get("/")
async def medical_root():
    return {
        "module": "Medical Triage",
        "status": "active",
        "photo_classes": list(WOUND_FIRST_AID.keys()),
        "symptom_guides": list(SYMPTOM_GUIDES.keys()),
    }


@router.post("/classify")
async def classify(
    file: UploadFile = File(...),
    available_items: str = Form(None),
    target_language: str = Form("English"),
):
    """
    Wound image upload -> classification + first aid.
    Pehle cache/first_aid/ me translation + audio dhoondta hai (instant, offline).
    Na mile to (LIVE_FALLBACK=True par) live model se banata hai.
    """
    try:
        os.makedirs(AUDIO_DIR, exist_ok=True)
        temp_path = f"{AUDIO_DIR}/temp_{file.filename}"
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        result = classify_wound(temp_path)
        os.remove(temp_path)

        items_list = [i.strip() for i in available_items.split(",")] if available_items else []
        tailored = get_tailored_first_aid(result["wound_type"], items_list, is_symptom_guide=False)
        english_steps = tailored["steps"]
        steps = english_steps

        translated_text = None
        audio_url = None
        warning = None

        key = (target_language or "").strip().lower()

        if key in ("", "english", "en") or not english_steps:
            pass
        else:
            slug = slugify(target_language)
            hit = try_cache(slug, result["wound_type"], english_steps)
            if hit:
                steps, translated_text, audio_url = hit
                if not audio_url:
                    warning = f"Audio is not available for {target_language}; text is shown."
            elif LIVE_FALLBACK:
                steps, translated_text, audio_url, warning = live_path(key, target_language, english_steps)
            else:
                warning = f"'{target_language}' is not in the offline cache. Showing English."

        return {
            "status": "success",
            "wound_type": result["wound_type"],
            "confidence": result["confidence"],
            "severity": result["severity"],
            "first_aid": steps,
            "target_language": target_language,
            "translated_first_aid": translated_text,
            "audio_url": audio_url,
            "warning": warning,
            "all_probs": result["all_probs"],
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/audio/{filename}")
async def get_audio(filename: str):
    """Live-generated audio (outputs/ folder se)."""
    safe = os.path.basename(filename)
    path = os.path.join(AUDIO_DIR, safe)
    if not safe.startswith("medical_") or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Audio not found")
    media = "audio/wav" if safe.endswith(".wav") else "audio/mpeg"
    return FileResponse(path, media_type=media)


@router.get("/cached-audio/{slug}/{filename}")
async def get_cached_audio(slug: str, filename: str):
    """Pre-built audio (cache/first_aid/audio/<lang>/<condition>.wav|mp3)."""
    safe_slug = slugify(slug)
    safe = os.path.basename(filename)
    path = os.path.join(CACHE_DIR, "audio", safe_slug, safe)
    if not safe.endswith((".wav", ".mp3")) or not os.path.exists(path):
        raise HTTPException(status_code=404, detail="Audio not found")
    media = "audio/wav" if safe.endswith(".wav") else "audio/mpeg"
    return FileResponse(path, media_type=media)


@router.get("/symptoms")
async def list_symptoms():
    """Symptom-based emergency guides (jo photo se diagnose nahi hote)."""
    return {
        "symptoms": [
            {"id": key, "label": guide["label"], "severity": guide["severity"]}
            for key, guide in SYMPTOM_GUIDES.items()
        ]
    }


@router.post("/symptom-guide")
async def symptom_guide(request: SymptomGuideRequest):
    if request.condition not in SYMPTOM_GUIDES:
        raise HTTPException(status_code=404, detail=f"Unknown condition: {request.condition}")
    tailored = get_tailored_first_aid(request.condition, request.available_items, is_symptom_guide=True)
    return {"status": "success", **tailored}


@router.get("/wound-types")
async def list_wound_types():
    return {
        "wound_types": [
            {"id": key, "label": entry["summary"], "severity": entry["severity"]}
            for key, entry in WOUND_FIRST_AID.items()
        ]
    }