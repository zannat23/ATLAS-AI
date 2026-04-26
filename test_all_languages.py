import sys
sys.path.append(".")
from src.voice.pipeline import translate

samples = {
    "hi": "मुझे मदद चाहिए",
    "ar": "أحتاج إلى مساعدة",
    "bn": "আমার সাহায্য দরকার",
    "ur": "مجھے مدد چاہیے",
    "fr": "J'ai besoin d'aide",
    "de": "Ich brauche Hilfe",
    "es": "Necesito ayuda",
    "ru": "Мне нужна помощь",
    "tr": "Yardıma ihtiyacım var",
    "sw": "Ninahitaji msaada",
    "ta": "எனக்கு உதவி தேவை",
    "te": "నాకు సహాయం కావాలి",
    "mr": "मला मदत हवी आहे",
    "gu": "મારે મદદ જોઈએ છે",
    "pa": "ਮੈਨੂੰ ਮਦਦ ਦੀ ਲੋੜ ਹੈ",
    "zh": "我需要帮助",
    "ja": "助けが必要です",
    "ko": "도움이 필요합니다",
    "vi": "Tôi cần giúp đỡ",
    "th": "ฉันต้องการความช่วยเหลือ",
    "id": "Saya butuh bantuan",
    "ms": "Saya memerlukan bantuan",
    "tl": "Kailangan ko ng tulong",
    "nl": "Ik heb hulp nodig",
    "pl": "Potrzebuję pomocy",
    "pt": "Preciso de ajuda",
    "it": "Ho bisogno di aiuto",
    "ro": "Am nevoie de ajutor",
    "cs": "Potřebuji pomoc",
    "sk": "Potrebujem pomoc",
    "hu": "Segítségre van szükségem",
    "sv": "Jag behöver hjälp",
    "da": "Jeg har brug for hjælp",
    "no": "Jeg trenger hjelp",
    "fi": "Tarvitsen apua",
    "el": "Χρειάζομαι βοήθεια",
    "uk": "Мені потрібна допомога",
    "bg": "Нуждая се от помощ",
    "hr": "Trebam pomoć",
    "sr": "Треба ми помоћ",
    "sk": "Potrebujem pomoc",
    "lt": "Man reikia pagalbos",
    "lv": "Man vajag palīdzību",
    "et": "Vajan abi",
    "sq": "Kam nevojë për ndihmë",
    "mk": "Ми треба помош",
    "sl": "Potrebujem pomoč",
    "af": "Ek het hulp nodig",
    "zu": "Ngidinga usizo",
    "ne": "मलाई सहायता चाहिन्छ",
    "si": "මට උදව් අවශ්‍යයි",
    "km": "ខ្ញុំត្រូវការជំនួយ",
    "my": "ကျွန်တော် အကူအညီ လိုသည်",
    "ml": "എനിക്ക് സഹായം വേണം",
    "kn": "ನನಗೆ ಸಹಾಯ ಬೇಕು",
    "hy": "Ինձ օգնություն է պետք",
    "ka": "მე დახმარება მჭირდება",
    "uz": "Menga yordam kerak",
    "az": "Mənə kömək lazımdır",
    "kk": "Маған көмек керек",
}

# NLLB language codes mapping
NLLB_CODES = {
    "hi": "hin_Deva", "ar": "ara_Arab", "bn": "ben_Beng",
    "ur": "urd_Arab", "fr": "fra_Latn", "de": "deu_Latn",
    "es": "spa_Latn", "ru": "rus_Cyrl", "tr": "tur_Latn",
    "sw": "swh_Latn", "ta": "tam_Taml", "te": "tel_Telu",
    "mr": "mar_Deva", "gu": "guj_Gujr", "pa": "pan_Guru",
    "zh": "zho_Hans", "ja": "jpn_Jpan", "ko": "kor_Hang",
    "vi": "vie_Latn", "th": "tha_Thai", "id": "ind_Latn",
    "ms": "zsm_Latn", "tl": "tgl_Latn", "nl": "nld_Latn",
    "pl": "pol_Latn", "pt": "por_Latn", "it": "ita_Latn",
    "ro": "ron_Latn", "cs": "ces_Latn", "sk": "slk_Latn",
    "hu": "hun_Latn", "sv": "swe_Latn", "da": "dan_Latn",
    "no": "nob_Latn", "fi": "fin_Latn", "el": "ell_Grek",
    "uk": "ukr_Cyrl", "bg": "bul_Cyrl", "hr": "hrv_Latn",
    "sr": "srp_Cyrl", "lt": "lit_Latn", "lv": "lvs_Latn",
    "et": "est_Latn", "sq": "als_Latn", "mk": "mkd_Cyrl",
    "sl": "slv_Latn", "af": "afr_Latn", "zu": "zul_Latn",
    "ne": "npi_Deva", "si": "sin_Sinh", "km": "khm_Khmr",
    "my": "mya_Mymr", "ml": "mal_Mlym", "kn": "kan_Knda",
    "hy": "hye_Armn", "ka": "kat_Geor", "uz": "uzn_Latn",
    "az": "azj_Latn", "kk": "kaz_Cyrl",
}

print("=" * 65)
print("        ATLAS — 60+ Language Translation Test")
print("=" * 65)

success = 0
failed  = []

for lang, text in samples.items():
    try:
        nllb_code = NLLB_CODES.get(lang, "hin_Deva")
        english   = translate(text, src_lang=lang, tgt_lang="eng_Latn")
        print(f"✅ {lang:6} | {text:35} → {english}")
        success += 1
    except Exception as e:
        print(f"❌ {lang:6} | Failed: {e}")
        failed.append(lang)

print("=" * 65)
print(f"✅ Success : {success} languages")
print(f"❌ Failed  : {len(failed)} — {failed if failed else 'None'}")
print("=" * 65)