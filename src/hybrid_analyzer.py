import logging

from src.analyzer import analyze_incident
from src.llm_analyzer import analyze_incident_with_llm
from src.models import Incident, IncidentAnalysis


logger = logging.getLogger(__name__)

SEVERITY_PRIORITY = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4
}

def merge_unique (first: list[str], second: list[str]) -> list [str]:
    """Merge two lists while preserving order and removing duplicates."""
    return list(dict.fromkeys(first + second))

def analyze_incident_hybrid(incident: Incident) -> IncidentAnalysis:
    """Combine rule-based analysis with LLM analysis."""

    rule_analysis = analyze_incident(incident)

    try:
        llm_analysis = analyze_incident_with_llm(incident)
    except Exception:
        logger.exception(
            "LLM analysis failed. Falling back to rule-based analysis."
        )
        return rule_analysis

    # If no rule matched, use the LLM categories instead of "unknown".
    if rule_analysis.categories == ["unknown"]:
        categories = list(dict.fromkeys(llm_analysis.categories))
    else:
        categories = merge_unique(
            rule_analysis.categories,
            llm_analysis.categories
        )

    # Ignore generic fallback information when no rule matched.
    has_rule_matches = rule_analysis.categories != ["unknown"]

    rule_causes = (
        rule_analysis.probable_causes if has_rule_matches else []
    )
    rule_actions = (
        rule_analysis.recommended_actions if has_rule_matches else []
    )

    probable_causes = merge_unique(
        rule_causes,
        llm_analysis.probable_causes,
    )
    recommended_actions = merge_unique(
        rule_actions,
        llm_analysis.recommended_actions,
    )


    highest_severity = max(
        [rule_analysis.severity, llm_analysis.severity],
        key=lambda severity: SEVERITY_PRIORITY[severity]
    )

    return IncidentAnalysis(
        categories=categories,
        severity=highest_severity,
        probable_causes=probable_causes,
        recommended_actions=recommended_actions,
        matched_rules=rule_analysis.matched_rules
    )
