# Experiment Specs

These are runnable spec files intended to become the canonical entry points for published moderation runs.

- [ncbi_disease_valid_round1.spec.json](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\experiments\ncbi_disease_valid_round1.spec.json)
- [bc5cdr_valid_round1.spec.json](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\experiments\bc5cdr_valid_round1.spec.json)
- [biored_valid_round1.spec.json](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\experiments\biored_valid_round1.spec.json)

Run one with:

```bash
python scripts/run_moderation_round.py --spec experiments/bc5cdr_valid_round1.spec.json
```

Before running, replace placeholder input files under `data/` with the real PubAnnotation exports and guideline text.
The train archives under `data/archives/` are the shared source pools for random 10-example moderation sampling.
