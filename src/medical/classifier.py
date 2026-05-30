import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image
import numpy as np

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

CLASSES = ['bruise', 'burn_mild', 'burn_severe',
           'infection', 'laceration', 'normal']

SEVERITY = {
    'normal':      1,
    'bruise':      2,
    'burn_mild':   3,
    'laceration':  3,
    'infection':   4,
    'burn_severe': 5,
}

FIRST_AID = {
    'normal':      "No wound detected. You appear to be okay.",
    'bruise':      "Apply ice pack wrapped in cloth for 20 minutes. Elevate the area. Rest.",
    'burn_mild':   "Cool the burn under running water for 10 minutes. Do NOT use ice. Cover with clean cloth.",
    'burn_severe': "EMERGENCY! Do NOT remove clothing. Cover loosely. Seek medical help IMMEDIATELY.",
    'laceration':  "Apply firm pressure with clean cloth. Elevate above heart level. Seek medical help.",
    'infection':   "Clean gently with clean water. Do NOT squeeze. Seek medical help for antibiotics.",
}

# Load model
print("Loading wound classifier...")
model = models.efficientnet_b0(weights=None)
model.classifier[1] = nn.Linear(
    model.classifier[1].in_features, len(CLASSES))

checkpoint = torch.load(
    "models/wound_classifier_best.pth",
    map_location=DEVICE,
    weights_only=False
)
model.load_state_dict(checkpoint['model_state_dict'])
model = model.to(DEVICE)
model.eval()
print("Wound classifier loaded ✅")

transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

def classify_wound(image_path: str) -> dict:
    """Classify a wound image and return results."""
    img   = Image.open(image_path).convert('RGB')
    tensor = transform(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        output = model(tensor)
        probs  = torch.softmax(output, dim=1)[0]

    pred_idx    = probs.argmax().item()
    pred_class  = CLASSES[pred_idx]
    confidence  = float(probs[pred_idx])
    severity    = SEVERITY[pred_class]
    first_aid   = FIRST_AID[pred_class]

    return {
        "wound_type":  pred_class,
        "confidence":  round(confidence, 3),
        "severity":    severity,
        "first_aid":   first_aid,
        "all_probs":   {
            CLASSES[i]: round(float(probs[i]), 3)
            for i in range(len(CLASSES))
        }
    }

if __name__ == "__main__":
    import sys
    sys.path.append(".")
    print("\nTest classification:")
    from src.medical.create_dataset import create_synthetic_wound
    img = create_synthetic_wound('burn_mild')
    img.save("outputs/test_wound.jpg")
    result = classify_wound("outputs/test_wound.jpg")
    print(f"Wound type : {result['wound_type']}")
    print(f"Confidence : {result['confidence']}")
    print(f"Severity   : {result['severity']}/5")
    print(f"First aid  : {result['first_aid']}")