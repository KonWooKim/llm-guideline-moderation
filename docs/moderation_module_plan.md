# Moderation Module Plan

## Goal

Extract only the guideline refinement / moderation simulation logic from the original `LLM-Annotator` codebase and rebuild it as a headless Python module for reproduction experiments.

## Why Python-Only Extraction

The original project mixes:

- React UI components
- workflow hooks for interactive usage
- provider-specific LLM calls
- evaluation and export utilities
- guideline generation and moderation logic

For reproduction, the reusable core is not the UI. It is the moderation pipeline:

1. inspect discrepancy evidence,
2. infer a dominant pattern,
3. generate one moderation principle,
4. rewrite the guideline text,
5. optionally re-moderate annotations with the refined guideline,
6. record audit trail and heuristic risk.

## Scope To Keep

- moderation prompts
- prompt formatting helpers
- moderation types
- risk heuristics
- provider-agnostic LLM interface
- single-round and multi-round moderation pipeline

## Scope To Exclude

- guideline generation from scratch
- evaluation code
- batch UI state
- charts and exports
- React hooks and components
- app-specific cost dashboards

## Python Package Layout

```text
src/llm_guideline_moderation/
  __init__.py
  types.py
  prompts.py
  prompt_utils.py
  risk.py
  pipeline.py
  providers/
    __init__.py
    base.py
```

## Core Abstraction

The module starts from already available experiment state:

- `text`
- `initial_annotations`
- `guidelines`
- optional `gold/reference samples`
- chosen `provider adapter`

It does **not** assume that the moderation module is responsible for creating the first-pass annotations.

## Pipeline Contract

### `simulate_moderation_round`

Input:

- text
- current guidelines
- initial annotations
- entity schema
- provider
- optional reference samples
- optional verified examples

Output:

- discrepancy insight
- moderation principle
- refined guidelines
- moderated annotations
- audit trail
- risk assessment

### `simulate_moderation_iterations`

Runs multiple rounds and stores snapshots for later analysis.

## Mapping From Old Code

### Reused concepts

- `moderateAnnotations` prompt
- `inferDiscrepancyPatterns` prompt
- `generateModerationPrinciples` prompt
- `refineGuidelines` prompt
- `formatSampleSectionsForPrompt`
- `generateSchemaParts`
- `assessRisk`

### Intentionally dropped

- `useBatchModerationFlow`
- `useFinalAnnotationSourceFlow`
- `ModerationContent.tsx`
- `ModerationQueuePanel.tsx`

Those files are orchestration/UI wrappers, not reusable research core.

## Recommended Next Step

After this skeleton lands, the next useful implementation step is to add one concrete provider adapter, likely OpenAI first, and define the JSON artifact format for round-by-round experiment outputs.
