import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://mb-api.abuse.ch/api/v1/"
API_KEY = os.getenv("MALWAREBAZAAR_API_KEY")
RAW_DATA_DIR = Path("data/raw/malwarebazaar")

def collect_recent_samples():
    if not API_KEY:
        raise RuntimeError("MALWAREBAZAAR_API_KEY is not set")

    payload = {
        "query": "get_recent",
        "selector": "time"
    }

    response = requests.post(
        url,
        headers = {"Auth-Key": API_KEY},
        data=payload,
        timeout=30
    )

    response.raise_for_status()
    return response.json()

def save_raw(data):
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
    output_file = RAW_DATA_DIR / f"{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    return output_file

if __name__ == "__main__":
    data = collect_recent_samples()
    output_file = save_raw(data)
    print("MalwareBazaar collection successful.")
    print(f"Saved raw response to: {output_file}")
    if data.get("query_status") == "ok":
        print(f"Samples received: {len(data.get('data', []))}")