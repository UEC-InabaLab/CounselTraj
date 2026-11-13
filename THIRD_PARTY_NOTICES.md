# Third-Party Data Notices

CounselTrajD is generated using seed conversations from the following datasets.
The source dataset names and original record identifiers are retained for
provenance; raw source conversations are not included in this release.

## SmileChat: 7,672 derived dialogues

- Creators: Huachuan Qiu, Hongliang He, Shuai Zhang, Anqi Li, and Zhenzhong Lan.
- Source: https://github.com/qiuhuachuan/smile
- Source license: https://github.com/qiuhuachuan/smile/blob/main/LICENSE (CC0-1.0).
- Paper: https://aclanthology.org/2024.findings-emnlp.34/
- Changes: source conversations conditioned dialogue-act trajectory generation
  and long-dialogue expansion; generated utterances and trajectories were
  extracted into the public JSONL schema. These are not original SmileChat rows.
- The paper's Data Sharing section additionally describes research-purpose
  release. The CC0 repository label is not represented as a separate warranty
  that all possible rights or uses have been cleared.

## PsyDTCorpus: 2,595 derived dialogues

- Creators: Haojie Xie, Yirong Chen, Xiaofen Xing, Jingkai Lin, and Xiangmin Xu.
- Source: https://modelscope.cn/datasets/YIRONGCHEN/PsyDTCorpus
- Direct dataset license metadata:
  https://modelscope.cn/api/v1/datasets/YIRONGCHEN/PsyDTCorpus (Apache License 2.0).
- Official project and license: https://github.com/scutcyr/SoulChat2.0
- Paper: https://aclanthology.org/2025.acl-long.55/
- Changes: source conversations conditioned dialogue-act trajectory generation
  and long-dialogue expansion; generated utterances and trajectories were
  extracted into the public JSONL schema. These are not original PsyDTCorpus rows.
- Preserve applicable copyright, attribution, and NOTICE information under
  Apache-2.0. The model-use statements in the project README do not relicense the
  model weights under this data release.

## CPsyCounD: 697 derived dialogues

- Creators: Chenhao Zhang and the CPsyCoun project authors.
- Source: https://huggingface.co/datasets/CAS-SIAT-XinHai/CPsyCoun
- Dataset card: https://huggingface.co/datasets/CAS-SIAT-XinHai/CPsyCoun/blob/main/README.md
  (CC-BY-SA-4.0).
- Project: https://github.com/CAS-SIAT-XinHai/CPsyCoun
- Paper: https://aclanthology.org/2024.findings-acl.830/
- Changes: source conversations conditioned dialogue-act trajectory generation
  and long-dialogue expansion; generated utterances and trajectories were
  extracted into the public JSONL schema. These are not original CPsyCounD rows.
- The GitHub repository LICENSE says CC-BY-4.0 while the official dataset card
  says CC-BY-SA-4.0. This release follows the dataset-specific ShareAlike label
  for these adaptations and does not erase that discrepancy.
- Adaptations are distributed under CC-BY-SA-4.0. Attribution, license links,
  and modification notices must be preserved as required by that license.

The original authors do not necessarily endorse CounselTraj or its outputs.
Please cite the original papers alongside the CounselTraj work when appropriate.
