import json
from dataclasses import asdict
from pathlib import Path
from modeling.records import IndicatorRecord

OUTPUT_FILE = Path("data/processed/indicators.json")

def save_indicators(records: list[IndicatorRecord]):

    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    data = [
        asdict(record)
        for record in records
    ]

    with open(OUTPUT_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=2, ensure_ascii=False)