from src.cli import run


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
