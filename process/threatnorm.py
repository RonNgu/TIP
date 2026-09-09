from modeling.Indicator import Indicator
from modeling.observe import Observation

def normalize(record: dict) -> Observation:
    indicator = Indicator(
        value=record["ioc"],
        indicator_type=record["ioc_type"],
    )

    observation = Observation(
        indicator=indicator,
        source="threatfox",
        source_id=str(record["id"]),
        first_seen=record.get("first_seen"),
        last_seen=record.get("last_seen"),
        confidence=record.get("confidence_level"),
        threat_type=record.get("threat_type"),
        malware_family=record.get("malware_printable"),
        raw_data=record,
    )
    return observation