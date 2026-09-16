from src.models import Incident, RuleMatch



def authentication_rule(incident: Incident) -> RuleMatch | None:
    message = incident.message.lower()

    if "authentication" in message or "login" in message:
        return RuleMatch(
            rule_name="authentication_rule",
            category="authentication",
            severity="medium",
            probable_cause="Authentication failure",
            recommended_actions=[
                "Check authentication service",
                "Review authentication logs",
                "Check recent configuration changes"
            ]
        )

    return None
