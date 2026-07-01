import argparse
import json
from typing import List
from src.transformer.ingest import ingest_file
from src.transformer.merge import project_sources, merge


def run(inputs: List[str]) -> dict:
    all_sources = []
    for p in inputs:
        all_sources.extend(ingest_file(p))
    mapped = project_sources(all_sources)
    result = merge(mapped)
    return result


def main():
    p = argparse.ArgumentParser()
    p.add_argument('--inputs', '-i', nargs='+', required=True)
    p.add_argument('--out', '-o', default='out.json')
    args = p.parse_args()
    res = run(args.inputs)
    with open(args.out, 'w', encoding='utf-8') as fh:
        json.dump(res, fh, indent=2, ensure_ascii=False)
    print('Wrote', args.out)


if __name__ == '__main__':
    main()
