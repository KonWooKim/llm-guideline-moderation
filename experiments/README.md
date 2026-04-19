# Experiment Specs

These are the main runnable specs for the repository.

- [ncbi_disease_valid_round1.spec.json](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\experiments\ncbi_disease_valid_round1.spec.json)
- [bc5cdr_valid_round1.spec.json](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\experiments\bc5cdr_valid_round1.spec.json)
- [biored_valid_round1.spec.json](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\experiments\biored_valid_round1.spec.json)

Run one with:

```bash
python scripts/run_moderation_round.py --spec experiments/bc5cdr_valid_round1.spec.json
```

Before running:

- unzip the dataset train archive from `data/archives/`
- make sure the input PubAnnotation JSON path in the spec exists
- make sure your API key is set
