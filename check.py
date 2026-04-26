import torch
import whisper
import transformers
import gradio
import tensorflow as tf

print("=" * 45)
print("      ATLAS — Final System Check")
print("=" * 45)
print(f"PyTorch       : {torch.__version__}")
print(f"Transformers  : {transformers.__version__}")
print(f"Gradio        : {gradio.__version__}")
print(f"TensorFlow    : {tf.__version__}")
print(f"Whisper       : OK")
print("-" * 45)
print(f"GPU Available : {torch.cuda.is_available()}")
print(f"GPU Name      : {torch.cuda.get_device_name(0)}")
mem = torch.cuda.get_device_properties(0).total_memory
print(f"GPU Memory    : {round(mem/1e9, 1)} GB")
print("=" * 45)
print("✅ ATLAS is ready to build!")