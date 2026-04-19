# Experiment Specs

These are the main runnable specs for the repository.

- `ncbi_disease_valid_round1.spec.json`
- `bc5cdr_valid_round1.spec.json`
- `biored_valid_round1.spec.json`

Run one with:

```bash
python scripts/run_moderation_round.py --spec experiments/bc5cdr_valid_round1.spec.json
```

Before running:

- use the train files already stored under `data/<dataset>/train/`
- make sure the input PubAnnotation JSON path in the spec exists
- make sure your API key is set
