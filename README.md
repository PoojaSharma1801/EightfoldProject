# Multi-Source Candidate Data Transformer

This repository contains a small pipeline that ingests candidate data from multiple source types (CSV, ATS JSON, plain text), normalizes and merges values into a canonical profile, and emits schema-valid JSON with provenance and confidence.

## Quick start (Windows)

1. Create and activate a virtual environment:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

2. Install dependencies:

```powershell
pip install -r requirements.txt
```

3. Run the CLI on the provided samples and write `out.json`:

```powershell
python -m src.cli --inputs samples\recruiter.csv samples\ats.json samples\resume.txt --out out.json
```

4. Run tests:

```powershell
python -m pytest -q
```

## Files of interest

- `src/cli.py` — command-line entrypoint
- `src/transformer/schema.py` — canonical schema and empty record
- `src/transformer/ingest.py` — simple file ingestors (CSV, JSON, text)
- `src/transformer/merge.py` — extraction, normalization, merging, provenance
- `samples/` — example input files
- `out.json` — example output produced by the CLI

## Notes

- Phone numbers are normalized to E.164 when possible.
- Skills extraction is heuristic and reads lines after a `Skills:` header until a blank line or next header.
- This project is intentionally small and easy to extend.

## Submission

This repository is ready for submission with the required README file, sample inputs, working CLI, and tests.
