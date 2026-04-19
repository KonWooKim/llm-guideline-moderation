# Moderation Sampling

## Key Point

This repository treats the train pool as a shared source directory for moderation.
Each moderation run records how its working subset was selected from that larger train pool.

## What Must Be Recorded Per Run

- `source_project_url`
- `source_dir_path`
- `source_split`
- `sampling_method`
- `sample_size`
- `seed` if randomization is used
- `shared_across_models`
- `selection_note`

## Why This Matters

Moderation behavior can change when:

- the subset size changes,
- the subset is sampled differently,
- different seeds are used,
- each model receives a different subset.

For that reason, the reproducibility target is:

- transparent subset selection metadata,
- not exact duplication of one hidden or fixed train split artifact.

## Recommended Default For This Repository

- `sampling_method`: `random`
- `sample_size`: `10`
- `shared_across_models`: `true`
- `seed`: record the actual seed used for the paper run or reproduction run
- `selection_note`: `Randomly sample 10 training examples from the shared train directory and reuse the same sampled subset for every model in this comparison.`

## Why Shared Sampling Is Preferred

If GPT, Gemini, and DeepSeek each receive a different random 10-example subset, model differences become harder to interpret.
Using the same sampled subset across models makes the comparison cleaner and closer to controlled reproduction.

## Current Evaluation Source Projects

- BioRED: [https://pubannotation.org/projects/biored-valid](https://pubannotation.org/projects/biored-valid)
- BC5CDR: [https://pubannotation.org/projects/bc5cdr-valid](https://pubannotation.org/projects/bc5cdr-valid)
- NCBI Disease: [https://pubannotation.org/projects/ncbi-valid](https://pubannotation.org/projects/ncbi-valid)
