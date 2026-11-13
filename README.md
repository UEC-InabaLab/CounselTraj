# CounselTraj

## CounselTrajD

CounselTrajD contains **10,964 synthetic Chinese counseling dialogues** with
utterance-level dialogue-act annotations and planned dialogue-act trajectories.
The complete release contains **958,791 utterances** across 15 topic categories.
These are generated expansions conditioned on source conversations, not newly
collected human counseling sessions.

| Source of seed conversations | Dialogues | Data terms |
| --- | ---: | --- |
| SmileChat | 7,672 | CC0-1.0; see source notices |
| PsyDTCorpus | 2,595 | Apache-2.0; retain applicable notices |
| CPsyCounD | 697 | CC-BY-SA-4.0; see source notices |
| **Total** | **10,964** | **Source-specific terms, not a single blanket license** |

The three losslessly compressed JSONL files together form one dataset. They are
separated by provenance to make attribution and licensing explicit. Raw seed
conversation text, provider API envelopes, billing information, and internal file
paths are not included.

### Download and verify

After obtaining this repository, run with Python 3.8 or newer:

```bash
python3 scripts/load_counseltraj.py
python3 -m unittest discover -s tests -v
```

The loader verifies file checksums, unique IDs, record counts, and utterance counts.
It uses only the Python standard library. For programmatic streaming:

```python
from scripts.load_counseltraj import load_dialogues

for dialogue in load_dialogues("data"):
    messages = dialogue["messages"]
```

See [the data card](data/README.md) for the schema and dataset details,
[source notices](THIRD_PARTY_NOTICES.md) for attribution, and
[licensing scope](LICENSING.md) for the code/data distinction.

### Limitations

This dataset is not a substitute for professional diagnosis, treatment, or safety
evaluation. Synthetic generation and omission of seed fields do not establish
that every utterance is anonymous; automated pattern screening is only a limited
check.

No model weights, benchmark test answers, or private training infrastructure are
included in this data release.

### Citation

If you use CounselTraj in your research, please cite:

```bibtex
@inproceedings{qi-inaba-2027-counseltraj,
    title = "{CounselTraj}: Synthesizing Process-Aware Psychological Counseling Dialogues via Dialogue-Act Trajectory Planning",
    author = "Qi, Zhiyang and Inaba, Michimasa",
    booktitle = "Proceedings of the 20th Conference of the European Chapter of the Association for Computational Linguistics",
    year = "2027",
}
```
