# CounselTrajD Data Card

## Contents

The three `*_derived.jsonl.gz` files contain all 10,964 retained dialogues, without
resampling or filtering by downstream model performance. Each gzip stream stores
one UTF-8 JSON object per line. Counts and SHA256 checksums are in `manifest.json`.

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
| `quality_score` | Automated strict evaluator overall score |
| `quality_recommendation` | Original automated `keep` or `review` recommendation |

`user` corresponds to the original `client` speaker, and `assistant` corresponds
to `counselor`. Dialogues can begin with an assistant greeting. The export preserves
all utterances, their order, and dialogue-act tags. It does not force alternation,
truncate to the planned trajectory, or silently correct generated content.
Planned and realized trajectories are separate fields and need not coincide.
In this release, 114 dialogues have different planned and realized trajectory
lengths. They are retained without truncation or silent repair.

The export removes the API wrapper and strips only outer whitespace following the
original dataset's statistics parser. It does not include the original
`short_dialogue`, internal filenames, absolute paths, request IDs, billing, usage,
or API response metadata.

## Construction and selection

The retained set follows the project's existing strict-quality selection, not a
new quality threshold selected for publication:

1. Start from 14,106 dialogues after the existing online/initial-consultation filters.
2. Score with the existing GPT-5.4-nano strict evaluator.
3. Retain dialogues with an overall score of at least 72.
4. Remove 200 score-72 entries from overrepresented topics, leaving 10,964.

The automated score ranges from 72 to 90, with mean 77.71. The original evaluator
recommended `keep` for 1,045 and `review` for 9,919. Those labels are retained;
`review` is not presented as manual approval. No new generations or paid
evaluations are part of this packaging step.

## Licensing and responsible interpretation

See `../LICENSING.md` and `../THIRD_PARTY_NOTICES.md`. The data files do not inherit
the code license. The release is synthetic research material, not validated
clinical advice. Automated pattern checks are not a substitute for privacy,
clinical safety, or rights review. Removing the seed field is not a claim that
generated text has no relationship to its source.
