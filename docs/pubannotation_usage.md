# PubAnnotation upload and comparison

This repository intentionally stops at producing PubAnnotation-format JSON files. Final visual inspection and comparison are meant to happen in PubAnnotation.

## Recommended workflow

1. Run iterative refinement on a sampled train subset.
2. Take the resulting `final_guidelines.txt`.
3. Annotate the valid set with `scripts/annotate_pubannotation_dir.py`.
4. Upload the generated JSON files to your own PubAnnotation project.
5. Compare your project with the public evaluation project for the same dataset.

## Before you upload

Make sure all three of these are aligned:

- the documents in your PubAnnotation project
- the local JSON files produced by this repo
- the public evaluation project you want to compare against

The important identity fields are:

- `sourcedb`
- `sourceid`

PubAnnotation compares annotations by canonical document identity, not by filename alone.

## What the repo outputs

After directory annotation, you will usually have a folder like:

```text
outputs/<run_name>/
  10074612.json
  10539815.json
  10840460.json
```

Each file is already valid PubAnnotation JSON with fields such as:

- `text`
- `sourcedb`
- `sourceid`
- `denotations`

Format reference:

- [PubAnnotation annotation format](https://www.pubannotation.org/docs/annotation-format/)

## Upload options

### Option 1: PubAnnotation UI

This is easiest when you want to inspect a few files manually.

- [Creating annotations](https://www.pubannotation.org/docs/create-annotation/)
- [Annotation editor](https://www.pubannotation.org/docs/annotation-editor/)

### Option 2: PubAnnotation API

This is better when you want to upload a full valid set.

- [PubAnnotation API](https://www.pubannotation.org/docs/api/)

Example request shape:

```bash
curl -H "content-type: application/json" -u "USERNAME:PASSWORD" -d @annotations.json "https://pubannotation.org/projects/<your-project>/docs/sourcedb/<SOURCE_DB>/sourceid/<SOURCE_ID>/annotations.json"
```

## Public evaluation projects

- BC5CDR: [https://pubannotation.org/projects/bc5cdr-valid](https://pubannotation.org/projects/bc5cdr-valid)
- BioRED: [https://pubannotation.org/projects/biored-valid](https://pubannotation.org/projects/biored-valid)
- NCBI Disease: [https://pubannotation.org/projects/ncbi-valid](https://pubannotation.org/projects/ncbi-valid)

## Practical comparison flow

1. Upload your output files to your own project.
2. Open the public evaluation project for the same dataset.
3. Check that both projects contain the same `sourcedb/sourceid`.
4. Inspect the same document across projects.
5. Use those comparisons for error analysis or reporting.

## Suggested usage pattern

Start small:

- run a debug spec with `sample_size = 3`
- annotate a few valid files
- confirm the outputs look right in PubAnnotation

Then scale up:

- run the main spec with `sample_size = 10`
- annotate the full valid 100-document set
- upload the full output directory
- compare against the public evaluation project

Official PubAnnotation documentation may change over time, so treat the links above as the authoritative source for UI and API details.
