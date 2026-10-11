"""
Cache me kharab translations dhoondhta hai aur sirf unhe theek karta hai.

Kharab = khaali / missing, ya ek hi shabd baar-baar repeat ("masagi masagi masagi ...").
Aise sentences ko NLLB se dobara translate karta hai (repeat rokne wali settings ke saath).
Jo phir bhi theek na ho, wo cache se hata deta hai (taaki gadbad text na dikhe).
Jis language me kuch badla, sirf uski audio dobara banti hai.

Chalane ka tareeka (project ke root se, jahan app.py hai):

    python -m src.medical.fix_translations --dry-run       # sirf report, kuch badalta nahi
    python -m src.medical.fix_translations                 # theek karo + audio dobara banao
    python -m src.medical.fix_translations --langs "Manipuri (Meitei),Kashmiri"
    python -m src.medical.fix_translations --no-audio
"""
import argparse
import glob
import os
import re
import sys
import time
from collections import Counter

sys.path.append(".")

from src.medical import build_translations as bt
from src.medical import indic_support
from src.medical.lang_table import LANG_TABLE, INDIC_NLLB_BACKUP, slugify

# Repeat rokne wali settings, ek ke baad ek try hoti hain
CONFIGS = [
    dict(num_beams=5, no_repeat_ngram_size=3, repetition_penalty=1.2),
    dict(num_beams=5, no_repeat_ngram_size=2, repetition_penalty=1.5),
    dict(num_beams=4, no_repeat_ngram_size=4, repetition_penalty=1.3, length_penalty=0.6),
    dict(num_beams=1, do_sample=True, top_p=0.9, temperature=0.7,
         no_repeat_ngram_size=3, repetition_penalty=1.3),
    dict(num_beams=1, do_sample=True, top_p=0.9, temperature=0.9,
         no_repeat_ngram_size=3, repetition_penalty=1.3),
    dict(num_beams=1, do_sample=True, top_p=0.85, temperature=1.0,
         no_repeat_ngram_size=2, repetition_penalty=1.5),
]


def is_degenerate(text, en=""):
    """True agar translation khaali hai ya repeat-loop me phansi hai."""
    if not isinstance(text, str) or not text.strip():
        return True
    toks = text.split()
    if len(toks) >= 8:
        if max(Counter(toks).values()) >= 6 and max(Counter(toks).values()) / len(toks) > 0.3:
            return True
    run = 1
    for a, b in zip(toks, toks[1:]):
        run = run + 1 if a == b else 1
        if run >= 4:
            return True
    # bina space wali languages (Chinese, Japanese...) me chhota hissa baar-baar
    if re.search(r"(.{2,12}?)\1{5,}", text, flags=re.S):
        return True
    # English se bahut zyada lamba
    if en and len(text) > 4 * len(en) + 60:
        return True
    return False


def nllb_code_for(key):
    if key in INDIC_NLLB_BACKUP:
        return INDIC_NLLB_BACKUP[key]
    if key in LANG_TABLE:
        return LANG_TABLE[key][0]
    return None


def regenerate(nllb, text, code):
    """Ek sentence ko alag-alag settings se tab tak translate karo jab tak theek na aaye."""
    if not nllb.ready:
        nllb._load()
    enc = nllb.tok([text], return_tensors="pt").to(nllb.device)
    max_new = min(200, len(text.split()) * 4 + 20)
    for cfg in CONFIGS:
        try:
            with nllb.torch.no_grad():
                out = nllb.model.generate(
                    **enc,
                    forced_bos_token_id=nllb.tok.convert_tokens_to_ids(code),
                    max_new_tokens=max_new, **cfg,
                )
            cand = nllb.tok.batch_decode(out, skip_special_tokens=True)[0]
        except Exception as e:
            print(f"      ! generate error: {e}")
            continue
        if not is_degenerate(cand, text):
            return cand
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--langs", default="all", help='jaise "Kashmiri,Manipuri (Meitei)" ya "all"')
    ap.add_argument("--dry-run", action="store_true", help="sirf report, kuch badlo mat")
    ap.add_argument("--no-audio", action="store_true", help="audio dobara mat banao")
    args = ap.parse_args()

    strings = bt.all_strings(False)
    slug_to_key = {slugify(k): k for k in list(indic_support.INDIC_LANGS) + list(LANG_TABLE)}

    files = sorted(glob.glob(os.path.join(bt.TRANS_DIR, "*.json")))
    if args.langs.strip().lower() != "all":
        wanted = {slugify(x) for x in args.langs.split(",") if x.strip()}
        files = [f for f in files if os.path.splitext(os.path.basename(f))[0] in wanted]

    try:
        from gtts.lang import tts_langs
        gtts_ok = set(tts_langs().keys())
    except Exception:
        gtts_ok = None

    nllb = bt.NLLBTranslator()
    conditions = [c for c in bt.PHOTO_CONDITIONS
                  if c in bt.WOUND_FIRST_AID and bt.WOUND_FIRST_AID[c]["steps"]]

    total_bad = total_fixed = total_removed = 0
    affected = []
    t0 = time.time()
    for path in files:
        slug = os.path.splitext(os.path.basename(path))[0]
        key = slug_to_key.get(slug)
        if not key:
            continue
        data = bt.read_json(path)
        overrides = {k: v for k, v in bt.read_json(os.path.join(bt.OVER_DIR, f"{slug}.json")).items()
                     if isinstance(v, str) and v.strip()}
        bad = [s for s in strings if s not in overrides and (s not in data or is_degenerate(data[s], s))]
        total_bad += len(bad)
        if not bad:
            continue

        print(f"[{slug}] {len(bad)} kharab / {len(strings)}")
        if args.dry_run:
            for s in bad[:3]:
                shown = data.get(s, "(missing)")
                print(f"    - {shown[:70]!r}")
            continue

        code = nllb_code_for(key)
        if not code:
            print("    NLLB code nahi mila, skip")
            continue

        fixed = removed = 0
        for s in bad:
            new = regenerate(nllb, s, code)
            if new:
                data[s] = new
                fixed += 1
            else:
                data.pop(s, None)
                removed += 1
        bt.write_json(path, data)
        total_fixed += fixed
        total_removed += removed
        print(f"    theek kiye: {fixed}, hata diye (English dikhega): {removed}")

        if not args.no_audio:
            folder = os.path.join(bt.AUDIO_DIR, slug)
            if os.path.isdir(folder):
                for fn in os.listdir(folder):
                    if fn.endswith((".wav", ".mp3")):
                        os.remove(os.path.join(folder, fn))
            merged = {**data, **overrides}
            n = bt.build_audio(key, slug, merged, conditions, True, gtts_ok)
            print(f"    audio dobara bani: {n}")
        affected.append(slug)

    print("\n--- Summary ---")
    print(f"Kharab sentences mile: {total_bad}")
    if args.dry_run:
        print("(dry-run: kuch badla nahi gaya. Theek karne ke liye bina --dry-run ke chalao.)")
    else:
        print(f"Theek kiye: {total_fixed} | Hata diye: {total_removed}")
        print("Languages jisme kuch badla:", ", ".join(affected) if affected else "koi nahi")
    print(f"Time: {(time.time() - t0) / 60:.1f} min")


if __name__ == "__main__":
    main()