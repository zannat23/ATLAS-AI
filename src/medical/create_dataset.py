import os
import numpy as np
from PIL import Image, ImageDraw
import random

# Wound categories
CLASSES = [
    'laceration',
    'burn_mild',
    'burn_severe', 
    'bruise',
    'infection',
    'normal'
]

def create_synthetic_wound(wound_type, size=(224, 224)):
    """Create a synthetic wound image for training."""
    img = Image.new('RGB', size, color=(200, 150, 130))
    draw = ImageDraw.Draw(img)

    if wound_type == 'laceration':
        # Red cut line
        x1 = random.randint(50, 100)
        y1 = random.randint(80, 120)
        x2 = random.randint(130, 180)
        y2 = random.randint(100, 140)
        draw.line([x1,y1,x2,y2], fill=(180,20,20), width=random.randint(3,8))

    elif wound_type == 'burn_mild':
        # Pink/red patch
        cx, cy = random.randint(80,140), random.randint(80,140)
        r = random.randint(30,60)
        draw.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(220,100,80))

    elif wound_type == 'burn_severe':
        # Dark burn
        cx, cy = random.randint(80,140), random.randint(80,140)
        r = random.randint(40,70)
        draw.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(80,40,30))

    elif wound_type == 'bruise':
        # Purple patch
        cx, cy = random.randint(80,140), random.randint(80,140)
        r = random.randint(25,50)
        draw.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(100,60,140), outline=(80,40,120))

    elif wound_type == 'infection':
        # Yellow/green patch with redness
        cx, cy = random.randint(80,140), random.randint(80,140)
        r = random.randint(20,45)
        draw.ellipse([cx-r,cy-r,cx+r,cy+r], fill=(180,160,50))
        draw.ellipse([cx-r+5,cy-r+5,cx+r-5,cy+r-5], fill=(200,180,80))

    elif wound_type == 'normal':
        # Normal skin with slight variation
        noise = random.randint(-20,20)
        img = Image.new('RGB', size,
                        color=(200+noise, 150+noise, 130+noise))
        draw = ImageDraw.Draw(img)

    # Add noise
    img_array = np.array(img)
    noise = np.random.randint(-15, 15, img_array.shape, dtype=np.int16)
    img_array = np.clip(img_array.astype(np.int16) + noise, 0, 255).astype(np.uint8)
    return Image.fromarray(img_array)

def generate_dataset(samples_per_class=200):
    print("Generating synthetic wound dataset...")
    for split in ['train', 'val']:
        n = samples_per_class if split == 'train' else samples_per_class // 5
        for cls in CLASSES:
            path = f"data/processed/wounds/{split}/{cls}"
            os.makedirs(path, exist_ok=True)
            for i in range(n):
                img = create_synthetic_wound(cls)
                img.save(f"{path}/{cls}_{i:04d}.jpg")
        print(f"✅ {split} set created")

    total = len(CLASSES) * (samples_per_class + samples_per_class//5)
    print(f"\n✅ Dataset created!")
    print(f"   Classes: {CLASSES}")
    print(f"   Total images: {total}")

if __name__ == "__main__":
    generate_dataset(samples_per_class=200)