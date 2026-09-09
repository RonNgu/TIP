from modeling.records import IndicatorRecord
from modeling.observe import Observation

def deduplicating(observations: list[Observation]) -> list[IndicatorRecord]:
    indicators = {}
    seen_observations = set()

    for observation in observations:
        # Remove exact source duplicates
        if observation.source_id:
            observation_key = (observation.source, observation.source_id)
            if observation_key in seen_observations:
                continue
            seen_observations.add(observation_key)

        # Group by indicator
        indicator = observation.indicator
        value = (indicator.normalized_value or indicator.value)

        indicator_key = (indicator.indicator_type, value)
        # Create IndicatorRecord
        if indicator_key not in indicators:
            indicators[indicator_key] = (IndicatorRecord(indicator=indicator))
        indicators[indicator_key].observations.append(observation)

    return list(indicators.values())