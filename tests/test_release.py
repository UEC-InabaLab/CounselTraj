# SPDX-License-Identifier: Apache-2.0
import gzip
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


def module(name):
    spec = importlib.util.spec_from_file_location(name, ROOT / 'scripts' / (name + '.py'))
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


class ExportTests(unittest.TestCase):
    def test_parse_roles_and_preserve_content(self):
        m = module('prepare_release')
        result = m.parse_messages('counselor:[Greeting]Hello.\nclient:[Greeting]Hi.')
        self.assertEqual(result[0], {'role': 'assistant', 'dialogue_act': 'Greeting', 'content': 'Hello.'})
        self.assertEqual(result[1]['role'], 'user')

    def test_bad_lines_and_empty_outputs_fail(self):
        m = module('prepare_release')
        for text in ['', 'not a tagged dialogue', 'client:[Greeting]']:
            with self.assertRaises(ValueError):
                m.parse_messages(text)

    def test_trajectory_and_format_validation(self):
        m = module('prepare_release')
        self.assertEqual(len(m.parse_trajectory('counselor:[Greeting] client:[Greeting]')), 2)
        with self.assertRaises(ValueError):
            m.parse_trajectory('unexpected counselor:[Greeting]')

    def test_private_fields_are_not_exported(self):
        m = module('prepare_release')
        raw = {'custom_id': 'example', 'error': None, 'response': {'status_code': 200,
               'request_id': 'private', 'body': {'status': 'completed', 'error': None,
               'output_text': 'client:[Greeting]Hello.'}}}
        meta = {'source_dataset': 'SmileChat', 'source_id': '42', 'topic': 'other',
                'topic_zh': 'other', 'tag_path': 'client:[Greeting]',
                'short_dialogue': 'PRIVATE SEED', 'source_file': '/home/private'}
        row = m.public_row(raw, meta, {'overall_score': 75, 'recommendation': 'review'})
        self.assertEqual(set(row), module('load_counseltraj').FIELDS)
        text = json.dumps(row)
        self.assertNotIn('PRIVATE SEED', text)
        self.assertNotIn('/home/private', text)
        self.assertNotIn('request_id', text)

    def test_loader_checks_files_and_unique_ids(self):
        m = module('load_counseltraj')
        with tempfile.TemporaryDirectory() as temp:
            d = Path(temp)
            row = {'id': 'example', 'source_dataset': 'SmileChat', 'source_id': '42',
                   'topic': 'other', 'topic_zh': 'other', 'license': 'CC0-1.0',
                   'messages': [{'role': 'user', 'content': 'Hello.', 'dialogue_act': 'Greeting'}],
                   'planned_dialogue_acts': [], 'quality_score': 75, 'quality_recommendation': 'review'}
            p = d / 'example.jsonl.gz'
            with gzip.open(p, 'wt', encoding='utf-8') as f:
                f.write(json.dumps(row) + '\n')
            import hashlib
            manifest = {'source_counts': {'SmileChat': 1}, 'dialogues': 1, 'utterances': 1,
                        'files': {p.name: {'source_dataset': 'SmileChat', 'bytes': p.stat().st_size,
                        'sha256': hashlib.sha256(p.read_bytes()).hexdigest()}}}
            (d / 'manifest.json').write_text(json.dumps(manifest))
            self.assertTrue(m.verify(d)['verified'])
            p.write_bytes(b'corrupted')
            with self.assertRaises(ValueError):
                m.verify(d)


if __name__ == '__main__':
    unittest.main()
