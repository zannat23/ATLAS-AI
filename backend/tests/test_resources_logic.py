"""Fast unit tests for resource-locator logic. No DB, no models."""
import math
from src.resource.locator import haversine, detect_intent

def test_haversine_same_point_is_zero():
    assert haversine(18.52, 73.85, 18.52, 73.85) == 0

def test_haversine_known_distance():
    # Pune to Mumbai is roughly 120-150 km
    d = haversine(18.5204, 73.8567, 19.0760, 72.8777)
    assert 100 < d < 170

def test_detect_intent_hospital():
    assert detect_intent("I am injured and need a doctor") == "hospital"

def test_detect_intent_water():
    assert detect_intent("I am thirsty, need drinking water") == "water"

def test_detect_intent_shelter():
    assert detect_intent("need a place to sleep tonight") == "shelter"

def test_detect_intent_food():
    assert detect_intent("I am hungry, need food") == "food"

def test_detect_intent_ngo():
    assert detect_intent("need support and aid") == "ngo"

def test_detect_intent_unrecognized_returns_none():
    assert detect_intent("random unrelated text") is None

def test_detect_intent_hindi_keyword():
    assert detect_intent("mujhe paani chahiye") == "water"
