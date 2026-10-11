"""
Splits a flat per-class dataset (dataset/<class>/*.jpg) into
data/processed/wounds/train/<class>/ and .../val/<class>/ (80/20 split),
which is the structure train_model.py expects.
"""
import os
import shutil
import random

SOURCE_DIR = "dataset"
DEST_DIR = "data/processed/wounds"
VAL_SPLIT = 0.2
SEED = 42

random.seed(SEED)

classes = [d for d in os.listdir(SOURCE_DIR) if os.path.isdir(os.path.join(SOURCE_DIR, d))]
print(f"Found classes: {classes}")

for cls in classes:
    src_folder = os.path.join(SOURCE_DIR, cls)
    images = [f for f in os.listdir(src_folder) if f.lower().endswith((".jpg", ".jpeg", ".png"))]
    random.shuffle(images)

    split_idx = int(len(images) * (1 - VAL_SPLIT))
    train_images = images[:split_idx]
    val_images = images[split_idx:]

    train_dest = os.path.join(DEST_DIR, "train", cls)
    val_dest = os.path.join(DEST_DIR, "val", cls)
    os.makedirs(train_dest, exist_ok=True)
    os.makedirs(val_dest, exist_ok=True)

    for img in train_images:
        shutil.copy2(os.path.join(src_folder, img), os.path.join(train_dest, img))
    for img in val_images:
        shutil.copy2(os.path.join(src_folder, img), os.path.join(val_dest, img))

    print(f"{cls}: {len(train_images)} train, {len(val_images)} val")

print("\nDone. Data ready at:", DEST_DIR)