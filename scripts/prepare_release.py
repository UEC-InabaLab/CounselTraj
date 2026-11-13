#!/usr/bin/env python3
# SPDX-License-Identifier: Apache-2.0
"""Export all retained dialogues without raw seeds or provider envelopes."""
import argparse
from collections import Counter
from contextlib import ExitStack
import gzip
import hashlib
import json
from pathlib import Path
import re


SOURCES = {
    'SmileChat': ('smilechat_derived.jsonl.gz', 'CC0-1.0', 7672),
    'PsyDTCorpus': ('psydt_derived.jsonl.gz', 'Apache-2.0', 2595),
    'CPsyCounD': ('cpsycound_derived.jsonl.gz', 'CC-BY-SA-4.0', 697),
}
LINE = re.compile(r'^(client|counselor):\s*\[([^\]]+)\](.*)$')
ACT = re.compile(r'(client|counselor):\[([^\]]+)\]')
ROLES = {'client': 'user', 'counselor': 'assistant'}
SENSITIVE = {
    'email_like': re.compile(r'[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}'),
    'cn_mobile_like': re.compile(r'(?<!\d)1[3-9]\d{9}(?!\d)'),
    'cn_id_like': re.compile(r'(?<![\dA-Za-z])[1-9]\d{5}(?:19|20)\d{2}(?:0[1-9]|1[0-2])(?:0[1-9]|[12]\d|3[01])\d{3}[\dXx](?![\dA-Za-z])'),
    'credential_like': re.compile(r'\b(?:sk-[A-Za-z0-9_-]{24,}|hf_[A-Za-z0-9]{24,})\b'),
    'internal_path_like': re.compile(r'/(?:home|Users|shrdlu|data/shrdlu)/'),
}


def rows(path):
    with path.open(encoding='utf-8') as f:
        for line in f:
            if line.strip():
                yield json.loads(line)


def index_rows(path, key):
    result = {}
    for row in rows(path):
        value = row[key]
        if value in result:
            raise ValueError('Duplicate ' + key + ': ' + value)
        result[value] = row
    return result


def sha256(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for block in iter(lambda: f.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()


def extract_text(row):
    response = row.get('response', {})
    body = response.get('body', {})
    if row.get('error') or response.get('status_code') != 200 or body.get('error'):
        raise ValueError('Unsuccessful response: ' + row['custom_id'])
    if body.get('status') != 'completed':
        raise ValueError('Incomplete response: ' + row['custom_id'])
    if isinstance(body.get('output_text'), str):
        return body['output_text'].strip()
    chunks = [c['text'] for item in body.get('output', [])
              if item.get('type') == 'message'
              for c in item.get('content', [])
              if c.get('type') == 'output_text' and isinstance(c.get('text'), str)]
    if not chunks:
        raise ValueError('Empty output: ' + row['custom_id'])
    return '\n'.join(chunks).strip()


def parse_messages(text):
    result = []
    for line in text.splitlines():
        if not line.strip():
            continue
        match = LINE.fullmatch(line.strip())
        if not match:
            raise ValueError('Unrecognized dialogue line')
        speaker, act, content = match.groups()
        if not content.strip():
            raise ValueError('Empty utterance')
        result.append({'role': ROLES[speaker], 'dialogue_act': act,
                       'content': content.strip()})
    if not result:
        raise ValueError('Empty dialogue')
    return result


def parse_trajectory(text):
    matches = list(ACT.finditer(text))
    if not matches or ACT.sub('', text).strip():
        raise ValueError('Unrecognized planned trajectory')
    return [{'role': ROLES[m.group(1)], 'dialogue_act': m.group(2)} for m in matches]


def public_row(raw, meta):
    source = meta['source_dataset']
    if source not in SOURCES:
        raise ValueError('Unexpected source: ' + source)
    return {
        'id': raw['custom_id'],
        'source_dataset': source,
        'source_id': str(meta['source_id']),
        'topic': meta['topic'],
        'topic_zh': meta['topic_zh'],
        'license': SOURCES[source][1],
        'messages': parse_messages(extract_text(raw)),
        'planned_dialogue_acts': parse_trajectory(meta['tag_path']),
    }


def build(source_dir, release_dir, private_audit):
    data_dir = release_dir / 'data'
    data_dir.mkdir(parents=True, exist_ok=True)
    for name, _, _ in SOURCES.values():
        if (data_dir / name).exists():
            raise FileExistsError('Refusing to overwrite an existing release')
    metadata = index_rows(source_dir / 'metadata.jsonl', 'custom_id')
    seen = set()
    source_counts = Counter()
    topic_counts = Counter()
    model_counts = Counter()
    role_counts = Counter()
    sensitive = {name: [] for name in SENSITIVE}
    utterances = characters = mismatched_plan_lengths = 0
    with ExitStack() as stack:
        outputs = {}
        for source, (name, _, _) in SOURCES.items():
            raw_file = stack.enter_context((data_dir / name).open('xb'))
            outputs[source] = stack.enter_context(gzip.GzipFile(
                filename='', mode='wb', fileobj=raw_file, mtime=0, compresslevel=6))
        for raw in rows(source_dir / 'dialogues.jsonl'):
            ident = raw['custom_id']
            if ident in seen:
                raise ValueError('Duplicate dialogue: ' + ident)
            row = public_row(raw, metadata[ident])
            seen.add(ident)
            source = row['source_dataset']
            source_counts[source] += 1
            topic_counts[row['topic_zh']] += 1
            model_counts[raw['response']['body'].get('model', 'unspecified')] += 1
            utterances += len(row['messages'])
            role_counts.update(m['role'] for m in row['messages'])
            characters += sum(len(m['content']) for m in row['messages'])
            mismatched_plan_lengths += len(row['messages']) != len(row['planned_dialogue_acts'])
            for name, pattern in SENSITIVE.items():
                if any(pattern.search(m['content']) for m in row['messages']):
                    sensitive[name].append(ident)
            outputs[source].write((json.dumps(row, ensure_ascii=False, separators=(',', ':')) + '\n').encode('utf-8'))
    if seen != set(metadata) or len(seen) != 10964:
        raise ValueError('The release must contain all 10,964 original IDs')
    for source, (_, _, expected) in SOURCES.items():
        if source_counts[source] != expected:
            raise ValueError('Incorrect source count: ' + source)
    if utterances != 958791 or characters != 42197155:
        raise ValueError('Released utterances or text do not match existing dataset statistics')
    files = {}
    for source, (name, license_id, _) in SOURCES.items():
        path = data_dir / name
        if path.stat().st_size >= 50 * 1024 * 1024:
            raise ValueError('Compressed file unexpectedly exceeds 50 MiB')
        files[name] = {'source_dataset': source, 'license': license_id,
                       'dialogues': source_counts[source], 'bytes': path.stat().st_size,
                       'sha256': sha256(path)}
    report = {
        'dataset': 'CounselTrajD', 'version': '10964-20261113',
        'dialogues': len(seen), 'unique_ids': len(seen), 'utterances': utterances,
        'text_characters': characters, 'source_counts': dict(source_counts),
        'topic_counts': dict(topic_counts), 'role_counts': dict(role_counts),
        'generation_model_counts': dict(model_counts),
        'dialogues_with_plan_length_mismatch': mismatched_plan_lengths,
        'sensitive_pattern_flag_counts': {k: len(v) for k, v in sensitive.items()},
        'raw_seed_dialogues_included': False, 'provider_envelopes_included': False,
        'files': files,
    }
    (data_dir / 'manifest.json').write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    private_audit.parent.mkdir(parents=True, exist_ok=True)
    private_audit.write_text(json.dumps({
        'source_dir': str(source_dir), 'release_dir': str(release_dir),
        'sensitive_pattern_ids': sensitive,
        'source_file_sha256': {n: sha256(source_dir / n) for n in
                               ['dialogues.jsonl', 'metadata.jsonl']},
        'report': report,
    }, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if any(sensitive.values()):
        print('REVIEW_REQUIRED: inspect private audit before publishing; do not silently drop or redact records.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--source-dir', required=True, type=Path)
    parser.add_argument('--release-dir', required=True, type=Path)
    parser.add_argument('--private-audit', required=True, type=Path)
    args = parser.parse_args()
    build(args.source_dir, args.release_dir, args.private_audit)
