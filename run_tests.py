import sys
from src.cli import run


def main():
    inputs = [
        'samples/recruiter.csv',
        'samples/ats.json',
        'samples/resume.txt',
    ]
    res = run(inputs)
    print('RESULT_KEYS:', list(res.keys()))
    print('EMAILS:', res.get('emails'))
    if not res.get('emails'):
        print('ERROR: no emails extracted')
        sys.exit(2)
    print('OK')


if __name__ == '__main__':
    main()
