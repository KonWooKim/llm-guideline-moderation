# Experiment Spec

## Purpose

Use one JSON spec file per reproducible moderation run so that:

- the dataset-level PubAnnotation collection link is preserved,
- PubAnnotation project links are preserved next to the run,
- the moderation subset selection rule is preserved,
- the exact guideline/input/schema files are recorded,
- the chosen provider/model/round count are explicit,
- readers can trace every artifact directory back to a named experiment.

## Directory Layout

Each run now uses this structure:

```text
outputs/<experiment_id>/
  inputs/
    input.pubann.json
    guidelines.txt
    entity_schema.json
    experiment_spec.json
  rounds/
    round_01/
      result.json
      infer_discrepancy_patterns.txt
      generate_moderation_principle.txt
      refine_guidelines.txt
      moderate_annotations.txt
  final/
    moderation_run.json
    final_guidelines.txt
    final_annotations.pubann.json
  links/
    reader_links.json
```

## Runner Usage

```bash
python scripts/run_moderation_round.py --spec examples/experiment_spec.example.json
```

You can still use the direct CLI flags, but `--spec` is the recommended format for published reproduction runs.

## Recommended Link Policy

- `collection_url`: the dataset landing page you plan to share publicly
- `project_url`: the concrete PubAnnotation project used for the current run
- `evaluation_url`: the concrete evaluation target if it differs from `project_url`

## Recommended Moderation Metadata

- `source_project_url`: the PubAnnotation project used as the pool for moderation sampling
- `source_archive_path`: the local train archive copied into this repository
- `source_split`: usually `train`
- `sampling_method`: how the subset was chosen
- `sample_size`: how many examples were used for moderation
- `seed`: random seed when applicable
- `shared_across_models`: whether the same sampled subset is reused across models
- `selection_note`: any manual rule or filtering note needed to interpret the run
