import whisper
import torch
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer

# ── Device ────────────────────────────────────────
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {DEVICE}")

# ── Whisper ───────────────────────────────────────
print("Loading Whisper model...")
whisper_model = whisper.load_model("small", device=DEVICE)
print("Whisper loaded ✅")

# ── NLLB Translation ──────────────────────────────
print("Loading translation model...")
MODEL_NAME = "facebook/nllb-200-distilled-600M"
tokenizer  = AutoTokenizer.from_pretrained(MODEL_NAME)
nllb_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(DEVICE)
print("Translator loaded ✅")

# ── Language codes ────────────────────────────────
LANG_CODES = {
    "hi": "hin_Deva",
    "ar": "ara_Arab",
    "ur": "urd_Arab",
    "bn": "ben_Beng",
    "en": "eng_Latn",
    "fr": "fra_Latn",
    "so": "som_Latn",
}

# ── Functions ─────────────────────────────────────
def transcribe(audio_path: str) -> dict:
    print(f"Transcribing: {audio_path}")
    result = whisper_model.transcribe(
        audio_path,
        language=None,
        task="transcribe"
    )
    return {
        "text":     result["text"].strip(),
        "language": result["language"]
    }

def translate(text: str, src_lang: str,
              tgt_lang: str = "eng_Latn") -> str:
    src_code = LANG_CODES.get(src_lang, "hin_Deva")

    tokenizer.src_lang = src_code
    inputs = tokenizer(
        text,
        return_tensors="pt",
        padding=True
    ).to(DEVICE)

    target_id = tokenizer.convert_tokens_to_ids(tgt_lang)

    outputs = nllb_model.generate(
        **inputs,
        forced_bos_token_id=target_id,
        max_length=512
    )
    return tokenizer.batch_decode(
        outputs, skip_special_tokens=True)[0]

def speak(text: str, language: str = "en",
          filename: str = "outputs/response.mp3"):
    from gtts import gTTS
    import os
    TTS_CODES = {
        "hi": "hi", "ar": "ar", "en": "en",
        "ur": "ur", "bn": "bn", "fr": "fr"
    }
    lang_code = TTS_CODES.get(language, "en")
    tts = gTTS(text=text, lang=lang_code, slow=False)
    tts.save(filename)
    os.system(f"start {filename}")
    print(f"Speaking in {language} ✅")