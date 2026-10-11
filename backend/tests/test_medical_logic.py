"""Structural sanity tests for the wound classifier (loads real model once)."""
import pytest
import glob

@pytest.fixture(scope="session")
def sample_image():
    imgs = glob.glob("data/processed/wounds/val/burn_mild/*")
    assert imgs, "No validation images found for burn_mild"
    return imgs[0]

def test_classify_output_structure(sample_image):
    from src.medical.classifier import classify_wound, CLASSES
    result = classify_wound(sample_image)
    assert result["wound_type"] in CLASSES
    assert 0.0 <= result["confidence"] <= 1.0
    assert 1 <= result["severity"] <= 5
    assert isinstance(result["first_aid"], str) and len(result["first_aid"]) > 0
    assert set(result["all_probs"].keys()) == set(CLASSES)

def test_all_probs_sum_to_one(sample_image):
    from src.medical.classifier import classify_wound
    result = classify_wound(sample_image)
    total = sum(result["all_probs"].values())
    assert 0.98 <= total <= 1.02
