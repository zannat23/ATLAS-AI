from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from pydantic import BaseModel
import sys, os, shutil, uuid
sys.path.append(".")
from src.voice.pipeline import transcribe, translate, speak, smart_detect_and_prepare, SHORT_TO_NAME

router = APIRouter()

# name -> (NLLB FLORES-200 code, gTTS code or None if gTTS doesn't support it)
TARGET_CODES = {
    # South Asian
    "Hindi": ("hin_Deva", "hi"), "English": ("eng_Latn", "en"), "Bengali": ("ben_Beng", "bn"),
    "Urdu": ("urd_Arab", "ur"), "Tamil": ("tam_Taml", "ta"), "Telugu": ("tel_Telu", "te"),
    "Marathi": ("mar_Deva", "mr"), "Gujarati": ("guj_Gujr", "gu"), "Punjabi": ("pan_Guru", "pa"),
    "Kannada": ("kan_Knda", "kn"), "Malayalam": ("mal_Mlym", "ml"), "Nepali": ("npi_Deva", "ne"),
    "Sinhala": ("sin_Sinh", "si"), "Odia": ("ory_Orya", None), "Assamese": ("asm_Beng", None),
    "Sindhi": ("snd_Arab", "sd"), "Pashto": ("pbt_Arab", "ps"),
    # East / Southeast Asian
    "Chinese (Simplified)": ("zho_Hans", "zh-CN"), "Chinese (Traditional)": ("zho_Hant", "zh-TW"),
    "Japanese": ("jpn_Jpan", "ja"), "Korean": ("kor_Hang", "ko"), "Thai": ("tha_Thai", "th"),
    "Vietnamese": ("vie_Latn", "vi"), "Indonesian": ("ind_Latn", "id"), "Malay": ("zsm_Latn", "ms"),
    "Javanese": ("jav_Latn", "jw"), "Sundanese": ("sun_Latn", "su"), "Khmer": ("khm_Khmr", "km"),
    "Lao": ("lao_Laoo", None), "Burmese": ("mya_Mymr", "my"), "Tagalog": ("tgl_Latn", "tl"),
    "Cebuano": ("ceb_Latn", "ceb"), "Hmong": ("hmn_Latn", "hmn"),
    # Middle Eastern / Central Asian
    "Arabic": ("arb_Arab", "ar"), "Hebrew": ("heb_Hebr", "iw"), "Persian": ("pes_Arab", None),
    "Turkish": ("tur_Latn", "tr"), "Azerbaijani": ("azj_Latn", "az"), "Kazakh": ("kaz_Cyrl", None),
    "Uzbek": ("uzn_Latn", "uz"), "Mongolian": ("khk_Cyrl", "mn"), "Tajik": ("tgk_Cyrl", None),
    "Kurdish": ("ckb_Arab", "ku"), "Armenian": ("hye_Armn", "hy"), "Georgian": ("kat_Geor", None),
    # European
    "French": ("fra_Latn", "fr"), "German": ("deu_Latn", "de"), "Spanish": ("spa_Latn", "es"),
    "Portuguese": ("por_Latn", "pt"), "Italian": ("ita_Latn", "it"), "Dutch": ("nld_Latn", "nl"),
    "Russian": ("rus_Cyrl", "ru"), "Ukrainian": ("ukr_Cyrl", "uk"), "Polish": ("pol_Latn", "pl"),
    "Czech": ("ces_Latn", "cs"), "Slovak": ("slk_Latn", "sk"), "Bulgarian": ("bul_Cyrl", "bg"),
    "Serbian": ("srp_Cyrl", "sr"), "Croatian": ("hrv_Latn", "hr"), "Bosnian": ("bos_Latn", "bs"),
    "Slovenian": ("slv_Latn", None), "Macedonian": ("mkd_Cyrl", "mk"), "Romanian": ("ron_Latn", "ro"),
    "Hungarian": ("hun_Latn", "hu"), "Finnish": ("fin_Latn", "fi"), "Estonian": ("est_Latn", "et"),
    "Latvian": ("lvs_Latn", "lv"), "Lithuanian": ("lit_Latn", None), "Swedish": ("swe_Latn", "sv"),
    "Norwegian": ("nob_Latn", "no"), "Danish": ("dan_Latn", "da"), "Icelandic": ("isl_Latn", "is"),
    "Greek": ("ell_Grek", "el"), "Catalan": ("cat_Latn", "ca"), "Galician": ("glg_Latn", "gl"),
    "Basque": ("eus_Latn", "eu"), "Welsh": ("cym_Latn", "cy"), "Irish": ("gle_Latn", None),
    "Scots Gaelic": ("gla_Latn", "gd"), "Maltese": ("mlt_Latn", "mt"), "Albanian": ("sqi_Latn", "sq"),
    "Belarusian": ("bel_Cyrl", "be"), "Luxembourgish": ("ltz_Latn", "lb"), "Frisian": ("fry_Latn", "fy"),
    "Corsican": ("cos_Latn", "co"), "Haitian Creole": ("hat_Latn", "ht"),
    # African
    "Swahili": ("swh_Latn", "sw"), "Amharic": ("amh_Ethi", "am"), "Somali": ("som_Latn", "so"),
    "Hausa": ("hau_Latn", None), "Yoruba": ("yor_Latn", None), "Igbo": ("ibo_Latn", None),
    "Zulu": ("zul_Latn", "zu"), "Xhosa": ("xho_Latn", None), "Afrikaans": ("afr_Latn", "af"),
    "Sesotho": ("sot_Latn", "st"), "Shona": ("sna_Latn", "sn"), "Kinyarwanda": ("kin_Latn", None),
    "Malagasy": ("plt_Latn", "mg"),
    # Pacific / Other
    "Hawaiian": ("haw_Latn", "haw"), "Maori": ("mri_Latn", "mi"), "Samoan": ("smo_Latn", "sm"),
}


# ── Models ──────────────────────────────────────────
class TranslateRequest(BaseModel):
    text: str
    src_lang: str = "hi"
    tgt_lang: str = "eng_Latn"


class TranslateResponse(BaseModel):
    original_text: str
    translated_text: str
    src_lang: str
    tgt_lang: str


class FullPipelineRequest(BaseModel):
    text: str
    src_lang: str = "hi"
    target_language: str = "Hindi"


class ConverseTextRequest(BaseModel):
    text: str
    target_language: str = "English"


# ── Basic endpoints ─────────────────────────────────
@router.get("/")
async def voice_root():
    return {"module": "Voice Bridge", "status": "active", "supported_languages": len(TARGET_CODES)}


@router.get("/languages")
async def get_languages():
    return {"languages": list(TARGET_CODES.keys()), "count": len(TARGET_CODES)}


@router.post("/transcribe")
async def transcribe_audio(file: UploadFile = File(...)):
    try:
        temp_path = f"outputs/temp_{file.filename}"
        os.makedirs("outputs", exist_ok=True)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
        result = transcribe(temp_path)
        os.remove(temp_path)
        return {"status": "success", "text": result["text"], "language": result["language"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/translate", response_model=TranslateResponse)
async def translate_text(request: TranslateRequest):
    try:
        translated = translate(request.text, src_lang=request.src_lang, tgt_lang=request.tgt_lang)
        return TranslateResponse(
            original_text=request.text, translated_text=translated,
            src_lang=request.src_lang, tgt_lang=request.tgt_lang
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/full-pipeline")
async def full_pipeline(request: FullPipelineRequest):
    try:
        english_text = translate(request.text, src_lang=request.src_lang, tgt_lang="eng_Latn")
        response_english = f"I understand. You said: {english_text}. ATLAS is here to help."
        nllb_code, tts_code = TARGET_CODES.get(request.target_language, ("eng_Latn", "en"))
        response_translated = translate(response_english, src_lang="en", tgt_lang=nllb_code)

        audio_url = None
        if tts_code:
            audio_filename = f"atlas_response_{uuid.uuid4().hex[:8]}.mp3"
            if speak(response_translated, language=tts_code, filename=f"outputs/{audio_filename}"):
                audio_url = f"/outputs/{audio_filename}"

        return {
            "status": "success", "original_text": request.text, "english_text": english_text,
            "response_english": response_english, "response_translated": response_translated,
            "audio_url": audio_url, "target_language": request.target_language
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Live conversation: VOICE input (Whisper auto-detects) ──
@router.post("/converse")
async def converse(file: UploadFile = File(...), target_language: str = Form(...)):
    try:
        temp_path = f"outputs/temp_{file.filename}"
        os.makedirs("outputs", exist_ok=True)
        with open(temp_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        transcript = transcribe(temp_path)
        os.remove(temp_path)

        detected_lang = transcript["language"]
        spoken_text = transcript["text"]

        nllb_code, tts_code = TARGET_CODES.get(target_language, ("eng_Latn", "en"))
        translated_text = translate(spoken_text, src_lang=detected_lang, tgt_lang=nllb_code)

        audio_url = None
        if tts_code:
            audio_filename = f"converse_{uuid.uuid4().hex[:8]}.mp3"
            if speak(translated_text, language=tts_code, filename=f"outputs/{audio_filename}"):
                audio_url = f"/outputs/{audio_filename}"

        return {
            "status": "success",
            "detected_language": detected_lang,
            "detected_language_name": SHORT_TO_NAME.get(detected_lang, detected_lang),
            "spoken_text": spoken_text,
            "translated_text": translated_text,
            "target_language": target_language,
            "audio_url": audio_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ── Live conversation: TEXT input (fully automatic) ─────────
@router.post("/converse-text")
async def converse_text(request: ConverseTextRequest):
    try:
        prep = smart_detect_and_prepare(request.text)
        processed_text = prep["processed_text"]
        detected_lang = prep["detected_lang"]

        nllb_code, tts_code = TARGET_CODES.get(request.target_language, ("eng_Latn", "en"))
        translated_text = translate(processed_text, src_lang=detected_lang, tgt_lang=nllb_code)

        audio_url = None
        if tts_code:
            audio_filename = f"converse_{uuid.uuid4().hex[:8]}.mp3"
            if speak(translated_text, language=tts_code, filename=f"outputs/{audio_filename}"):
                audio_url = f"/outputs/{audio_filename}"

        return {
            "status": "success",
            "detected_language": detected_lang,
            "detected_language_name": SHORT_TO_NAME.get(detected_lang, detected_lang),
            "spoken_text": request.text,
            "translated_text": translated_text,
            "target_language": request.target_language,
            "audio_url": audio_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))