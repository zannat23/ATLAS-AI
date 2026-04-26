from gtts import gTTS

# Create a Hindi test audio
tts = gTTS("मुझे पानी चाहिए", lang="hi")
tts.save("test.mp3")
print("test.mp3 created ✅")

# create_test_audios.py
from gtts import gTTS
import os

os.makedirs("tests/audio_samples", exist_ok=True)

samples = {
    "ar": ("أحتاج إلى ماء", "Arabic — I need water"),
    "fr": ("J'ai besoin d'eau", "French — I need water"),
    "bn": ("আমার পানি দরকার", "Bengali — I need water"),
    "ur": ("مجھے پانی چاہیے", "Urdu — I need water"),
    "en": ("I need water and food", "English"),
}

for lang, (text, label) in samples.items():
    filename = f"tests/audio_samples/test_{lang}.mp3"
    tts = gTTS(text=text, lang=lang, slow=False)
    tts.save(filename)
    print(f"✅ Created {filename} — {label}")

print("\nAll test audios created!")