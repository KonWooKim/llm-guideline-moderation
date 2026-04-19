# llm-guideline-moderation

Python code and metadata for rerunning the moderation simulation used in the paper.

## What this repo is for

- inspect the guideline files used for each dataset
- inspect the train files used as the moderation source pool
- run iterative guideline refinement with your own API key
- annotate a valid/evaluation set with the final refined guidelines
- compare your outputs against the public PubAnnotation evaluation projects

This repository does **not** guarantee exact reproduction of the paper's original LLM outputs.
Instead, it provides:

- the public paper artifacts through PubAnnotation links
- the code path for rerunning similar moderation experiments
- the shared dataset directories used for random subset sampling
- the public evaluation references for comparison

## Dataset references

- BioRED evaluation: [https://pubannotation.org/projects/biored-valid](https://pubannotation.org/projects/biored-valid)
- BC5CDR evaluation: [https://pubannotation.org/projects/bc5cdr-valid](https://pubannotation.org/projects/bc5cdr-valid)
- NCBI evaluation: [https://pubannotation.org/projects/ncbi-valid](https://pubannotation.org/projects/ncbi-valid)

## Reproduction rule used here

- sample from the shared `train` directory
- use `random` sampling
- use `10` examples for paper-style reproduction runs
- use `3` examples for quick debug runs
- use a strict-match moderation termination threshold of `F1 >= 0.9`
- reuse the same sampled subset across compared models
- record the `seed` and sampling metadata in the experiment spec

## Key files

- `src/llm_guideline_moderation/`
- `experiments/`
- `data/`
- `docs/experiment_spec.md`
- `docs/moderation_sampling.md`
- `docs/pubannotation_usage.md`

## Recommended workflow

1. clone the repository
2. inspect the dataset files under `data/datasets/` for the dataset you want to use
3. start with a debug spec in `experiments/` if you want a quick loop check
4. switch to the main spec once the provider, prompts, and evaluation flow look stable
5. set your API key
6. run `python scripts/run_iterative_refinement.py --spec <spec>`
7. take the resulting `final_guidelines.txt`
8. run `python scripts/annotate_pubannotation_dir.py --input-dir <valid_dir> --guidelines <final_guidelines.txt> --entities <schema.json> --output-dir <output_dir>`
9. upload the output JSON files to PubAnnotation and compare them with the public evaluation project

For upload and comparison details, see:

- `docs/pubannotation_usage.md`

## Quick test vs reproduction

- quick debug run: use `*_debug_round1.spec.json` with `sample_size = 3`
- paper-style run: use `*_valid_round1.spec.json` with `sample_size = 10`
- both keep the seed fixed so the same sampled subset can be reused across models
