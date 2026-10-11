"""Integration tests against the real resources.db"""
from src.resource.locator import search_resources

def test_search_returns_results():
    results = search_resources(resource_type="hospital", limit=10)
    assert len(results) > 0

def test_search_respects_limit():
    results = search_resources(resource_type="hospital", limit=2)
    assert len(results) <= 2

def test_search_sorted_by_distance():
    results = search_resources(resource_type="hospital", limit=10)
    distances = [r["distance_km"] for r in results]
    assert distances == sorted(distances)

def test_search_filters_by_type():
    results = search_resources(resource_type="water", limit=10)
    assert all(r["type"] == "water" for r in results)

def test_search_by_query_keyword():
    results = search_resources(query="hospital", limit=5)
    assert len(results) > 0
