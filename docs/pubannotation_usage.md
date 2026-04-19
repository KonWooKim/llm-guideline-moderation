# PubAnnotation Upload And Comparison

This repository produces PubAnnotation JSON files so that you can inspect and compare outputs in PubAnnotation rather than only in local files.

PubAnnotation is a good fit for this workflow because it aligns uploaded annotations to canonical PubMed or PMC texts, and annotations for the same document can be viewed together across projects.

## What You Need Before Upload

- a PubAnnotation project that contains the same documents as your target evaluation set
- local output JSON files produced by this repository
- matching `sourcedb` and `sourceid` values between your output files and the PubAnnotation documents

In this repository, the most common path is:

1. run iterative refinement on a train subset
2. take the resulting `final_guidelines.txt`
3. annotate the valid set with `scripts/annotate_pubannotation_dir.py`
4. upload the produced JSON files to your own PubAnnotation project
5. compare your project with the public evaluation project

## Local Output To Upload

After annotation, you will typically have a directory like:

```text
outputs/<run_name>/
  10074612.json
  10539815.json
  10840460.json
```

Each file is already in PubAnnotation JSON format. The important fields are:

- `text`
- `sourcedb`
- `sourceid`
- `denotations`

The PubAnnotation JSON format is documented here:

- [Annotation format](https://www.pubannotation.org/docs/annotation-format/)

## Recommended Upload Workflow

### 1. Create or open your project

Create your own PubAnnotation project for the model output you want to inspect.

Keep the project dataset-specific. For example:

- one project for BC5CDR valid outputs
- one project for BioRED valid outputs
- one project for NCBI valid outputs

### 2. Make sure document identity matches

Before upload, confirm that:

- your local JSON files use the same `sourcedb`
- your local JSON files use the same `sourceid`

as the documents in the PubAnnotation project you want to compare against.

This matters because PubAnnotation aligns annotations by canonical document identity, not by local filename alone.

### 3. Upload annotations

There are two practical ways to upload.

#### Option A. Use the PubAnnotation editor UI

PubAnnotation documents can be opened in the editor and saved back to PubAnnotation.

Official references:

- [Creating annotations](https://www.pubannotation.org/docs/create-annotation/)
- [Annotation editors](https://www.pubannotation.org/docs/annotation-editor/)

This is the easiest route if you want to inspect a few files manually.

#### Option B. Use the PubAnnotation API

PubAnnotation exposes annotation endpoints that accept PubAnnotation JSON.

Official references:

- [PubAnnotation API](https://www.pubannotation.org/docs/api/)
- [Annotation editors](https://www.pubannotation.org/docs/annotation-editor/)

The general pattern is:

```bash
curl -H "content-type: application/json" -u "USERNAME:PASSWORD" -d @annotations.json "https://pubannotation.org/projects/<your-project>/docs/sourcedb/<SOURCE_DB>/sourceid/<SOURCE_ID>/annotations.json"
```

Use this route when you want to upload many files produced by this repository.

## How To Compare With The Public Evaluation Project

The easiest conceptual rule is:

- your project holds your model output
- the public evaluation project holds the reference annotations
- both point to the same `sourcedb/sourceid`

Because PubAnnotation aligns annotations for the same canonical text, you can inspect the same document across projects.

Useful official background:

- [Intro](https://www.pubannotation.org/docs/intro/)
- [PubAnnotation top page](https://pubannotation.org/)

### Practical comparison workflow

1. Upload your output files to your own project.
2. Open the corresponding public evaluation project for the dataset.
3. Check that the same `sourceid` exists in both projects.
4. Inspect the document in PubAnnotation to compare spans and labels.
5. Repeat for error analysis or reporting.

### Dataset evaluation references

- BC5CDR evaluation: [https://pubannotation.org/projects/bc5cdr-valid](https://pubannotation.org/projects/bc5cdr-valid)
- BioRED evaluation: [https://pubannotation.org/projects/biored-valid](https://pubannotation.org/projects/biored-valid)
- NCBI evaluation: [https://pubannotation.org/projects/ncbi-valid](https://pubannotation.org/projects/ncbi-valid)

## Comparison Tip

When you want to compare annotations across projects, make sure you are looking at the same document identity, not just a similar filename.

For BC5CDR and BioRED in particular, local filenames may include prefixes such as `valid_`, while the canonical alignment still depends on the `sourceid` and `sourcedb` inside the JSON.

## Suggested Repository Workflow

### Quick smoke test

Use a debug spec and annotate only a few valid files first.

Example:

```bash
python scripts/run_iterative_refinement.py --spec experiments/bc5cdr_debug_round1.spec.json
python scripts/annotate_pubannotation_dir.py --input-dir outputs/bc5cdr_valid_smoke_input --guidelines outputs/bc5cdr_valid_gpt_r_g_debug_round1_iterative/final/final_guidelines.txt --entities data/schemas/bc5cdr_entities.schema.json --output-dir outputs/bc5cdr_valid_smoke_output
```

### Full evaluation preparation

After the smoke test looks correct:

1. rerun refinement with the main spec
2. annotate the full valid 100-document directory
3. upload the resulting JSON files to your PubAnnotation project
4. compare them with the public evaluation project

## Notes

- PubAnnotation UI details may change over time, so the official documentation links above should be treated as the authoritative reference.
- This repository focuses on producing valid PubAnnotation JSON outputs and a reproducible refinement workflow; final visual comparison is intentionally delegated to PubAnnotation.
