from src.models import Incident, RuleMatch

def timeout_rule(incident: Incident) -> RuleMatch | None:
    message = incident.message.lower()

    if "timeout" in message:
        return RuleMatch(
            rule_name="timeout_rule",
            category="network",
            severity= "medium",
            probable_cause= "Network or service timeout",
            recommended_actions= [
                "Check service availability",
                "Review network latency",
                "Review recent deployments"
            ]
        )

    return None
