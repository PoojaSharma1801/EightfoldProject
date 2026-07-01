import re
from typing import List, Dict, Any
from .schema import canonical_empty
import phonenumbers


def _clean_email(e: str) -> str:
    return e.strip().lower()


def _normalize_phone(raw: str) -> str:
    if not raw:
        return None
    # remove common separators but keep leading +
    cleaned = re.sub(r"[^\d+]+", "", raw)
    try:
        pn = phonenumbers.parse(cleaned, None)
        if phonenumbers.is_valid_number(pn):
            return phonenumbers.format_number(pn, phonenumbers.PhoneNumberFormat.E164)
    except Exception:
        pass
    # fallback: digits only
    digits = re.sub(r"\D", "", raw)
    if len(digits) < 7:
        return None
    return digits


def extract_from_recruiter(row: Dict[str, Any]) -> Dict[str, Any]:
    r = row.get('raw', {})
    out = {}
    out['full_name'] = r.get('name') or r.get('full_name')
    emails = []
    if r.get('email'):
        emails = [_clean_email(r.get('email'))]
    out['emails'] = emails
    phones = []
    if r.get('phone'):
        p = _normalize_phone(r.get('phone'))
        if p:
            phones.append(p)
    out['phones'] = phones
    out['headline'] = r.get('title')
    out['links'] = {}
    out['skills'] = [s.strip() for s in (r.get('skills') or '').replace(';', ',').split(',') if s.strip()]
    return out


def extract_from_ats(row: Dict[str, Any]) -> Dict[str, Any]:
    r = row.get('raw', {})
    out = {}
    out['full_name'] = r.get('candidateName') or r.get('name')
    emails = []
    if r.get('emails'):
        if isinstance(r['emails'], list):
            emails = [_clean_email(e) for e in r['emails'] if e]
        else:
            emails = [_clean_email(r['emails'])]
    out['emails'] = emails
    phones = []
    if r.get('phone'):
        p = _normalize_phone(r.get('phone'))
        if p:
            phones.append(p)
    out['phones'] = phones
    out['skills'] = r.get('skills') or []
    out['headline'] = r.get('headline')
    return out


def extract_from_text(row: Dict[str, Any]) -> Dict[str, Any]:
    text = row.get('raw', {}).get('text', '')
    out = {}
    # emails
    emails = re.findall(r"[\w\.-]+@[\w\.-]+", text)
    out['emails'] = [_clean_email(e) for e in emails]

    # phones: find sequences that look like phone numbers, but filter year ranges
    phones = []
    phones_raw = re.findall(r"(\+?\d[\d\-\s\(\)\.]{6,}\d)", text)
    for p in phones_raw:
        if re.search(r"\b\d{4}\s*[-–—]\s*\d{4}\b", p):
            continue
        n = _normalize_phone(p)
        if n:
            phones.append(n)
    out['phones'] = phones

    # naive name heuristic: first capitalized two words near start
    m = re.search(r"^([A-Z][a-z]+\s+[A-Z][a-z]+)", text.strip())
    out['full_name'] = m.group(1) if m else None

    # skills: capture lines after 'Skills:' until a blank line or next header (e.g. 'Experience:')
    skills = []
    mpos = re.search(r"Skills\s*:\s*", text, re.IGNORECASE)
    if mpos:
        rest = text[mpos.end():]
        lines = rest.splitlines()
        skills_lines = []
        for line in lines:
            if not line.strip():
                break
            if re.match(r'^[A-Z][A-Za-z ]{0,30}:', line):
                break
            skills_lines.append(line)
        skills_text = ' '.join(skills_lines)
        skills = [s.strip() for s in re.split('[,;\n]', skills_text) if s.strip()]
    out['skills'] = skills
    return out


def project_sources(sources: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    mapped = []
    for s in sources:
        src = s.get('source')
        if src == 'recruiter_csv':
            data = extract_from_recruiter(s)
        elif src == 'ats_json':
            data = extract_from_ats(s)
        else:
            data = extract_from_text(s)
        mapped.append({'source': src, 'data': data})
    return mapped


def merge(mapped: List[Dict[str, Any]]) -> Dict[str, Any]:
    record = canonical_empty()
    provenance = []
    confidences = []
    for m in mapped:
        src = m['source']
        d = m['data']
        prov = {'source': src, 'fields': []}
        for k in ['full_name', 'emails', 'phones', 'headline', 'skills']:
            v = d.get(k)
            if v:
                if k in ['emails', 'phones', 'skills']:
                    existing = set(record.get(k) or [])
                    for item in v:
                        if item not in existing:
                            record[k].append(item)
                            existing.add(item)
                            prov['fields'].append(k)
                else:
                    if not record.get(k):
                        record[k] = v
                        prov['fields'].append(k)
        provenance.append(prov)
        confidences.append(0.8 if src == 'ats_json' else 0.6)
    if confidences:
        record['overall_confidence'] = sum(confidences) / len(confidences)
    record['provenance'] = provenance
    return record
