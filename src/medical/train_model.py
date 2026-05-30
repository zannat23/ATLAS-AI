import torch
import torch.nn as nn
import torchvision
import torchvision.transforms as transforms
from torchvision import datasets, models
from torch.utils.data import DataLoader
import wandb
import os

# ── Config ────────────────────────────────────────
DEVICE      = "cuda" if torch.cuda.is_available() else "cpu"
CLASSES     = ['burn_mild','burn_severe','bruise',
               'infection','laceration','normal']
NUM_CLASSES = len(CLASSES)
BATCH_SIZE  = 32
EPOCHS      = 20
LR          = 0.001
DATA_DIR    = "data/processed/wounds"
MODEL_DIR   = "models"

print(f"Training on: {DEVICE}")
os.makedirs(MODEL_DIR, exist_ok=True)

# ── Data transforms ────────────────────────────────
train_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(
        brightness=0.3,
        contrast=0.3,
        saturation=0.2
    ),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

val_transforms = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.ToTensor(),
    transforms.Normalize(
        mean=[0.485, 0.456, 0.406],
        std=[0.229, 0.224, 0.225]
    )
])

# ── Load data ──────────────────────────────────────
train_dataset = datasets.ImageFolder(
    f"{DATA_DIR}/train",
    transform=train_transforms
)
val_dataset = datasets.ImageFolder(
    f"{DATA_DIR}/val",
    transform=val_transforms
)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
    num_workers=0
)
val_loader = DataLoader(
    val_dataset,
    batch_size=BATCH_SIZE,
    shuffle=False,
    num_workers=0
)

print(f"Train: {len(train_dataset)} images")
print(f"Val:   {len(val_dataset)} images")
print(f"Classes: {train_dataset.classes}")

# ── Model — EfficientNet-B0 ────────────────────────
model = models.efficientnet_b0(
    weights=models.EfficientNet_B0_Weights.IMAGENET1K_V1
)

# Replace final layer for our classes
model.classifier[1] = nn.Linear(
    model.classifier[1].in_features,
    NUM_CLASSES
)
model = model.to(DEVICE)

# ── Loss + Optimizer ───────────────────────────────
criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(
    model.parameters(),
    lr=LR,
    weight_decay=1e-4
)
scheduler = torch.optim.lr_scheduler.CosineAnnealingLR(
    optimizer,
    T_max=EPOCHS
)

# ── W&B tracking ───────────────────────────────────
wandb.init(
    project="atlas-medical",
    name="wound-classifier-v1",
    config={
        "epochs": EPOCHS,
        "batch_size": BATCH_SIZE,
        "lr": LR,
        "model": "efficientnet_b0"
    }
)

# ── Training loop ──────────────────────────────────
best_val_acc = 0.0

for epoch in range(EPOCHS):
    # Train
    model.train()
    train_loss, train_correct = 0, 0

    for images, labels in train_loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)
        optimizer.zero_grad()
        outputs = model(images)
        loss = criterion(outputs, labels)
        loss.backward()
        optimizer.step()
        train_loss    += loss.item()
        train_correct += (outputs.argmax(1) == labels).sum().item()

    # Validate
    model.eval()
    val_loss, val_correct = 0, 0

    with torch.no_grad():
        for images, labels in val_loader:
            images, labels = images.to(DEVICE), labels.to(DEVICE)
            outputs   = model(images)
            loss      = criterion(outputs, labels)
            val_loss     += loss.item()
            val_correct  += (outputs.argmax(1) == labels).sum().item()

    train_acc = train_correct / len(train_dataset)
    val_acc   = val_correct   / len(val_dataset)
    scheduler.step()

    print(f"Epoch {epoch+1:2d}/{EPOCHS} | "
          f"Train: {train_acc:.3f} | "
          f"Val: {val_acc:.3f}")

    wandb.log({
        "train_acc": train_acc,
        "val_acc":   val_acc,
        "train_loss": train_loss/len(train_loader),
        "val_loss":   val_loss/len(val_loader)
    })

    # Save best model
    if val_acc > best_val_acc:
        best_val_acc = val_acc
        torch.save({
            "model_state_dict": model.state_dict(),
            "classes":          CLASSES,
            "val_acc":          val_acc,
            "epoch":            epoch
        }, f"{MODEL_DIR}/wound_classifier_best.pth")
        print(f"   ✅ Best model saved! Val acc: {val_acc:.3f}")

wandb.finish()
print(f"\n🎉 Training complete!")
print(f"   Best val accuracy: {best_val_acc:.3f}")
print(f"   Model saved: models/wound_classifier_best.pth")