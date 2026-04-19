# Reproduction Plan: Refining and Reusing Annotation Guidelines for LLM Annotation

## Goal

Reproduce the paper's main claim that reusing and iteratively refining annotation guidelines improves LLM-based biomedical NER annotation, and verify how much benefit comes from:

1. adding guidelines at inference time,
2. using stronger reasoning-oriented models,
3. iteratively moderating and refining the guidelines with minimal supervision.

## What We Know So Far

Based on the paper abstract and metadata on OpenReview, the study focuses on:

- Task: biomedical named entity recognition
- Datasets: `NCBI Disease`, `BC5CDR`, `BioRED`
- Model families: `GPT`, `Gemini`, `DeepSeek`
- Core method: reuse existing annotation guidelines, then refine them through an iterative moderation framework
- Main hypotheses:
  - guideline integration helps LLM annotation,
  - reasoning-optimized models help more,
  - guideline moderation is viable even with minimal supervision.

## First Principle

Do not start from "training a big system."
Start from a **traceable inference-and-evaluation pipeline** where every prediction can be linked back to:

- the input abstract or sentence,
- the guideline version,
- the prompt version,
- the model name,
- the decoding settings,
- the post-processing rules,
- the gold annotation,
- the evaluation result.

If we build that spine first, the rest of the reproduction becomes manageable.

## Recommended Starting Point

### Phase 1: Nail the smallest faithful reproduction

Build only this first:

1. one dataset: `NCBI Disease`
2. one model family: `GPT`
3. two prompt conditions:
   - `no_guideline`
   - `with_reused_guideline`
4. one evaluation mode:
   - entity-level precision / recall / F1

Why this first:

- NCBI Disease is the cleanest place to validate the paper's basic claim.
- It likely has the most directly reusable disease annotation guideline.
- If the baseline pipeline is shaky here, scaling to BC5CDR and BioRED will only amplify confusion.

### Phase 2: Add the real experimental axes

After the minimal pipeline works, expand to:

1. dataset axis: `NCBI Disease -> BC5CDR -> BioRED`
2. model axis: `GPT -> Gemini -> DeepSeek`
3. guideline axis:
   - `no guideline`
   - `original reused guideline`
   - `refined guideline v1/v2/...`
4. supervision axis:
   - `zero/minimal supervision`
   - any stronger moderation setting reported in the paper

## Experimental Design We Should Implement

### A. Recreate the comparison table first

Before coding too much, write down the exact experimental matrix from the paper in a CSV or Markdown table.

At minimum, include:

| experiment_id | dataset | split | model | prompt_condition | guideline_version | moderation_round | supervision_level | metric |
|---|---|---|---|---|---|---|---|---|
| exp_001 | NCBI Disease | test | GPT | no_guideline | none | 0 | none | strict_f1 |

This becomes the contract for the whole repo.

### B. Treat guidelines as versioned data

The paper is about guidelines, so guidelines should live as first-class artifacts:

- `guidelines/original/`
- `guidelines/refined/round_01/`
- `guidelines/refined/round_02/`
- `guidelines/refined/final/`

Each guideline file should have:

- source dataset
- source URL or citation
- normalization notes
- changes from previous version
- who or what produced the revision
- rationale for each revision

### C. Separate three prompt roles

Do not mix these into one giant prompt file.

1. `annotation prompt`
   - asks the model to label entities
2. `moderation prompt`
   - asks the model to analyze disagreements, misses, or ambiguous cases
3. `guideline revision prompt`
   - asks the model to update the guideline text itself

That separation will matter when we analyze which component actually helps.

### D. Decide the annotation unit early

This is one of the biggest reproduction risks.
We need to confirm from the paper whether annotation is run on:

- full abstract,
- sentence,
- sentence with surrounding context,
- candidate span list,
- token-tag sequence.

Until the paper confirms otherwise, the safest default is:

- run inference on the natural document unit used by the benchmark,
- convert model output into normalized entity spans,
- evaluate against gold spans.

## Repo Structure To Create

```text
docs/
  reproduction_plan.md
  experiment_matrix.csv
  open_questions.md
data/
  raw/
  processed/
  splits/
guidelines/
  original/
  refined/
prompts/
  annotation/
  moderation/
  revision/
outputs/
  predictions/
  moderation_logs/
  guideline_diffs/
  tables/
src/
  loaders/
  prompting/
  parsing/
  moderation/
  evaluation/
  utils/
configs/
  datasets/
  models/
  experiments/
```

## Concrete Deliverables To Upload

If you need to "make and upload related information" for reproduction, prepare these first:

1. `paper_summary.md`
   - one-page summary of task, hypotheses, datasets, models, and results
2. `experiment_matrix.csv`
   - exact list of all experimental runs to reproduce
3. `artifact_inventory.md`
   - what must be collected from the paper, external datasets, and guideline sources
4. `open_questions.md`
   - every method detail still missing from the paper read
5. `reproduction_checklist.md`
   - a yes/no execution checklist for each experiment

These five files are more useful than writing code too early.

## Information To Extract From The Paper Before Coding Further

This is the minimum metadata extraction checklist:

### Task and data

- exact dataset versions
- train/dev/test usage
- any subsampling or few-shot setting
- whether chemical and disease labels are both used in BC5CDR
- which BioRED entity types are included
- preprocessing rules
- span normalization rules

### Models and inference

- exact model names and release dates
- API vs local inference
- system prompts / user prompts
- temperature / top-p / seed
- max tokens
- number of retries
- output format constraints
- cost control or truncation rules

### Moderation framework

- what input the moderator sees
- whether gold labels are shown
- how "minimal supervision" is defined
- how many moderation rounds are run
- whether revision is dataset-specific or transferred across datasets
- who approves a revised guideline version

### Evaluation

- exact metric definition
- strict vs partial span matching
- micro vs macro averaging
- statistical significance test
- number of runs / variance reporting

## Biggest Reproduction Risks

1. **Prompt under-specification**
   - Small wording changes may strongly affect LLM annotation quality.
2. **Guideline format drift**
   - Converting PDF guidelines into prompt-ready text may unintentionally change the method.
3. **Span parsing errors**
   - Many apparent model mistakes are actually output-parsing mistakes.
4. **Dataset mismatch**
   - BC5CDR and BioRED may differ in scope and label semantics enough to break cross-dataset transfer.
5. **Model version drift**
   - Current API models may not match the paper's exact evaluation environment.

## Suggested Success Criteria

Define success in layers:

1. **Pipeline success**
   - the run is deterministic and evaluable end to end
2. **Directional success**
   - `with_guideline` beats `no_guideline` on the main dataset
3. **Pattern success**
   - stronger reasoning models outperform weaker ones in the same setting
4. **Paper-level success**
   - the ranking and relative gains broadly match the reported trends

This is better than insisting on exact absolute scores too early.

## 7-Day Practical Plan

### Day 1

- read the paper closely and fill `paper_summary.md`
- build `experiment_matrix.csv`
- collect dataset and guideline source links

### Day 2

- implement dataset loader for `NCBI Disease`
- define prediction JSON schema
- define evaluation script for entity-level F1

### Day 3

- implement `no_guideline` and `with_reused_guideline` prompts
- run a tiny pilot on 20 to 50 examples
- debug parsing and error categories

### Day 4

- run full `NCBI Disease` baseline
- write first error analysis note
- freeze prompt version `v1`

### Day 5

- implement moderation loop
- create `refined guideline v1`
- compare against original guideline

### Day 6

- extend to `BC5CDR`
- test transfer or reuse behavior

### Day 7

- extend to one more model family
- generate final tables and a short reproduction report

## What I Would Do Next In This Repo

Immediate next actions:

1. create the metadata files listed above,
2. transcribe the paper's experiment table into `docs/experiment_matrix.csv`,
3. collect the original guideline documents for `NCBI Disease`, `BC5CDR`, and `BioRED`,
4. define a single JSON output schema for model predictions,
5. only then start implementing the loader and evaluator.

## Important Note

This plan is grounded in the paper's OpenReview abstract and the repository goal in `README.md`.
Before locking any prompt or evaluation detail, we should verify the full paper text for the exact implementation choices.
