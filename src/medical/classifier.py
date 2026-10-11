import torch
import torch.nn as nn
import torchvision.transforms as transforms
import torchvision.models as models
from PIL import Image

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

CLASSES = ['normal', 'bruise', 'abrasion', 'laceration', 'puncture_wound', 'burn']

from src.medical.first_aid_kb import WOUND_FIRST_AID, get_tailored_first_aid

SEVERITY = {k: WOUND_FIRST_AID[k]['severity'] for k in CLASSES}
FIRST_AID = {k: WOUND_FIRST_AID[k]['summary'] for k in CLASSES}

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
print("Wound classifier loaded")

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
    img = Image.open(image_path).convert('RGB')
    tensor = transform(img).unsqueeze(0).to(DEVICE)

    with torch.no_grad():
        output = model(tensor)
        probs = torch.softmax(output, dim=1)[0]

    pred_idx = probs.argmax().item()
    pred_class = CLASSES[pred_idx]
    confidence = float(probs[pred_idx])
    severity = SEVERITY[pred_class]

    tailored = get_tailored_first_aid(pred_class, is_symptom_guide=False)

    return {
        "wound_type": pred_class,
        "confidence": round(confidence, 3),
        "severity": severity,
        "first_aid": tailored["steps"],
        "all_probs": {
            CLASSES[i]: round(float(probs[i]), 3)
            for i in range(len(CLASSES))
        }
    }

if __name__ == "__main__":
    import sys
    sys.path.append(".")
    print("\nTest classification:")
    result = classify_wound("outputs/test_wound.jpg")
    print(f"Wound type : {result['wound_type']}")
    print(f"Confidence : {result['confidence']}")
    print(f"Severity   : {result['severity']}/5")
    print(f"First aid  : {result['first_aid']}")