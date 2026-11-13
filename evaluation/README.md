# Response-level and dialogue-level evaluation prompts

These Chinese templates cover the response-level and dialogue-level evaluations
of counseling models in the CounselTraj paper. Appendix D.2
(Figure 12) and Appendix D.4 (Figure 14) present their English descriptions.

| Evaluation | Prompt | Dimensions | Score range |
| --- | --- | --- | --- |
| Response-level: PsyDial-D101 | [response_level_zh.txt](prompts/response_level_zh.txt) | AL, Emp., IC, OQ, SE, CR, GQ, NJA | 1–5, integers |
| Dialogue-level: PsychEval | [dialogue_level_zh.txt](prompts/dialogue_level_zh.txt) | TA, EU, PU, EI, PC, SB | 1–5, integers |

The evaluations use GPT-5.4 and gemini-3.5-flash. The response-level evaluation
covers 1,278 examples; the dialogue-level evaluation covers 100 client profiles.
Reported scores average the two judges' scores. The Ovl. score is the arithmetic mean
of the corresponding skill or process dimensions, rather than the separate
`overall` judgment requested by the response-level prompt.

## Research basis and references

### Response-level evaluation

The response-level evaluation follows the PsyDial evaluation setting of Qiu and
Lan (2025), using PsyDial-D101 and its eight counseling-skill dimensions: Active
Listening, Empathy, Issue Clarification, Open-ended Questioning, Encouraging
Self-Exploration, Cognitive Restructuring, Guided Questioning, and Non-judgmental
Acceptance.

- Huachuan Qiu and Zhenzhong Lan (2025). [PsyDial: A Large-scale Long-term Conversational Dataset for Mental Health Support](https://aclanthology.org/2025.acl-long.1049/). ACL 2025. Provides the professional-book counseling benchmark and response-level skill evaluation setting.

### Dialogue-level evaluation

The dialogue-level evaluation uses client profiles from PsychEval and draws on
the counseling constructs below. The six-dimensional rubric adapts these
foundations to evaluate complete simulated counseling sessions.

| Prior work | Role in this evaluation |
| --- | --- |
| Qianjun Pan et al. (2026). [PsychEval: A Multi-Session and Multi-Therapy Benchmark for High-Realism AI Psychological Counselor](https://arxiv.org/abs/2601.01802). | Source of client profiles and a reference for interactive counseling evaluation. |
| Adam O. Horvath and Leslie S. Greenberg (1989). [Development and Validation of the Working Alliance Inventory](https://doi.org/10.1037/0022-0167.36.2.223). Journal of Counseling Psychology. | Conceptual basis for Therapeutic Alliance (TA), including collaboration, trust, and the counseling relationship. |
| Carl R. Rogers (1957). [The Necessary and Sufficient Conditions of Therapeutic Personality Change](https://doi.org/10.1037/h0045357). Journal of Consulting Psychology. | Conceptual basis for empathic understanding, acceptance, and the therapeutic relationship. |
| Clara E. Hill (2009). [Helping Skills: Facilitating Exploration, Insight, and Action, third edition](https://www.apa.org/pubs/books/interviews/4311012-hill). APA book; link to the publisher's author discussion. | Conceptual basis for exploration, appropriate interventions, and progression through the helping process. |

## Inputs and scoring

For the response-level template, replace `<<LABEL_LIST>>` with anonymous candidate
IDs, `<<SCORE_SCHEMA>>` with a JSON score schema for those IDs, `<<HISTORY>>` with
the dialogue history, and `<<CANDIDATES>>` with the labeled candidate responses.
The implementation shuffles the candidates and asks the judge to compare them
before assigning scores. The original evaluation includes a human reference and
two additional decoding variants alongside the ten models compared in the paper.

For the dialogue-level template, replace `<<CLIENT_PROFILE>>` with the client
profile and `<<MODEL_DIALOGUES>>` with the complete dialogues. The implementation
shuffles the dialogue order and uses `[Model: model_id]` headers. Some batches
request scores without explanations, using the same six-dimensional rubric.

These templates retain the experiment's scoring criteria and omit unused output
fields.
