# CounselTrajD Data Card

📄 **Paper:** [CounselTraj (arXiv:2611.24168)](https://arxiv.org/abs/2611.24168)

📦 **Download:** [Hugging Face dataset](https://huggingface.co/datasets/UEC-InabaLab/CounselTrajD)

## Contents

The three `*_derived.jsonl.gz` files contain all 10,964 dialogues. Each gzip stream
stores one UTF-8 JSON object per line. Counts and SHA256 checksums are in
`manifest.json`.

The mean dialogue length is 87.45 individual utterances (not 87.45 client/counselor
pairs). The complete release contains 473,910 user utterances and 484,881 assistant
utterances, with 42,197,155 text characters excluding speaker and tag markup.

## Schema

| Field | Meaning |
| --- | --- |
| `id` | Stable unique CounselTrajD identifier |
| `source_dataset` | Source of the seed conversation |
| `source_id` | Original source record identifier |
| `topic`, `topic_zh` | Topic labels |
| `license` | Source-specific release license identifier |
| `messages` | Ordered generated utterances; keys are `role`, `dialogue_act`, and `content` |
| `planned_dialogue_acts` | Intended ordered trajectory; keys are `role` and `dialogue_act` |

`user` corresponds to the original `client` speaker, and `assistant` corresponds
to `counselor`. Dialogues can begin with an assistant greeting. The export preserves
all utterances, their order, and dialogue-act tags. It does not force alternation,
truncate to the planned trajectory, or silently correct generated content.
The message-level `dialogue_act` values are tags emitted during generation.
They are stored separately from the planned trajectory and are not guaranteed
to align with it one-to-one.
See [dialogue acts and trajectories](../README.md#dialogue-acts) for the role-specific
tag definitions and an illustrative trajectory segment.
In this release, 114 dialogues have different planned and realized trajectory
lengths. They are retained without truncation or silent repair.

The export removes the API wrapper and strips only outer whitespace following the
original dataset's statistics parser. It does not include the original
`short_dialogue`, internal filenames, absolute paths, request IDs, billing, usage,
or API response metadata.

## Licensing and responsible interpretation

See `../LICENSING.md` and `../THIRD_PARTY_NOTICES.md`. The data files do not inherit
the code license. The release is synthetic research material, not validated
clinical advice. Automated pattern checks are not a substitute for privacy,
clinical safety, or rights review. Removing the seed field is not a claim that
generated text has no relationship to its source.
