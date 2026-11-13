#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Stream source-specific CounselTrajD files and verify the release manifest."""
import argparse
from collections import Counter
import gzip
import hashlib
import json
from pathlib import Path


FIELDS = {'id', 'source_dataset', 'source_id', 'topic', 'topic_zh', 'license',
          'messages', 'planned_dialogue_acts'}


def load_dialogues(data_dir, source=None):
    data_dir = Path(data_dir)
    manifest = json.loads((data_dir / 'manifest.json').read_text(encoding='utf-8'))
    if source is not None and source not in manifest['source_counts']:
        raise ValueError('Unknown source: ' + source)
    for filename, info in manifest['files'].items():
        if source is not None and info['source_dataset'] != source:
            continue
        if Path(filename).name != filename:
            raise ValueError('Unsafe manifest filename')
        with gzip.open(data_dir / filename, 'rt', encoding='utf-8') as f:
            for line in f:
                yield json.loads(line)


def verify(data_dir):
    data_dir = Path(data_dir)
    manifest = json.loads((data_dir / 'manifest.json').read_text(encoding='utf-8'))
    for filename, info in manifest['files'].items():
        if Path(filename).name != filename:
            raise ValueError('Unsafe manifest filename')
        path = data_dir / filename
        h = hashlib.sha256()
        with path.open('rb') as f:
            for block in iter(lambda: f.read(1024 * 1024), b''):
                h.update(block)
        if h.hexdigest() != info['sha256'] or path.stat().st_size != info['bytes']:
            raise ValueError('Checksum or size mismatch: ' + filename)
    counts = Counter()
    seen = set()
    utterances = 0
    for row in load_dialogues(data_dir):
        if set(row) != FIELDS or row['id'] in seen:
            raise ValueError('Schema or duplicate ID error')
        seen.add(row['id'])
        counts[row['source_dataset']] += 1
        utterances += len(row['messages'])
        for message in row['messages']:
            if set(message) != {'role', 'dialogue_act', 'content'}:
                raise ValueError('Unexpected message fields')
            if message['role'] not in ['user', 'assistant'] or not message['content']:
                raise ValueError('Invalid role or empty utterance')
    if dict(counts) != manifest['source_counts'] or len(seen) != manifest['dialogues']:
        raise ValueError('Dialogue count mismatch')
    if utterances != manifest['utterances']:
        raise ValueError('Utterance count mismatch')
    result = {'dialogues': len(seen), 'unique_ids': len(seen),
              'utterances': utterances, 'source_counts': dict(counts), 'verified': True}
    print(json.dumps(result, indent=2))
    return result


if __name__ == '__main__':
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--data-dir', type=Path, default=Path(__file__).resolve().parents[1] / 'data')
    args = p.parse_args()
    verify(args.data_dir)
