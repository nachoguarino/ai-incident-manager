from src.models import Incident, IncidentAnalysis

from src.rules import (
    database_rule,
    authentication_rule,
    timeout_rule, 
    redis_rule
)

RULES = [
    database_rule,
    authentication_rule,
    timeout_rule,
    redis_rule
]

SEVERITY_PRIORITY = {
    "low": 1,
    "medium": 2,
    "high": 3,
    "critical": 4
}


def combine_actions(matches):
    actions = []

    for match in matches:
        for action in match.recommended_actions:
            if action not in actions:
                actions.append(action)

    return actions


def analyze_incident(incident: Incident) -> IncidentAnalysis:

    matches = []

    for rule in RULES:
        result = rule(incident)

        if result is not None:
            matches.append(result)

    if not matches:
        return IncidentAnalysis(
            categories=["unknown"],
            severity="low",
            probable_causes=["Unable to determine cause"],
            recommended_actions=[
                "Review application logs",
                "Investigate incident manually",
                "Cry for your system administrator"
            ],
            matched_rules=[]
        )

    categories = list({
        match.category for match in matches
    })

    probable_causes = [
        match.probable_cause for match in matches
    ]

    recommended_actions = combine_actions(matches)

    highest_severity = max(
        matches,
        key=lambda match: SEVERITY_PRIORITY[match.severity]
    ).severity

    matched_rules = [
        match.rule_name
        for match in matches
    ]

    return IncidentAnalysis(
        categories=categories,
        severity=highest_severity,
        probable_causes=probable_causes,
        recommended_actions=recommended_actions,
        matched_rules=matched_rules
    )


