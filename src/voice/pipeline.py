import re
import os
import torch
import whisper
import requests
import fasttext
from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
from langdetect import detect
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate as indic_transliterate

# Device
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print(f"Using device: {DEVICE}")

# Whisper
print("Loading Whisper model...")
whisper_model = whisper.load_model("small", device=DEVICE)
print("Whisper loaded")

# NLLB Translation
print("Loading translation model...")
MODEL_NAME = "facebook/nllb-200-distilled-600M"
tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
nllb_model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(DEVICE)
print("Translator loaded")

# fastText language-ID model (trained on large multilingual web/Wikipedia data)
FASTTEXT_MODEL_PATH = "lid.176.bin"
fasttext_model = None
if os.path.exists(FASTTEXT_MODEL_PATH):
    print("Loading fastText language ID model...")
    fasttext_model = fasttext.load_model(FASTTEXT_MODEL_PATH)
    print("fastText model loaded")
else:
    print("lid.176.bin not found - falling back to langdetect only")

LANG_CODES = {
    "hi": "hin_Deva", "mr": "mar_Deva", "ne": "npi_Deva", "bn": "ben_Beng", "as": "asm_Beng",
    "gu": "guj_Gujr", "pa": "pan_Guru", "or": "ory_Orya", "ta": "tam_Taml", "te": "tel_Telu",
    "kn": "kan_Knda", "ml": "mal_Mlym", "si": "sin_Sinh", "ur": "urd_Arab", "ar": "arb_Arab",
    "en": "eng_Latn", "fr": "fra_Latn", "de": "deu_Latn", "es": "spa_Latn", "pt": "por_Latn",
    "it": "ita_Latn", "nl": "nld_Latn", "ru": "rus_Cyrl", "uk": "ukr_Cyrl", "pl": "pol_Latn",
    "tr": "tur_Latn", "fa": "pes_Arab", "he": "heb_Hebr", "zh-cn": "zho_Hans", "ja": "jpn_Jpan",
    "ko": "kor_Hang", "th": "tha_Thai", "vi": "vie_Latn", "id": "ind_Latn", "ms": "zsm_Latn",
    "sw": "swh_Latn", "so": "som_Latn", "am": "amh_Ethi", "af": "afr_Latn", "zu": "zul_Latn",
    "el": "ell_Grek", "ro": "ron_Latn", "hu": "hun_Latn", "cs": "ces_Latn", "sv": "swe_Latn",
    "da": "dan_Latn", "fi": "fin_Latn", "no": "nob_Latn", "bg": "bul_Cyrl", "sr": "srp_Cyrl",
    "hr": "hrv_Latn", "sk": "slk_Latn", "tl": "tgl_Latn", "my": "mya_Mymr", "km": "khm_Khmr",
}

SHORT_TO_NAME = {
    "hi": "Hindi", "mr": "Marathi", "ne": "Nepali", "bn": "Bengali", "as": "Assamese",
    "gu": "Gujarati", "pa": "Punjabi", "or": "Odia", "ta": "Tamil", "te": "Telugu",
    "kn": "Kannada", "ml": "Malayalam", "si": "Sinhala", "ur": "Urdu", "ar": "Arabic",
    "en": "English", "fr": "French", "de": "German", "es": "Spanish", "pt": "Portuguese",
    "it": "Italian", "nl": "Dutch", "ru": "Russian", "uk": "Ukrainian", "pl": "Polish",
    "tr": "Turkish", "fa": "Persian", "he": "Hebrew", "zh-cn": "Chinese", "ja": "Japanese",
    "ko": "Korean", "th": "Thai", "vi": "Vietnamese", "id": "Indonesian", "ms": "Malay",
    "sw": "Swahili", "so": "Somali", "am": "Amharic", "af": "Afrikaans", "zu": "Zulu",
    "el": "Greek", "ro": "Romanian", "hu": "Hungarian", "cs": "Czech", "sv": "Swedish",
    "da": "Danish", "fi": "Finnish", "no": "Norwegian", "bg": "Bulgarian", "sr": "Serbian",
    "hr": "Croatian", "sk": "Slovak", "tl": "Tagalog", "my": "Burmese", "km": "Khmer",
}

def transcribe(audio_path: str) -> dict:
    print(f"Transcribing: {audio_path}")
    result = whisper_model.transcribe(audio_path, language=None, task="transcribe")
    return {"text": result["text"].strip(), "language": result["language"]}

def translate(text: str, src_lang: str, tgt_lang: str = "eng_Latn") -> str:
    src_code = LANG_CODES.get(src_lang, "eng_Latn")
    tokenizer.src_lang = src_code
    inputs = tokenizer(text, return_tensors="pt", padding=True).to(DEVICE)
    target_id = tokenizer.convert_tokens_to_ids(tgt_lang)
    outputs = nllb_model.generate(**inputs, forced_bos_token_id=target_id, max_length=512)
    return tokenizer.batch_decode(outputs, skip_special_tokens=True)[0]

def speak(text: str, language: str = "en", filename: str = "outputs/response.mp3") -> bool:
    from gtts import gTTS
    try:
        tts = gTTS(text=text, lang=language, slow=False)
        tts.save(filename)
        print(f"Audio saved: {filename}")
        return True
    except Exception as e:
        print(f"Audio not available for '{language}': {e}")
        return False

SCRIPT_RANGES = {
    "hi": (0x0900, 0x097F), "bn": (0x0980, 0x09FF), "pa": (0x0A00, 0x0A7F),
    "gu": (0x0A80, 0x0AFF), "or": (0x0B00, 0x0B7F), "ta": (0x0B80, 0x0BFF),
    "te": (0x0C00, 0x0C7F), "kn": (0x0C80, 0x0CFF), "ml": (0x0D00, 0x0D7F),
    "si": (0x0D80, 0x0DFF), "ar": (0x0600, 0x06FF), "he": (0x0590, 0x05FF),
    "el": (0x0370, 0x03FF), "ru": (0x0400, 0x04FF), "th": (0x0E00, 0x0E7F),
    "ko": (0xAC00, 0xD7AF), "ja": (0x3040, 0x30FF), "zh-cn": (0x4E00, 0x9FFF),
    "my": (0x1000, 0x109F), "km": (0x1780, 0x17FF), "am": (0x1200, 0x137F),
}

def detect_by_script(text: str):
    for ch in text:
        cp = ord(ch)
        for lang, (start, end) in SCRIPT_RANGES.items():
            if start <= cp <= end:
                return lang
    return None

def is_latin_script(text: str) -> bool:
    return bool(re.match(r"^[A-Za-z0-9\s.,!?'\"-]+$", text.strip()))

ROMAN_WORD_DICTS = {
    "hi": {
        "mujhe","mujhko","mera","meri","mere","hume","humein","hamara","hamari","tumhe","tumhara",
        "hai","hain","tha","thi","the","nahi","nahin","kya","kyun","kyunki","kaise","kaun","kahan",
        "kab","kitna","kitne","chahiye","chahie","karo","kro","karna","karein","kardo","kar",
        "do","dijiye","dena","lao","lana","batao","suno","dekho","jao","aao","aana","jana",
        "paani","pani","khana","khaana","madad","sahayata","bachao","chot","dard","bimar","beemar",
        "bukhar","dawa","dawai","aspatal","zakhmi","khoon","aag","raasta","rasta","ghar","gaon",
        "shehar","turant","jaldi","abhi","bhookh","bhook","pyaas","pyas","thand","garmi","sardi",
        "khansi","saans","behosh","yeh","woh","yahan","wahan","accha","theek","thik","bhai","behen",
        "maa","papa","beta","beti","haan","han","hoon","hun","raha","rahi","gaya","gayi",
    },
    "mr": {
        "mala","tula","tumhi","aamhi","mi","tu","ahe","ahet","hote","nahi","kay","ka","kasa","kase",
        "kuthe","kevha","kiti","havi","hava","have","kara","dya","paani","jevan","madad","vachva",
        "dukhapat","dawakhana","ghar","gaon","lavkar","atta","ho","dhanyawad","bhau","bahin","aai",
        "baba","tap","aushadh","rakta","aag","bhuk","tahan",
    },
    "bn": {
        "ami","tumi","apni","amar","tomar","amader","bhalo","bhalobashi","achi","acho","ache","chai",
        "lage","korchi","koro","korbo","keno","kobe","kothay","koto","kemon","khabo","khai","jol",
        "khudha","sahajjo","bachao","byatha","osudh","hasapatal","rokto","agun","bari","gram","shohor",
        "taratari","ekhoni","na","hae","dhonnobad","bhai","bon","ma","baba","jor","pipasa",
    },
    "ta": {
        "enakku","enakkuth","enaku","naan","nee","neenga","unakku","namma","enga","engal","thanneer",
        "thanni","tanni","vaendum","venum","vendum","saapadu","sappadu","udhavi","uthavi","kaapathunga",
        "vali","valikuthu","kaaychal","maruthuvam","maruthuvamanai","aaspathiri","ratham","thee",
        "veedu","oor","seekiram","ippo","illai","aamaam","nandri","anna","akka","amma","appa",
        "pasikkuthu","thaagam","enna","yaaru","engey","eppadi","eppo","evlo",
    },
    "te": {
        "naaku","nenu","nuvvu","meeru","mee","maa","neeru","neellu","thindi","annam","sahayam",
        "kaapadandi","noppi","jwaram","mandu","asupatri","raktham","mantalu","illu","ooru","twaraga",
        "ippudu","ledu","avunu","dhanyavadalu","anna","akka","amma","nanna","aakali","dahamga",
        "emi","evaru","ekkada","ela","eppudu","enta","kavali",
    },
    "kn": {
        "nanage","naanu","neenu","neevu","namma","neeru","oota","sahaya","kaapadi","novu","jwara",
        "aushadhi","aspatre","rakta","benki","mane","ooru","bega","eega","illa","houdu","dhanyavada",
        "anna","akka","amma","appa","hasivu","baayarike","enu","yaaru","elli","hege","yavaga","estu",
        "beku","bekagide",
    },
    "ml": {
        "enikku","njan","nee","ningal","namme","vellam","bhakshanam","sahayam","rakshikku","vedana",
        "pani","marunnu","aashupathri","raktham","thee","veedu","gramam","vegam","ippol","illa","athe",
        "nandi","chetta","chechi","amma","achan","visakkunnu","dahikkunnu","entha","aaru","evide",
        "engane","eppol","ethra","venam",
    },
    "gu": {
        "mane","hu","tame","tamaru","amaru","paani","jaman","madad","bachavo","dukhavo","taav",
        "dava","lohi","aag","ghar","gaam","jaldi","atyare","na","ha","aabhar","bhai",
        "ben","maa","pappa","bhookh","taras","shu","kon","kya","kevi","kyare","ketlu","joiye",
    },
    "pa": {
        "mainu","main","tu","tusi","sada","pani","khana","madad","bachao","dard","bukhar","dawai",
        "khoon","agg","ghar","pind","jaldi","hun","nahi","haan","dhanwaad","bhra","bhain",
        "mummy","papa","bhukh","pyaas","ki","kaun","kithe","kive","kado","kinna","chahida",
    },
}

def score_roman_language(text: str):
    words = re.findall(r"[a-zA-Z']+", text.lower())
    if not words:
        return None, 0.0
    best_lang, best_ratio = None, 0.0
    for lang, wordset in ROMAN_WORD_DICTS.items():
        matches = sum(1 for w in words if w in wordset)
        ratio = matches / len(words)
        if ratio > best_ratio:
            best_lang, best_ratio = lang, ratio
    return best_lang, best_ratio

TRANSLITERATION_TARGETS = {
    "hi": sanscript.DEVANAGARI, "mr": sanscript.DEVANAGARI, "bn": sanscript.BENGALI,
    "ta": sanscript.TAMIL, "te": sanscript.TELUGU, "kn": sanscript.KANNADA,
    "ml": sanscript.MALAYALAM, "gu": sanscript.GUJARATI, "pa": sanscript.GURMUKHI,
}

GOOGLE_TRANSLIT_CODES = {
    "hi": "hi", "mr": "mr", "bn": "bn", "ta": "ta", "te": "te",
    "kn": "kn", "ml": "ml", "gu": "gu", "pa": "pa", "ur": "ur",
    "ne": "ne", "or": "or", "as": "as", "si": "si",
}

def transliterate_smart(text: str, lang: str) -> str:
    code = GOOGLE_TRANSLIT_CODES.get(lang)
    if not code:
        return text
    try:
        out = []
        for w in text.split():
            r = requests.get(
                "https://inputtools.google.com/request",
                params={
                    "text": w, "itc": f"{code}-t-i0-und", "num": 1,
                    "cp": 0, "cs": 1, "ie": "utf-8", "oe": "utf-8",
                },
                timeout=5,
            )
            data = r.json()
            out.append(data[1][0][1][0] if data[0] == "SUCCESS" else w)
        result = " ".join(out)
        print(f"Transliterated [{lang}]: {text} -> {result}")
        return result
    except Exception as e:
        print(f"Online transliteration failed ({e}), using offline fallback")
        target_script = TRANSLITERATION_TARGETS.get(lang)
        if target_script:
            return indic_transliterate(text, sanscript.ITRANS, target_script)
        return text

def detect_with_fasttext(text: str):
    """Use fastText's ML model (trained on a very large multilingual corpus) as a
    stronger, broader-coverage fallback detector than a hand-written word list."""
    if not fasttext_model:
        return None
    try:
        labels, probs = fasttext_model.predict(text.replace("\n", " "), k=1)
        lang = labels[0].replace("__label__", "")
        confidence = float(probs[0])
        print(f"fastText: {lang} (confidence={confidence:.2f})")
        return lang if confidence > 0.5 else None
    except Exception as e:
        print(f"fastText detection failed: {e}")
        return None

def smart_detect_and_prepare(text: str) -> dict:
    """
    Fully automatic language handling for typed text - no manual selection needed.

    Tier 1: Native script present -> identified directly via Unicode range (100% reliable).
    Tier 2: Latin script -> scored against romanized Indian-language dictionaries;
            a confident match is transliterated into that language's native script,
            because NLLB only understands native scripts, not romanized input.
    Tier 3: fastText ML model - trained on a large multilingual corpus, broader
            coverage than the hand-written dictionaries above.
    Tier 4: langdetect as a final fallback.
    """
    stripped = text.strip()

    script_lang = detect_by_script(stripped)
    if script_lang:
        print(f"Script-detected: {script_lang}")
        return {"processed_text": stripped, "detected_lang": script_lang}

    if is_latin_script(stripped):
        roman_lang, ratio = score_roman_language(stripped)
        print(f"Roman word-score: lang={roman_lang} ratio={ratio:.2f}")
        if roman_lang and ratio >= 0.25:
            processed = transliterate_smart(stripped, roman_lang)
            return {"processed_text": processed, "detected_lang": roman_lang}

    ft_lang = detect_with_fasttext(stripped)
    if ft_lang and ft_lang in LANG_CODES:
        return {"processed_text": stripped, "detected_lang": ft_lang}

    try:
        detected = detect(stripped)
        if detected not in LANG_CODES:
            detected = "en"
    except Exception:
        detected = "en"
    print(f"Fallback langdetect: {detected}")
    return {"processed_text": stripped, "detected_lang": detected}