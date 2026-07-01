import os
from tempfile import NamedTemporaryFile

from src.cli import run
from src.transformer.ingest import ingest_file


def test_pipeline_samples():
    inputs = [
        'samples/recruiter.csv',
        'samples/ats.json',
        'samples/resume.txt',
    ]
    result = run(inputs)
    assert 'emails' in result
    assert isinstance(result['emails'], list)
    assert any('alice.smith' in e for e in result['emails'])
    assert 'phones' in result
    assert result['overall_confidence'] > 0


def test_pdf_ingestion():
    with NamedTemporaryFile('wb', suffix='.pdf', delete=False) as fh:
        fh.write(b'%PDF-1.4\n%binary payload\x00\xff\xfeAlice Smith\nEmail: alice.smith@example.com\n')
        path = fh.name

    try:
        rows = ingest_file(path)
        assert rows
        text = rows[0]['raw']['text']
        assert 'Alice Smith' in text
        assert 'alice.smith@example.com' in text
    finally:
        if os.path.exists(path):
            os.unlink(path)
