from typing import Dict, Any

CANONICAL_FIELDS: Dict[str, str] = {
    "candidate_id": "string",
    "full_name": "string",
    "emails": "string[]",
    "phones": "string[]",
    "location": "object",
    "links": "object",
    "headline": "string|null",
    "years_experience": "number|null",
    "skills": "array",
    "experience": "array",
    "education": "array",
    "provenance": "array",
    "overall_confidence": "number",
}


def canonical_empty() -> Dict[str, Any]:
    return {
        "candidate_id": None,
        "full_name": None,
        "emails": [],
        "phones": [],
        "location": {"city": None, "region": None, "country": None},
        "links": {},
        "headline": None,
        "years_experience": None,
        "skills": [],
        "experience": [],
        "education": [],
        "provenance": [],
        "overall_confidence": 0.0,
    }
