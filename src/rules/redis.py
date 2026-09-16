from src.models import Incident, RuleMatch

def redis_rule(incident: Incident) -> RuleMatch | None:
    message = incident.message.lower()

    if "redis" in message:
        return RuleMatch(
            rule_name="redis_rule",
            category="cache",
            severity="high",
            probable_cause="Redis service issues",
            recommended_actions=[
                "Check Redis availability",
                "Review Redis logs",
                "Check Redis connection"
            ]
        )

    return None 