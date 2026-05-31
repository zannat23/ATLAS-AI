import sqlite3
import math

DB_PATH = "data/resources.db"

def haversine(lat1, lon1, lat2, lon2):
    """Calculate distance in km between two coordinates."""
    R = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (math.sin(dlat/2)**2 +
         math.cos(math.radians(lat1)) *
         math.cos(math.radians(lat2)) *
         math.sin(dlon/2)**2)
    return R * 2 * math.asin(math.sqrt(a))

def search_resources(
    resource_type: str = None,
    query: str = None,
    lat: float = 18.5204,
    lon: float = 73.8567,
    limit: int = 5
) -> list:
    """Search resources by type or keyword, sorted by distance."""
    conn   = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if resource_type:
        cursor.execute(
            "SELECT * FROM resources WHERE type=?",
            (resource_type,)
        )
    elif query:
        cursor.execute(
            """SELECT * FROM resources WHERE
               name LIKE ? OR type LIKE ? OR description LIKE ?""",
            (f"%{query}%", f"%{query}%", f"%{query}%")
        )
    else:
        cursor.execute("SELECT * FROM resources")

    rows = cursor.fetchall()
    conn.close()

    results = []
    for row in rows:
        id_, name, rtype, rlat, rlon, address, phone, desc, city = row
        distance = haversine(lat, lon, rlat, rlon)
        results.append({
            "id":          id_,
            "name":        name,
            "type":        rtype,
            "lat":         rlat,
            "lon":         rlon,
            "address":     address,
            "phone":       phone,
            "description": desc,
            "city":        city,
            "distance_km": round(distance, 2)
        })

    # Sort by distance
    results.sort(key=lambda x: x["distance_km"])
    return results[:limit]

def detect_intent(query: str) -> str:
    """Detect resource type from natural language query."""
    query = query.lower()
    if any(w in query for w in
           ["hospital","doctor","medical","hurt","injured","pain","clinic"]):
        return "hospital"
    elif any(w in query for w in
             ["water","paani","पानी","drinking","thirsty"]):
        return "water"
    elif any(w in query for w in
             ["shelter","sleep","stay","camp","raat","रात","house"]):
        return "shelter"
    elif any(w in query for w in
             ["food","khana","खाना","eat","hungry","meal","bhook"]):
        return "food"
    elif any(w in query for w in
             ["ngo","help","support","aid","sahayata","सहायता"]):
        return "ngo"
    return None

if __name__ == "__main__":
    # Test
    print("Testing resource locator...\n")
    results = search_resources(resource_type="hospital", limit=3)
    for r in results:
        print(f"🏥 {r['name']} — {r['distance_km']} km")
        print(f"   📍 {r['address']}")
        print(f"   📞 {r['phone']}\n")