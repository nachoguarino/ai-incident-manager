from models import Incident,RuleMatch


def redis_rule(incident: Incident) -> RuleMatch | None:
    message = incident.message.lower()

    if "redis" in message:
        return RuleMatch(
            rule_name="redis_rule",
            category="cache",
            severity="high",
            probable_cause="Redis service issues",
            recommended_actions=[
                "Check Redis aviailability",
                "Review Redis logs",
                "Check Redis connection"
            ]
        )

    return None 


def database_rule(incident: Incident) -> RuleMatch | None:
    message = incident.message.lower()

    if "databese" in message or "connection" in message:
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
                "Check recent deployments"
            ]
        )

    return None
