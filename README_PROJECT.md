# Multi-Source Candidate Data Transformer

This repository contains a small pipeline that ingests candidate data from multiple source types (CSV, ATS JSON, plain text), normalizes and merges values into a canonical profile, and emits schema-valid JSON with provenance and confidence.

Quick start (Windows)

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

4. Quick runner (prints basic verification):

```powershell
python run_tests.py
```

Run tests (cross-platform)

```bash
python -m pytest -q
```

Files of interest

- `src/cli.py` — command-line entrypoint
- `src/transformer/schema.py` — canonical schema and empty record
- `src/transformer/ingest.py` — simple file ingestors (CSV, JSON, text)
- `src/transformer/merge.py` — extraction, normalization, merging, provenance
- `samples/` — example input files
- `out.json` — example output produced by the CLI

Notes

- Phone numbers are normalized to E.164 when possible and filtered for obvious year ranges.
- Skills extraction is heuristic: it reads lines after a `Skills:` header until a blank line or next header.
- This is minimal, intentionally small, and easy to extend (PDF parsing, LinkedIn/GitHub scrapers, better NER) — see TODOs.

Next steps

- Improve parsers for PDFs and LinkedIn/GitHub profiles.
- Add more comprehensive tests and a small CI workflow.

Example output

Running the CLI on the sample inputs writes `out.json` at the project root. Example (trimmed):

```
{
	"full_name": "Alice Smith",
	"emails": ["alice.smith@example.com", "bob.jones@example.com"],
	"phones": ["+14155551234", "4155555678"],
	"skills": ["Python", "SQL", "Java", "Go", "Docker"],
	"overall_confidence": 0.65
}
```

Key files (quick reference)

- `src/cli.py` — command-line entrypoint
- `src/transformer/ingest.py` — CSV/JSON/text ingestors
- `src/transformer/merge.py` — extraction, normalization, merge logic
- `samples/` — example input files you can try
- `out.json` — produced by the CLI when you run the samples

If you'd like, I can also create a separate `README.md` at the repo root and add a short demo script/gif for your submission.
