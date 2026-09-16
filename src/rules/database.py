from src.models import Incident, RuleMatch


def database_rule(incident: Incident) -> RuleMatch | None:
    message = incident.message.lower()

    if "database" in message or "connection" in message:
        return RuleMatch(
            rule_name="database_rule",
            category="database",
            severity="high",
            probable_cause="Database connection issues",
            recommended_actions=[
                "Check database availability",
                "Check database connection pool",
                "Review recent deployments"
            ]
        )

    return None