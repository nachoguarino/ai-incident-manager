from dataclasses import dataclass
from datetime import datetime

@dataclass
class Incident:
    service: str
    environment: str
    level: str
    message: str
    timestamp: datetime

@dataclass
class IncidentAnalysis:
    categories: list[str]
    severity: str
    probable_causes: list[str]
    recommended_actions: list[str]
    matched_rules: list[str]

@dataclass
class RuleMatch:
    rule_name: str
    category: str
    severity: str
    probable_cause: str
    recommended_actions: list[str]