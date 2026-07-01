import csv
import json
from typing import List, Dict, Any


def read_recruiter_csv(path: str) -> List[Dict[str, Any]]:
    out = []
    with open(path, newline='', encoding='utf-8') as fh:
        reader = csv.DictReader(fh)
        for row in reader:
            out.append({"source": "recruiter_csv", "raw": row})
    return out


def read_ats_json(path: str) -> List[Dict[str, Any]]:
    with open(path, encoding='utf-8') as fh:
        blob = json.load(fh)
    rows = blob if isinstance(blob, list) else [blob]
    return [{"source": "ats_json", "raw": r} for r in rows]


def read_text_resume(path: str) -> List[Dict[str, Any]]:
    with open(path, encoding='utf-8') as fh:
        text = fh.read()
    return [{"source": "resume_text", "raw": {"text": text}}]


def ingest_file(path: str) -> List[Dict[str, Any]]:
    if path.lower().endswith('.csv'):
        return read_recruiter_csv(path)
    if path.lower().endswith('.json'):
        return read_ats_json(path)
    if path.lower().endswith('.txt') or path.lower().endswith('.pdf'):
        return read_text_resume(path)
    try:
        return read_ats_json(path)
    except Exception:
        return read_text_resume(path)
