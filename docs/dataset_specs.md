# Dataset Specs

## Purpose

These template specs give each benchmark the same reproduction shape:

- one dataset-level PubAnnotation collection URL,
- one concrete PubAnnotation project URL for the run,
- one moderation source project URL for subset selection,
- one guideline file path,
- one PubAnnotation input document path,
- one evidence block for moderation/refinement.

## Available Templates

- [examples/ncbi_disease_experiment_spec.template.json](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\examples\ncbi_disease_experiment_spec.template.json)
- [examples/bc5cdr_experiment_spec.template.json](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\examples\bc5cdr_experiment_spec.template.json)
- [examples/biored_experiment_spec.template.json](C:\Users\kken1\OneDrive\바탕 화면\ACL\llm-guideline-moderation\examples\biored_experiment_spec.template.json)

## Suggested Convention

- `experiment_id`: `<dataset>_<split>_<project-slug>_round<k>`
- `collection_url`: dataset landing page
- `project_url`: one concrete project inside the collection
- `evaluation_url`: same as `project_url` unless evaluation is hosted separately

## Current Entity Schemas

- `NCBI Disease`: `SpecificDisease`, `DiseaseClass`, `Modifier`, `CompositeMention`
- `BC5CDR`: `Chemical`, `Disease`
- `BioRED`: `GeneOrGeneProduct`, `DiseaseOrPhenotypicFeature`, `ChemicalEntity`, `SequenceVariant`, `CellLine`, `OrganismTaxon`

## Expected Follow-Up

Copy each template, replace the placeholder paths with real files, and keep the shared collection/project URLs in version control so readers can trace the public benchmark context.
