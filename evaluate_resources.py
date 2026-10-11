"""Evaluate detect_intent accuracy on a labeled query set."""
import json, os
from src.resource.locator import detect_intent, search_resources

TEST_QUERIES = [
    ("I am injured and need a doctor", "hospital"),
    ("Someone is hurt, need medical help", "hospital"),
    ("There is a clinic nearby?", "hospital"),
    ("I need drinking water", "water"),
    ("I am so thirsty", "water"),
    ("mujhe paani chahiye", "water"),
    ("Where can I sleep tonight", "shelter"),
    ("I need a place to stay", "shelter"),
    ("Is there a camp nearby", "shelter"),
    ("I am hungry, need food", "food"),
    ("Where can I get a meal", "food"),
    ("mujhe khana chahiye", "food"),
    ("I need support and aid", "ngo"),
    ("Which NGO can help me", "ngo"),
    ("mujhe sahayata chahiye", "ngo"),
    ("Just saying hello", None),
    ("What is the weather today", None),
]

def main():
    records = []
    for query, expected in TEST_QUERIES:
        detected = detect_intent(query)
        records.append({
            "query": query,
            "expected": expected,
            "detected": detected,
            "correct": detected == expected
        })

    accuracy = sum(r["correct"] for r in records) / len(records)

    os.makedirs("results", exist_ok=True)
    output = {
        "module": "resource_intent_detection",
        "total_queries": len(records),
        "accuracy": round(accuracy, 4),
        "results": records
    }
    with open("results/resources_eval.json", "w") as f:
        json.dump(output, f, indent=2)

    print("="*50)
    print(f"RESOURCE INTENT DETECTION — Accuracy: {accuracy*100:.1f}%")
    print("="*50)
    for r in records:
        mark = "OK" if r["correct"] else "WRONG"
        print(f"[{mark}] '{r['query']}' -> expected={r['expected']} detected={r['detected']}")

    print("\nSaved full results to results/resources_eval.json")

if __name__ == "__main__":
    main()
