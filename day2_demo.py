import sys
sys.path.append(".")
from src.voice.pipeline import transcribe, translate, speak
import os

os.makedirs("outputs", exist_ok=True)

print("=" * 50)
print("       ATLAS — Day 2 Voice Demo")
print("=" * 50)

# Step 1: Transcribe
audio_file = "test.mp3"
print(f"\n🎤 Transcribing audio: {audio_file}")
result = transcribe(audio_file)

detected_lang = result["language"]
original_text = result["text"]
print(f"Detected Language : {detected_lang}")
print(f"Original Text     : {original_text}")

# Step 2: Translate to English
print(f"\n🔄 Translating to English...")
if detected_lang != "en":
    english_text = translate(original_text, src_lang=detected_lang, tgt_lang="eng_Latn")
else:
    english_text = original_text
print(f"English Text : {english_text}")

# Step 3: Translate response to Hindi
print(f"\n🔄 Translating response to Hindi...")
hindi_response = translate(
    f"I understand. You said: {english_text}. I am here to help.",
    src_lang="en",
    tgt_lang="hin_Deva"
)
print(f"Hindi Response : {hindi_response}")

# Step 4: Speak
print(f"\n🔊 Speaking response...")
speak(hindi_response, language="hi", filename="outputs/atlas_response.mp3")

print("\n" + "=" * 50)
print("✅ Day 2 Complete — Full voice pipeline working!")
print("=" * 50)