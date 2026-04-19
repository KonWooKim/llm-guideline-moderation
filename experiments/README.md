# Experiment Specs

These are the main runnable specs for the repository.

- `ncbi_disease_valid_round1.spec.json`
- `bc5cdr_valid_round1.spec.json`
- `biored_valid_round1.spec.json`

These are the quick debug specs for faster live testing.

- `ncbi_disease_debug_round1.spec.json`
- `bc5cdr_debug_round1.spec.json`
- `biored_debug_round1.spec.json`

Run a paper-style spec with:

```bash
python scripts/run_moderation_round.py --spec experiments/bc5cdr_valid_round1.spec.json
```

Run a quick debug spec with:

```bash
python scripts/run_iterative_refinement.py --spec experiments/bc5cdr_debug_round1.spec.json
```

Before running:

- use the train files already stored under `data/datasets/<dataset>/train/`
- make sure the input PubAnnotation JSON path in the spec exists
- make sure your API key is set
- use debug specs for `sample_size = 3`
- use main specs for `sample_size = 10`
