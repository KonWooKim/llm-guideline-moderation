# llm-guideline-moderation
Resources for refining and reusing annotation guidelines for LLM annotation, with a Python-first moderation module for reproduction experiments.

## Current focus

The repository is being organized around the guideline refinement workflow rather than the original UI-heavy annotation tool.

- [docs/reproduction_plan.md](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\docs\reproduction_plan.md)
- [docs/moderation_module_plan.md](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\docs\moderation_module_plan.md)

## Python module

The extracted headless moderation package lives under:

- [src/llm_guideline_moderation](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\src\llm_guideline_moderation)

It currently includes:

- moderation-related data types
- prompt templates ported from the original project
- prompt formatting helpers
- heuristic risk assessment
- provider-agnostic moderation pipeline
- PubAnnotation conversion helpers
- OpenAI and Gemini provider adapters
- experiment spec and artifact layout helpers

## PubAnnotation workflow

The expected reproduction setup is:

1. each dataset is exposed through a PubAnnotation collection
2. documents and evaluation context are hosted in PubAnnotation projects inside that collection
3. this repository stores moderation/refinement artifacts
4. readers can verify the original context through published PubAnnotation collection/project links

Moderation runs do not assume one fixed train set artifact.
Each run should record how its working subset was sampled from the shared train archive.
The current recommended default is random sampling of 10 training examples with one shared seed and one shared sampled subset reused across all compared models.

- [docs/pubannotation_integration.md](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\docs\pubannotation_integration.md)
- [docs/experiment_spec.md](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\docs\experiment_spec.md)
- [docs/dataset_specs.md](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\docs\dataset_specs.md)
- [docs/moderation_sampling.md](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\docs\moderation_sampling.md)

## Working Files

- [experiments](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\experiments)
- [data](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\data)
