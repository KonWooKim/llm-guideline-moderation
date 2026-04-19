# PubAnnotation Integration

## Intended Reader Experience

The moderation module does not duplicate the full dataset hosting or evaluation UI.
Instead, readers should be able to:

1. inspect dataset-level context through PubAnnotation collection links,
2. inspect source documents and gold/project context through PubAnnotation project links,
3. inspect evaluation context through PubAnnotation project or evaluation links,
4. inspect moderation artifacts generated in this repository.

## Recommended Artifact Split

### Hosted externally in PubAnnotation

- source documents
- collection landing pages for each dataset
- benchmark project pages
- evaluation project pages

### Stored in this repository

- current guideline text
- train pool archives used for moderation sampling
- moderation subset metadata
- discrepancy evidence used in a moderation round
- moderation prompts
- refined guideline outputs
- moderated annotations in PubAnnotation JSON
- round-by-round logs

## Files Produced By The Runner

The example runner writes:

- `moderation_run.json`
- `final_guidelines.txt`
- `final_annotations.pubann.json`
- `reader_links.json`

`reader_links.json` is meant to store the public PubAnnotation collection/project/evaluation URLs that readers can use to verify the hosted data/evaluation context.

## Example Usage

```bash
python scripts/run_moderation_round.py \
  --input path/to/document.pubann.json \
  --guidelines path/to/guidelines.txt \
  --entities examples/entity_schema.example.json \
  --output-dir outputs/run_001 \
  --model gpt-5 \
  --rounds 1 \
  --project-link "https://pubannotation.org/projects/your-project" \
  --evaluation-link "https://pubannotation.org/projects/your-eval-project"
```

## Suggested Public Links To Publish

- one dataset project link per benchmark
- one collection link per benchmark
- one evaluation link per benchmark or split
- one short README table that maps experiment IDs to those URLs
