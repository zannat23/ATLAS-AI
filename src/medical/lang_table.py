"""
Shared language table for the Medical module.
Used by build_translations.py (offline cache builder) and medical.py (API).

NLLB table: (dropdown name, NLLB code, gTTS code(s) or None).
Indian languages that IndicTrans2 supports live in indic_support.INDIC_LANGS instead.
"""
import re


def slugify(name: str) -> str:
    """'Manipuri (Meitei)' -> 'manipuri_meitei'. Cache folder/file names me use hota hai."""
    return re.sub(r"[^a-z0-9]+", "_", (name or "").strip().lower()).strip("_")


LANGS = [
    # ---- Indian (NLLB only, IndicTrans2 me nahi hain) ----
    ("Awadhi", "awa_Deva", None), ("Bhojpuri", "bho_Deva", None), ("Chhattisgarhi", "hne_Deva", None),
    ("Kashmiri (Devanagari)", "kas_Deva", None), ("Magahi", "mag_Deva", None), ("Mizo", "lus_Latn", None),
    # ---- South / South-East / East Asia ----
    ("Sinhala", "sin_Sinh", "si"),
    ("Chinese (Simplified)", "zho_Hans", ["zh-CN", "zh"]), ("Chinese (Traditional)", "zho_Hant", ["zh-TW", "zh"]),
    ("Chinese", "zho_Hans", ["zh-CN", "zh"]),
    ("Japanese", "jpn_Jpan", "ja"), ("Korean", "kor_Hang", "ko"), ("Thai", "tha_Thai", "th"),
    ("Vietnamese", "vie_Latn", "vi"), ("Indonesian", "ind_Latn", "id"), ("Malay", "zsm_Latn", "ms"),
    ("Javanese", "jav_Latn", ["jw", "jv"]), ("Sundanese", "sun_Latn", "su"), ("Khmer", "khm_Khmr", "km"),
    ("Lao", "lao_Laoo", None), ("Burmese", "mya_Mymr", "my"), ("Tagalog", "tgl_Latn", ["tl", "fil"]),
    ("Filipino", "tgl_Latn", ["tl", "fil"]), ("Cebuano", "ceb_Latn", None),
    ("Tibetan", "bod_Tibt", None), ("Mongolian", "khk_Cyrl", None),
    # ---- Middle East / Central Asia / Caucasus ----
    ("Arabic", "arb_Arab", "ar"), ("Hebrew", "heb_Hebr", ["iw", "he"]), ("Persian", "pes_Arab", None),
    ("Dari", "prs_Arab", None), ("Pashto", "pbt_Arab", None), ("Turkish", "tur_Latn", "tr"),
    ("Azerbaijani", "azj_Latn", None), ("Kazakh", "kaz_Cyrl", None), ("Uzbek", "uzn_Latn", None),
    ("Tajik", "tgk_Cyrl", None), ("Kurdish", "ckb_Arab", None), ("Kurdish (Kurmanji)", "kmr_Latn", None),
    ("Armenian", "hye_Armn", None), ("Georgian", "kat_Geor", None), ("Kyrgyz", "kir_Cyrl", None),
    ("Turkmen", "tuk_Latn", None), ("Uyghur", "uig_Arab", None), ("Tatar", "tat_Cyrl", None),
    # ---- Europe ----
    ("French", "fra_Latn", "fr"), ("German", "deu_Latn", "de"), ("Spanish", "spa_Latn", "es"),
    ("Portuguese", "por_Latn", "pt"), ("Italian", "ita_Latn", "it"), ("Dutch", "nld_Latn", "nl"),
    ("Russian", "rus_Cyrl", "ru"), ("Ukrainian", "ukr_Cyrl", "uk"), ("Polish", "pol_Latn", "pl"),
    ("Czech", "ces_Latn", "cs"), ("Slovak", "slk_Latn", "sk"), ("Bulgarian", "bul_Cyrl", "bg"),
    ("Serbian", "srp_Cyrl", "sr"), ("Croatian", "hrv_Latn", "hr"), ("Bosnian", "bos_Latn", "bs"),
    ("Slovenian", "slv_Latn", "sl"), ("Macedonian", "mkd_Cyrl", None), ("Romanian", "ron_Latn", "ro"),
    ("Hungarian", "hun_Latn", "hu"), ("Finnish", "fin_Latn", "fi"), ("Estonian", "est_Latn", "et"),
    ("Latvian", "lvs_Latn", "lv"), ("Lithuanian", "lit_Latn", "lt"), ("Swedish", "swe_Latn", "sv"),
    ("Norwegian", "nob_Latn", ["no", "nb"]), ("Danish", "dan_Latn", "da"), ("Icelandic", "isl_Latn", "is"),
    ("Greek", "ell_Grek", "el"), ("Catalan", "cat_Latn", "ca"), ("Galician", "glg_Latn", "gl"),
    ("Basque", "eus_Latn", "eu"), ("Welsh", "cym_Latn", "cy"), ("Irish", "gle_Latn", None),
    ("Scots Gaelic", "gla_Latn", None), ("Maltese", "mlt_Latn", None), ("Albanian", "als_Latn", "sq"),
    ("Belarusian", "bel_Cyrl", None), ("Luxembourgish", "ltz_Latn", None), ("Esperanto", "epo_Latn", None),
    ("Yiddish", "ydd_Hebr", None),
    # ---- Africa ----
    ("Swahili", "swh_Latn", "sw"), ("Amharic", "amh_Ethi", "am"), ("Somali", "som_Latn", None),
    ("Hausa", "hau_Latn", "ha"), ("Yoruba", "yor_Latn", None), ("Igbo", "ibo_Latn", None),
    ("Zulu", "zul_Latn", None), ("Xhosa", "xho_Latn", None), ("Afrikaans", "afr_Latn", "af"),
    ("Sesotho", "sot_Latn", None), ("Shona", "sna_Latn", None), ("Kinyarwanda", "kin_Latn", None),
    ("Malagasy", "plt_Latn", None), ("Haitian Creole", "hat_Latn", None), ("Tigrinya", "tir_Ethi", None),
    ("Wolof", "wol_Latn", None), ("Lingala", "lin_Latn", None), ("Oromo", "gaz_Latn", None),
    ("Chichewa", "nya_Latn", None), ("Tswana", "tsn_Latn", None),
    # ---- Pacific / Americas ----
    ("Maori", "mri_Latn", None), ("Samoan", "smo_Latn", None), ("Fijian", "fij_Latn", None),
    ("Quechua", "quy_Latn", None),
]

LANG_TABLE = {name.lower(): (nllb, g) for name, nllb, g in LANGS}

# Agar IndicTrans2 live translation fail ho, to in Indian languages ke liye NLLB backup
INDIC_NLLB_BACKUP = {
    "hindi": "hin_Deva", "bengali": "ben_Beng", "tamil": "tam_Taml", "telugu": "tel_Telu",
    "marathi": "mar_Deva", "gujarati": "guj_Gujr", "kannada": "kan_Knda", "malayalam": "mal_Mlym",
    "punjabi": "pan_Guru", "urdu": "urd_Arab", "nepali": "npi_Deva", "odia": "ory_Orya",
    "assamese": "asm_Beng", "sindhi": "snd_Arab", "sanskrit": "san_Deva", "santali": "sat_Olck",
    "maithili": "mai_Deva", "kashmiri": "kas_Arab", "manipuri (meitei)": "mni_Beng",
}


def pick_gtts(candidates, gtts_ok):
    """gTTS ka valid language code chunta hai; na mile to None (audio nahi)."""
    if not candidates:
        return None
    if isinstance(candidates, str):
        candidates = [candidates]
    if gtts_ok is None:
        return candidates[0]
    for c in candidates:
        if c in gtts_ok:
            return c
    return None