# llm-guideline-moderation

Python code and metadata for rerunning the moderation simulation used in the paper.

## What this repo is for

- inspect the guideline files used for each dataset
- inspect the train archives used as the moderation source pool
- run moderation simulation code with your own API key
- compare your outputs against the public PubAnnotation evaluation projects

This repository does **not** guarantee exact reproduction of the paper's original LLM outputs.
Instead, it provides:

- the public paper artifacts through PubAnnotation links
- the code path for rerunning similar moderation experiments
- the shared train archives used for random subset sampling
- the public evaluation references for comparison

## Dataset references

- BioRED evaluation: [https://pubannotation.org/projects/biored-valid](https://pubannotation.org/projects/biored-valid)
- BC5CDR evaluation: [https://pubannotation.org/projects/bc5cdr-valid](https://pubannotation.org/projects/bc5cdr-valid)
- NCBI evaluation: [https://pubannotation.org/projects/ncbi-valid](https://pubannotation.org/projects/ncbi-valid)

## Reproduction rule used here

- sample from the shared `train` archive
- use `random` sampling
- use `10` examples
- reuse the same sampled subset across compared models
- record the `seed` and sampling metadata in the experiment spec

## Key files

- `src/llm_guideline_moderation/`
- `experiments/`
- `data/`
- `docs/experiment_spec.md`
- `docs/moderation_sampling.md`

## Minimal workflow

1. clone the repository
2. unzip the train archive for the dataset you want to use
3. check the corresponding spec in `experiments/`
4. set your API key
5. run `python scripts/run_moderation_round.py --spec <spec>`
6. compare your outputs with the public PubAnnotation evaluation project
