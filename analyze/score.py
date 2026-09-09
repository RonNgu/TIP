from modeling.records import IndicatorRecord

class ThreatAnalyzer:
    def analyze(self, record: IndicatorRecord) -> IndicatorRecord:
        score = 0
        reasons = []
        
        # 1. Multiple CTI sources
        source_count = len(record.observations)
        if source_count >= 2:
            score += 30
            reasons.append("Indicator observed by multiple CTI sources")
        elif source_count == 1:
            score += 10
            reasons.append("Indicator observed by one CTI source")

        # 2. ThreatFox confidence
        for observation in record.observations:
            if observation.confidence is not None:
                if observation.confidence >= 90:
                    score += 30
                    reasons.append("High-confidence ThreatFox observation")
                elif observation.confidence >= 50:
                    score += 15
                    reasons.append("Medium-confidence ThreatFox observation")

        # 3. Malware association
        for observation in record.observations:
            if observation.malware_family:
                score += 20
                reasons.append(
                    f"Associated with malware: "
                    f"{observation.malware_family}"
                )

        # 4. Cap score
        score = min(score, 100)

        # 5. Determine severity
        if score >= 70:
            severity = "high"
        elif score >= 40:
            severity = "medium"
        else:
            severity = "low"

        # 6. Store analysis
        record.analysis = {
            "score": score,
            "severity": severity,
            "reasons": reasons
        }
        return record