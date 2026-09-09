from collectors import threatfox
from collectors import bazaar
from collectors import urlhaus
from process.threatnorm import normalize as norm_fox
from process.bazaarnorm import normalize as norm_baz
from process.urlnorm import normalize as norm_url
from process.deduplicate import deduplicating
from modeling.Indicator import Indicator
from modeling.observe import Observation
from enrichment.enrich import PyOTIEnricher
from analyze.score import ThreatAnalyzer
from storage.json_store import save_indicators

def run_pipeline():
    observations = []
    # 1. ThreatFox
    print("Collecting ThreatFox...")
    threatfox_response = threatfox.collect_ioc()

    for record in threatfox_response.get("data", []):
        observation = norm_fox(record)
        observations.append(observation)

    print(
        f"ThreatFox observations: "
        f"{len(observations)}"
    )
    # 2. URLhaus
    print("Collecting URLhaus...")
    urlhaus_response = urlhaus.collect_urls()
    urlhaus_records = urlhaus_response.get("urls", [])
    urlhaus_count = 0

    for record in urlhaus_records:
        observation = norm_url(record)
        observations.append(observation)
        urlhaus_count += 1

    print(
        f"URLhaus observations: "
        f"{urlhaus_count}"
    )
    # 3. MalwareBazaar
    print("Collecting MalwareBazaar...")
    malwarebazaar_response = (bazaar.collect_recent_samples())
    bazaar_count = 0

    for record in malwarebazaar_response.get("data", []):
        observation = norm_baz(record)
        observations.append(observation)
        bazaar_count += 1

    print(
        f"MalwareBazaar observations: "
        f"{bazaar_count}"
    )
    # 4. Deduplicate
    print("Deduplicating...")
    indicator_records = deduplicating(observations)
    # print("Enriching indicators with PyOTI...")
    # enricher = PyOTIEnricher()

    # for record in indicator_records:
    #     try:
    #         print(f"Enriching "
    #             f"{record.indicator.indicator_type}: "
    #             f"{record.indicator.value}"
    #         )
    #         enricher.enrich(record)
    #     except Exception as error:
    #         record.enrichment_status = "failed"
    #         record.enrichment = {"error": str(error)}

    # ANALYSIS
    analyzer = ThreatAnalyzer()
    for record in indicator_records:
        analyzer.analyze(record)

    save_indicators(indicator_records)
    print("Dun")

def print_summary(records):
    for record in records:
        indicator = record.indicator
        print(
            f"\n{indicator.indicator_type}: "
            f"{indicator.value}"
        )
        print(
            f"Observations: "
            f"{len(record.observations)}"
        )

        for observation in record.observations:
            print(
                f"  - {observation.source}"
            )

if __name__ == "__main__":
    records = run_pipeline()
    print(
        f"\nPipeline complete."
        f"\nIndicator records: {len(records)}"
    )
    print_summary(records)