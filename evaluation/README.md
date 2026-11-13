# Table 6 evaluation prompts

These are the original Chinese implementation templates for the response-level
and dialogue-level evaluations in Table 6 of the CounselTraj paper. Appendix D.2
(Figure 12) and Appendix D.4 (Figure 14) present their English descriptions.

| Evaluation | Prompt | Dimensions | Score range |
| --- | --- | --- | --- |
| Response-level: PsyDial-D101 | [response_level_zh.txt](prompts/response_level_zh.txt) | AL, Emp., IC, OQ, SE, CR, GQ, NJA | 1–5, integers |
| Dialogue-level: PsychEval | [dialogue_level_zh.txt](prompts/dialogue_level_zh.txt) | TA, EU, PU, EI, PC, SB | 1–5, integers |

The evaluations use GPT-5.4 and gemini-3.5-flash. The response-level evaluation
covers 1,278 examples; the dialogue-level evaluation covers 100 client profiles.
Table 6 averages the two judges' scores. Its Ovl. column is the arithmetic mean
of the corresponding skill or process dimensions, rather than the separate
`overall` judgment requested by the response-level prompt.

## Inputs and scoring

For the response-level template, replace `<<LABEL_LIST>>` with anonymous candidate
IDs, `<<SCORE_SCHEMA>>` with a JSON score schema for those IDs, `<<HISTORY>>` with
the dialogue history, and `<<CANDIDATES>>` with the labeled candidate responses.
The implementation shuffles the candidates and asks the judge to compare them
before assigning scores. The original evaluation includes a human reference and
two additional decoding variants alongside the ten models reported in Table 6.

For the dialogue-level template, replace `<<CLIENT_PROFILE>>` with the client
profile and `<<MODEL_DIALOGUES>>` with the complete dialogues. The implementation
shuffles the dialogue order and uses `[Model: model_id]` headers. Some batches
request scores without explanations, using the same six-dimensional rubric.

These files preserve the experiment wording; they are not rewritten translations
of the appendix figures.
