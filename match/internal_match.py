class InternalRelevanceMatcher:
    def __init__(self, sightings):
        self.sightings = sightings

    def match(self, record):
        indicator_value = record.indicator.value.lower()
        matches = []

        for sighting in self.sightings:
            sighting_value = sighting["value"].lower()
            if indicator_value == sighting_value:
                matches.append(sighting)

        hosts = list({
            match.get("host")
            for match in matches
            if match.get("host")
        })
        return {
            "observed": len(matches) > 0,
            "hit_count": len(matches),
            "hosts": hosts
        }