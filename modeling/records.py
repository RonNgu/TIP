from dataclasses import dataclass, field
from modeling.Indicator import Indicator
from modeling.observe import Observation

@dataclass
class IndicatorRecord:
    indicator: Indicator
    observations: list[Observation] = field(default_factory=list)
    enrichment: dict = field(default_factory=dict)
    analysis: dict = field(default_factory=dict)