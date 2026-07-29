import urllib.request
import urllib.error
import json

base_url = "http://127.0.0.1:8000/api/v1/terrain/value"

test_coords = [
    ("Jammu (Valid)", 32.7266, 74.8570),
    ("Ramban (Valid)", 33.2450, 75.2410),
    ("Outside J&K (Bounds error)", 10.0, 10.0),
    ("Outside UT inside viewport", 31.5, 74.0),
    ("Edge of bounds", 32.0, 73.0),
    ("High altitude NoData candidate", 35.8, 76.8),
]

for name, lat, lon in test_coords:
    url = f"{base_url}?lat={lat}&lon={lon}"
    try:
        req = urllib.request.urlopen(url)
        data = json.loads(req.read().decode('utf-8'))
        print(f"[{name}] HTTP {req.status} OK: {data}")
    except urllib.error.HTTPError as e:
        body = e.read().decode('utf-8')
        print(f"[{name}] HTTP {e.code} Error: {body}")
    except Exception as e:
        print(f"[{name}] Connection Error: {e}")
