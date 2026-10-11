"""
Indian languages ke liye translation (IndicTrans2) + voice (Indic Parler-TTS).
Models pehli baar use hone par download hote hain (internet chahiye), uske baad offline chalte hain.
"""
import torch

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Parler-TTS (voice) band karna ho to False kar do (sirf text aayega)
USE_INDIC_TTS = True

# dropdown ka naam (lowercase) -> (IndicTrans2 code, Parler-TTS audio support)
INDIC_LANGS = {
    "assamese": ("asm_Beng", True),
    "bengali": ("ben_Beng", True),
    "bodo": ("brx_Deva", True),
    "dogri": ("doi_Deva", True),
    "gujarati": ("guj_Gujr", True),
    "hindi": ("hin_Deva", True),
    "kannada": ("kan_Knda", True),
    "kashmiri": ("kas_Arab", False),
    "konkani": ("gom_Deva", True),
    "maithili": ("mai_Deva", True),
    "malayalam": ("mal_Mlym", True),
    "manipuri (meitei)": ("mni_Mtei", True),
    "marathi": ("mar_Deva", True),
    "nepali": ("npi_Deva", True),
    "odia": ("ory_Orya", True),
    "punjabi": ("pan_Guru", False),   # audio ke liye gTTS fallback (internet chahiye)
    "sanskrit": ("san_Deva", True),
    "santali": ("sat_Olck", True),
    "sindhi": ("snd_Deva", True),
    "tamil": ("tam_Taml", True),
    "telugu": ("tel_Telu", True),
    "urdu": ("urd_Arab", True),
}

TRANSLATION_MODEL = "ai4bharat/indictrans2-en-indic-dist-200M"
TTS_MODEL = "ai4bharat/indic-parler-tts"
VOICE_DESCRIPTION = (
    "A female speaker delivers a clear and calm speech with a moderate speed and pitch. "
    "The recording is of very high quality, with the speaker's voice sounding clear and very close up."
)

_tr = {}
_tts = {}


def indic_available() -> bool:
    """IndicTransToolkit installed hai ya nahi (Windows par aksar nahi hota)."""
    try:
        try:
            from IndicTransToolkit import IndicProcessor  # noqa: F401
        except ImportError:
            try:
                from IndicTransToolkit.processor import IndicProcessor  # noqa: F401
            except ImportError:
                from IndicTransToolkit.IndicTransToolkit import IndicProcessor  # noqa: F401
        return True
    except Exception:
        return False


def _load_translator():
    if not _tr:
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        # IndicTransToolkit ke alag versions me IndicProcessor alag jagah milta hai
        try:
            from IndicTransToolkit import IndicProcessor
        except ImportError:
            try:
                from IndicTransToolkit.processor import IndicProcessor
            except ImportError:
                from IndicTransToolkit.IndicTransToolkit import IndicProcessor
        print("[indic] Loading IndicTrans2 (first time download hoga)...")
        _tr["tok"] = AutoTokenizer.from_pretrained(TRANSLATION_MODEL, trust_remote_code=True)
        _tr["model"] = AutoModelForSeq2SeqLM.from_pretrained(
            TRANSLATION_MODEL, trust_remote_code=True
        ).to(DEVICE).eval()
        _tr["ip"] = IndicProcessor(inference=True)
        print("[indic] IndicTrans2 loaded")
    return _tr["tok"], _tr["model"], _tr["ip"]


def translate_en_to_indic(texts: list, tgt_code: str) -> list:
    """English sentences ko Indian language me translate karta hai."""
    tok, model, ip = _load_translator()
    batch = ip.preprocess_batch(texts, src_lang="eng_Latn", tgt_lang=tgt_code)
    inputs = tok(
        batch, truncation=True, padding="longest",
        return_tensors="pt", return_attention_mask=True,
    ).to(DEVICE)
    def _generate(use_cache):
        with torch.no_grad():
            return model.generate(
                **inputs, use_cache=use_cache, min_length=0,
                max_length=256, num_beams=5, num_return_sequences=1,
            )
    try:
        out = _generate(True)
    except Exception as e:
        # Kuch transformers versions me cache wali generation fail hoti hai
        print(f"[indic] generate(use_cache=True) failed ({e}); retrying with use_cache=False")
        out = _generate(False)
    decoded = tok.batch_decode(out, skip_special_tokens=True, clean_up_tokenization_spaces=True)
    return ip.postprocess_batch(decoded, lang=tgt_code)


def _load_tts():
    if not _tts:
        from parler_tts import ParlerTTSForConditionalGeneration
        from transformers import AutoTokenizer
        print("[indic] Loading Indic Parler-TTS (first time download hoga)...")
        model = ParlerTTSForConditionalGeneration.from_pretrained(TTS_MODEL).to(DEVICE)
        _tts["model"] = model
        _tts["tok"] = AutoTokenizer.from_pretrained(TTS_MODEL)
        _tts["dtok"] = AutoTokenizer.from_pretrained(model.config.text_encoder._name_or_path)
        print("[indic] Indic Parler-TTS loaded")
    return _tts["model"], _tts["tok"], _tts["dtok"]


def indic_tts(texts: list, out_path: str) -> str:
    """Har sentence ki audio banakar ek .wav file me jodta hai."""
    import numpy as np
    import soundfile as sf
    model, tok, dtok = _load_tts()
    sr = model.config.sampling_rate
    silence = np.zeros(int(0.5 * sr), dtype="float32")
    pieces = []
    for t in texts:
        d = dtok(VOICE_DESCRIPTION, return_tensors="pt").to(DEVICE)
        p = tok(t, return_tensors="pt").to(DEVICE)
        with torch.no_grad():
            gen = model.generate(
                input_ids=d.input_ids, attention_mask=d.attention_mask,
                prompt_input_ids=p.input_ids, prompt_attention_mask=p.attention_mask,
            )
        pieces.append(gen.cpu().numpy().squeeze().astype("float32"))
        pieces.append(silence)
    sf.write(out_path, np.concatenate(pieces), sr)
    return out_path