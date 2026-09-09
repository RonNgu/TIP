from modeling.Indicator import Indicator
from modeling.observe import Observation

def normalize(record: dict) -> Observation:
    indicator = Indicator(
        value=record["url"],
        indicator_type="url",
    )

    observation = Observation(
        indicator=indicator,
        source="urlhaus",
        source_id=str(record["id"]),
        first_seen=record.get("date_added"),
        threat_type=record.get("threat"),
        raw_data=record,
    )
    return observation