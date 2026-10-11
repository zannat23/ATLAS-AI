"""Evaluate wound classifier accuracy on the real validation set."""
import glob, json, os, time
from sklearn.metrics import classification_report, confusion_matrix
from src.medical.classifier import classify_wound, CLASSES

VAL_DIR = "data/processed/wounds/val"

def main():
    y_true, y_pred, records = [], [], []
    start = time.time()

    for cls in CLASSES:
        img_paths = glob.glob(os.path.join(VAL_DIR, cls, "*"))
        print(f"Evaluating class '{cls}' ({len(img_paths)} images)...")
        for path in img_paths:
            result = classify_wound(path)
            y_true.append(cls)
            y_pred.append(result["wound_type"])
            records.append({
                "image": path,
                "true_label": cls,
                "predicted": result["wound_type"],
                "confidence": result["confidence"],
                "correct": cls == result["wound_type"]
            })

    elapsed = time.time() - start
    accuracy = sum(r["correct"] for r in records) / len(records)
    report = classification_report(y_true, y_pred, labels=CLASSES, output_dict=True, zero_division=0)
    cm = confusion_matrix(y_true, y_pred, labels=CLASSES).tolist()

    os.makedirs("results", exist_ok=True)
    output = {
        "module": "medical_classifier",
        "total_images": len(records),
        "overall_accuracy": round(accuracy, 4),
        "eval_time_seconds": round(elapsed, 2),
        "classification_report": report,
        "confusion_matrix": {"labels": CLASSES, "matrix": cm},
        "per_image_results": records
    }
    with open("results/medical_eval.json", "w") as f:
        json.dump(output, f, indent=2)

    print("\n" + "="*50)
    print(f"MEDICAL CLASSIFIER — Overall Accuracy: {accuracy*100:.2f}%")
    print(f"Total images tested: {len(records)}")
    print(f"Eval time: {elapsed:.1f}s")
    print("="*50)
    print("\nPer-class precision/recall/f1:")
    for cls in CLASSES:
        r = report[cls]
        print(f"  {cls:15s} precision={r['precision']:.2f}  recall={r['recall']:.2f}  f1={r['f1-score']:.2f}")
    print("\nSaved full results to results/medical_eval.json")

if __name__ == "__main__":
    main()
