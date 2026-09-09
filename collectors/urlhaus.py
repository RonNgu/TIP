import json
import os
from datetime import datetime, timezone
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

url = "https://urlhaus-api.abuse.ch/v1/urls/recent/"
API_KEY = os.getenv("URLHAUS_API_KEY")
RAW_DATA_DIR = Path("data/raw/urlhaus")

def collect_urls():
    if not API_KEY:
        raise RuntimeError("URLHAUS_API_KEY is not set")

    new_url = url  # No need to format with API_KEY

    response = requests.get(
        new_url,
        headers={"Auth-Key": API_KEY},
        timeout=60
    )

    response.raise_for_status()
    return response.json()

def save_raw(data):
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime(
        "%Y%m%d_%H%M%S"
    )

    output_file = RAW_DATA_DIR / f"{timestamp}.json"

    with open(output_file, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2)

    return output_file


if __name__ == "__main__":
    data = collect_urls()
    output_file = save_raw(data)
    print("URLhaus collection successful.")
    print(f"Saved raw response to: {output_file}")

# def collect_url():
#     if not API_KEY:
#         raise RuntimeError("URLHAUS_API_KEY is not set")

#     response = requests.get(
#         url,
#         headers={"Auth-Key": API_KEY},
#         timeout=60
#     )

#     response.raise_for_status()
#     save_raw(response.content)
#     return parse_csv(response.text)

# def parse_csv(csv_data: str) -> list[dict]:
#     lines = [
#         line
#         for line in csv_data.splitlines()
#         if not line.startswith("#")
#     ]

#     reader = csv.DictReader(lines)
#     return list(reader)

# def save_raw(data: bytes):
#     RAW_DATA_DIR.mkdir(
#         parents=True,
#         exist_ok=True
#     )

#     timestamp = datetime.now(
#         timezone.utc
#     ).strftime("%Y%m%d_%H%M%S")

#     output_file = (
#         RAW_DATA_DIR /
#         f"{timestamp}.csv"
#     )

#     with open(output_file, "wb") as file:
#         file.write(data)

#     return output_file

# if __name__ == "__main__":
#     data = collect_url()
#     output_file = save_raw(data)
#     print("URLhaus collection successful.")
#     print(f"Saved raw response to: {output_file}")