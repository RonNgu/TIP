from dataclasses import dataclass
from typing import Optional

@dataclass
class Indicator:
    value: str
    indicator_type: str
    normalized_value: Optional[str] = None
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None