# Dialogue-act annotation prompts

📄 **Paper:** [CounselTraj (arXiv:2611.24168)](https://arxiv.org/abs/2611.24168)

These prompts assign dialogue-act tags to existing counseling utterances for
trajectory construction and cross-dataset dialogue-act analysis. The files retain
the original prompt text and language.

| Target role | Prompt language | Dataset(s) | Tags | Prompt |
| --- | --- | --- | ---: | --- |
| Client | Japanese | KokoroChat | 14 | [client_ja.txt](prompts/client_ja.txt) |
| Counselor | Japanese | KokoroChat | 11 | [counselor_ja.txt](prompts/counselor_ja.txt) |
| Client | Chinese | SmileChat, PsyDTCorpus, CPsyCounD | 14 | [client_zh.txt](prompts/client_zh.txt) |
| Client | English | AnnoMI, Cactus | 14 | [client_en.txt](prompts/client_en.txt) |

## Usage

Choose the template for the target role and dialogue language. Provide the
complete dialogue as JSON, including the other speaker's utterances as context.
The prompts select one tag for each target utterance and request JSON output in a
Markdown code block, with `think` (the label-selection explanation) and `tag`
fields. The Japanese templates preserve `role`, `time`, and `utterance`; the
Chinese and English client templates preserve `role` and `utterance`.

See [dialogue acts and trajectories](../README.md#dialogue-acts) for the label
definitions. These annotation templates are separate from the
[counseling-model evaluation prompts](../evaluation/README.md).
