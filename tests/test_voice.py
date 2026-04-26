import sys
sys.path.append(".")
from src.voice.pipeline import transcribe

# Test with our audio file
result = transcribe("test.mp3")

print("=" * 40)
print("WHISPER RESULT")
print("=" * 40)
print(f"Detected Language : {result['language']}")
print(f"Transcribed Text  : {result['text']}")
print("=" * 40)