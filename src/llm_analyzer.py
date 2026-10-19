import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from src.models import Incident, IncidentAnalysis

load_dotenv()
api_key = os.getenv("OPEN_AI_API_KEY")

if not api_key:
    raise RuntimeError(
        "Openai apikey was not found."
    )

client = OpenAI(api_key=api_key)

def analyze_incident_with_llm(incident: Incident) -> IncidentAnalysis:
    """Analyze an incident using LLM via Openai API."""

    prompt = f"""
Analyze the following software incident.

Service: {incident.service}
Environment: {incident.environment}
Log level: {incident.level}
Timestamps: {incident.timestamp.isoformat()}
Message: {incident.message}

Return a JSON object with exactly these fields:
-categories: list of strings
-severity: one of "low", "medium", "high", "critical"
-probable_causes: list of strings
-recommended_actions: list of strings
-matched_rules: list of strings

Intructions:
-Identify plausible causes based on the available information.
-Recommend concrete diagnostic of remediation steps.
-Do not claim certainty when the evidence is insufficient.
-Use an empty list for "matched_rules" because this analysis
is produced by the LLM, not by the rule engine.
-Return only valid JSON.
"""

    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt,
        text={
            "format":{
                "type": "json_object"
            }
        }
    )

    output = response.output_text

    if not output:
        raise ValueError(
            "Openai returned an empty response. "
            f"Response status: {response.status}"
        )
    try:
        result = json.loads(output)
    except json.JSONDecodeError as exc:
        raise ValueError(
            f"Openai returned invalid JSON: {output!r}"
        ) from exc

    required_fields = {
        "categories",
        "severity",
        "probable_causes",
        "recommended_actions"
    }

    missing_fields = required_fields - result.keys()

    if missing_fields:
        raise ValueError(
            f"OpenAi response is missing fields:{missing_fields}"
        )

    valid_severities = {"low", "medium", "high", "critical"}

    if result["severity"] not in valid_severities:
        raise ValueError(
            f"Invalid severity returned by OpenAi: {result['severity']!r}"
        )


    return IncidentAnalysis(
        categories=result["categories"],
        severity=result["severity"],
        probable_causes=result["probable_causes"],
        recommended_actions=result["recommended_actions"],
        matched_rules=[],
    )