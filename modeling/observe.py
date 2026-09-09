from dataclasses import dataclass
from typing import Any, Optional
from modeling.Indicator import Indicator

@dataclass
class Observation:
    indicator: Indicator
    source: str
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None
    confidence: Optional[int] = None
    threat_type: Optional[str] = None
    malware_family: Optional[str] = None
    source_id: Optional[str] = None
    status: Optional[str] = None
    raw_data: Optional[dict[str, Any]] = None