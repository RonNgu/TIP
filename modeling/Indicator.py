from dataclasses import dataclass
from typing import Optional

@dataclass
class Indicator:
    value: str
    indicator_type: Optional[str] = None
    normalized_value: Optional[str] = None
    first_seen: Optional[str] = None
    last_seen: Optional[str] = None

    def __init__(
        self,
        value: str,
        indicator_type: Optional[str] = None,
        normalized_value: Optional[str] = None,
        first_seen: Optional[str] = None,
        last_seen: Optional[str] = None,
        type: Optional[str] = None,
    ):
        if indicator_type is None:
            indicator_type = type
        if indicator_type is None:
            raise TypeError("Indicator requires an indicator_type or type")

        self.value = value
        self.indicator_type = indicator_type
        self.normalized_value = normalized_value
        self.first_seen = first_seen
        self.last_seen = last_seen

    @property
    def type(self):
        return self.indicator_type

    @type.setter
    def type(self, value):
        self.indicator_type = value