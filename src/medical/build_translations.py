"""
Ek baar chalane wali script: saare first-aid steps ko sab languages me translate karke
aur unki audio banakar cache/first_aid/ folder me save karti hai.
Uske baad medical.py bina kisi model ke, seedha cache se jawab deta hai (instant + offline).

Chalane ka tareeka (project ke root folder se, jahan app.py hai):

    python -m src.medical.build_translations --langs "Hindi,Tamil"     # kuch languages
    python -m src.medical.build_translations                           # saari languages
    python -m src.medical.build_translations --no-audio                # sirf text
    python -m src.medical.build_translations --template "Tulu"         # haath se translation ke liye khaali file
    python -m src.medical.build_translations --force-audio             # audio dobara banao (overrides ke baad)

Folder structure jo ban-ta hai:
    cache/first_aid/translations/<lang>.json   <- machine translation
    cache/first_aid/overrides/<lang>.json      <- tumhare/native speaker ke sudhare hue translations (ye jeette hain)
    cache/first_aid/audio/<lang>/<condition>.wav|mp3
"""
import argparse
import json
import os
import sys
import time

sys.path.append(".")

from src.medical.first_aid_kb import WOUND_FIRST_AID, SYMPTOM_GUIDES, ITEM_SUBSTITUTES
from src.medical import indic_support
from src.medical.lang_table import LANG_TABLE, INDIC_NLLB_BACKUP, slugify, pick_gtts

CACHE_DIR = os.path.join("cache", "first_aid")
TRANS_DIR = os.path.join(CACHE_DIR, "translations")
OVER_DIR = os.path.join(CACHE_DIR, "overrides")
AUDIO_DIR = os.path.join(CACHE_DIR, "audio")

# Classifier jin wound types ko pehchanta hai (normal me koi steps nahi hote)
PHOTO_CONDITIONS = ["bruise", "abrasion", "laceration", "puncture_wound", "burn"]
BATCH = 8


# ------------------------------------------------------------------
# Kya-kya translate karna hai
# ------------------------------------------------------------------
def all_strings(include_all: bool = False) -> list:
    """
    Default: sirf wo English sentences jo Medical page par dikhte hain
    (classifier ke 5 wound types ke steps + item notes).
    include_all=True: symptom guides aur baaki wound types bhi.
    """
    s = set()
    if include_all:
        for source in (WOUND_FIRST_AID, SYMPTOM_GUIDES):
            for entry in source.values():
                s.update(entry["steps"])
    else:
        for cond in PHOTO_CONDITIONS:
            if cond in WOUND_FIRST_AID:
                s.update(WOUND_FIRST_AID[cond]["steps"])
    # get_tailored_first_aid ke item notes (finite set: har item + har substitute)
    for item, subs in ITEM_SUBSTITUTES.items():
        s.add(f"You have {item} - use it directly.")
        for sub in subs:
            s.add(f"No {item}? You can use: {sub}.")
    return sorted(s)


def read_json(path):
    if not os.path.exists(path):
        return {}
    try:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"  ! {path} padh nahi paya: {e}")
        return {}


def write_json(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


# ------------------------------------------------------------------
# Translators
# ------------------------------------------------------------------
class NLLBTranslator:
    """Lazy-loaded NLLB (sirf zarurat padne par load hota hai)."""
    def __init__(self):
        self.ready = False

    def _load(self):
        import torch
        from transformers import AutoModelForSeq2SeqLM, AutoTokenizer
        self.torch = torch
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        name = "facebook/nllb-200-distilled-600M"
        print("Loading NLLB translator...")
        self.tok = AutoTokenizer.from_pretrained(name, src_lang="eng_Latn")
        self.model = AutoModelForSeq2SeqLM.from_pretrained(name).to(self.device).eval()
        self.ready = True

    def translate(self, texts, tgt_code):
        if not self.ready:
            self._load()
        out = []
        for i in range(0, len(texts), BATCH):
            enc = self.tok(texts[i:i + BATCH], return_tensors="pt", padding=True).to(self.device)
            with self.torch.no_grad():
                gen = self.model.generate(
                    **enc,
                    forced_bos_token_id=self.tok.convert_tokens_to_ids(tgt_code),
                    max_length=256, num_beams=4,
                )
            out += self.tok.batch_decode(gen, skip_special_tokens=True)
        return out


def translate_texts(key, texts, nllb):
    """key = lowercase language name. Indian (IndicTrans2) ya baaki (NLLB)."""
    if key in indic_support.INDIC_LANGS:
        if indic_support.indic_available():
            code, _ = indic_support.INDIC_LANGS[key]
            out = []
            for i in range(0, len(texts), BATCH):
                out += indic_support.translate_en_to_indic(texts[i:i + BATCH], code)
            return out
        # IndicTransToolkit nahi hai -> NLLB se karo (agar ye language NLLB me hai)
        if key in INDIC_NLLB_BACKUP:
            print("  (IndicTransToolkit nahi mila, NLLB use ho raha hai)")
            return nllb.translate(texts, INDIC_NLLB_BACKUP[key])
        raise RuntimeError(
            f"'{key}' ke liye IndicTransToolkit chahiye, aur NLLB ye language nahi jaanta. Skip kar rahe hain."
        )
    if key in LANG_TABLE:
        return nllb.translate(texts, LANG_TABLE[key][0])
    raise ValueError(f"Unknown language: {key}")


# ------------------------------------------------------------------
# Audio
# ------------------------------------------------------------------
def build_audio(key, slug, merged, conditions, force, gtts_ok):
    folder = os.path.join(AUDIO_DIR, slug)
    os.makedirs(folder, exist_ok=True)
    made = 0
    for cond in conditions:
        english_steps = WOUND_FIRST_AID[cond]["steps"]
        if not english_steps or not all(s in merged for s in english_steps):
            continue
        steps = [merged[s] for s in english_steps]

        wav = os.path.join(folder, f"{cond}.wav")
        mp3 = os.path.join(folder, f"{cond}.mp3")
        if force:
            for p in (wav, mp3):
                if os.path.exists(p):
                    os.remove(p)
        elif os.path.exists(wav) or os.path.exists(mp3):
            continue

        try:
            if key in indic_support.INDIC_LANGS:
                _, has_tts = indic_support.INDIC_LANGS[key]
                if has_tts and indic_support.USE_INDIC_TTS:
                    indic_support.indic_tts(steps, wav)
                    made += 1
                elif key == "punjabi" and (gtts_ok is None or "pa" in gtts_ok):
                    from gtts import gTTS
                    text = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(steps))
                    gTTS(text=text, lang="pa").save(mp3)
                    made += 1
                    time.sleep(1)
            elif key in LANG_TABLE:
                gcode = pick_gtts(LANG_TABLE[key][1], gtts_ok)
                if gcode:
                    from gtts import gTTS
                    text = "\n".join(f"{i + 1}. {t}" for i, t in enumerate(steps))
                    gTTS(text=text, lang=gcode).save(mp3)
                    made += 1
                    time.sleep(1)
        except Exception as e:
            print(f"  ! audio fail ({cond}): {e}")
    return made


# ------------------------------------------------------------------
# Ek language ka poora kaam
# ------------------------------------------------------------------
def build_language(key, strings, args, nllb, gtts_ok):
    slug = slugify(key)
    tpath = os.path.join(TRANS_DIR, f"{slug}.json")
    existing = {} if args.force else read_json(tpath)

    missing = [s for s in strings if s not in existing]
    if missing:
        print(f"  translating {len(missing)} sentences...")
        out = translate_texts(key, missing, nllb)
        existing.update(dict(zip(missing, out)))
        write_json(tpath, existing)
    else:
        print("  text cache already complete")

    if args.no_audio:
        return
    overrides = {k: v for k, v in read_json(os.path.join(OVER_DIR, f"{slug}.json")).items()
                 if isinstance(v, str) and v.strip()}
    merged = {**existing, **overrides}
    conditions = list(WOUND_FIRST_AID) if args.all_conditions else PHOTO_CONDITIONS
    conditions = [c for c in conditions if c in WOUND_FIRST_AID and WOUND_FIRST_AID[c]["steps"]]
    n = build_audio(key, slug, merged, conditions, args.force_audio or args.force, gtts_ok)
    print(f"  audio files made: {n}")


def write_template(name, strings):
    slug = slugify(name)
    path = os.path.join(OVER_DIR, f"{slug}.json")
    if os.path.exists(path):
        print(f"{path} pehle se hai, chhoda nahi.")
        return
    write_json(path, {s: "" for s in strings})
    print(f"Template ban gaya: {path}")
    print("Har English line ke saamne apna translation likho (khaali chhodo to skip hoga).")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--langs", default="all", help='comma-separated, jaise "Hindi,Tamil" ya "all"')
    ap.add_argument("--no-audio", action="store_true")
    ap.add_argument("--force", action="store_true", help="text + audio dobara banao")
    ap.add_argument("--force-audio", action="store_true", help="sirf audio dobara banao")
    ap.add_argument("--all-conditions", action="store_true",
                    help="saare conditions ki audio (default: sirf photo classifier wale)")
    ap.add_argument("--all-strings", action="store_true",
                    help="symptom guides + baaki wound types bhi translate karo (default: sirf Medical page wale)")
    ap.add_argument("--template", default=None, help='kisi language ke liye khaali overrides file banao, jaise "Tulu"')
    args = ap.parse_args()

    strings = all_strings(args.all_strings)
    print(f"Total unique English sentences: {len(strings)}")

    if args.template:
        write_template(args.template, strings)
        return

    if args.langs.strip().lower() == "all":
        keys = list(indic_support.INDIC_LANGS) + [k for k in LANG_TABLE if k not in indic_support.INDIC_LANGS]
    else:
        keys = [x.strip().lower() for x in args.langs.split(",") if x.strip()]

    try:
        from gtts.lang import tts_langs
        gtts_ok = set(tts_langs().keys())
    except Exception:
        gtts_ok = None

    nllb = NLLBTranslator()
    failed = []
    t_start = time.time()
    for n, key in enumerate(keys, 1):
        print(f"[{n}/{len(keys)}] {key}")
        t0 = time.time()
        try:
            build_language(key, strings, args, nllb, gtts_ok)
        except Exception as e:
            print(f"  ! FAILED: {e}")
            failed.append(key)
        took = time.time() - t0
        avg = (time.time() - t_start) / n
        eta_min = avg * (len(keys) - n) / 60
        print(f"  -> {took:.0f}s | andaza: ~{eta_min:.0f} min baaki")

    print("\nDone.")
    if failed:
        print("Ye languages fail hui (dobara try karo ya error mujhe bhejo):", ", ".join(failed))


if __name__ == "__main__":
    main()