from modeling.Indicator import Indicator
from modeling.observe import Observation

def normalize(record: dict) -> Observation:
    indicator = Indicator(
        value = record["sha256_hash"],
        indicator_type = "sha256_hash",
    )

    observation = Observation(
        indicator = indicator,
        source = "malwarebazaar",
        source_id=record["sha256_hash"],
        first_seen = record.get("first_seen"),
        last_seen = record.get("last_seen"),
        malware_family = record.get("signature"),
        raw_data = record,
    )
    return observation