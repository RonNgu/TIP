class VendorMatcher:
    def __init__(self, vendors):
        self.vendors = vendors

    def match(self, record):
        matches = []

        value = record.indicator.value.lower()
        indicator_type = str(
            record.indicator.indicator_type
            or record.indicator.type
        ).lower()

        for vendor in self.vendors:
            if indicator_type == "domain":
                for domain in vendor["domains"]:
                    domain = domain.lower()

                    if value == domain or value.endswith("." + domain):
                        matches.append({
                            "vendor": vendor["name"],
                            "relationship": "infrastructure_match"
                        })
            elif indicator_type == "url":
                for domain in vendor["domains"]:
                    domain = domain.lower()

                    if self._url_matches_domain(value, domain):
                        matches.append({
                            "vendor": vendor["name"],
                            "relationship": "infrastructure_match"
                        })
        return matches

    def _url_matches_domain(self, url, domain):
        return (
            f"://{domain}/" in url
            or f"://{domain}:" in url
            or f".{domain}/" in url
            or f".{domain}:" in url
        )