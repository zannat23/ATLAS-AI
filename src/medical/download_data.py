import os
import urllib.request
import zipfile

os.makedirs("data/raw/wounds", exist_ok=True)
os.makedirs("data/processed/wounds/train", exist_ok=True)
os.makedirs("data/processed/wounds/val", exist_ok=True)

# Download from public medical image sources
datasets = {
    "burn":      "https://storage.googleapis.com/mediapipe-models/image_classifier/efficientnet_lite0/float32/1/efficientnet_lite0.tflite",
}

print("Downloading wound dataset...")
print("Please go to: https://www.kaggle.com/datasets/truthisneverlinear/wound-classification")
print("Download and extract to: data/raw/wounds/")
print("\nOr we can use synthetic data for now!")