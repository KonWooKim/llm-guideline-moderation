PROMPT_TEMPLATES = {
    "moderate_annotations": """
You are an AI quality control specialist for text annotation.
Your single source of truth is the "ENHANCED AI GUIDELINES".
Your goal is to review the "INITIAL ANNOTATIONS" and the "ORIGINAL TEXT", and produce a final, corrected set of annotations that perfectly aligns with the guidelines.
Perform compliance, completeness, and precision checks, and resolve any disagreements by prioritizing the intent of the "ENHANCED AI GUIDELINES". When adding or removing annotations, explicitly justify the decision and reference the relevant section.

REFERENCE SAMPLES (Follow priority: Primary Gold -> Initial Annotations Sample -> Additional Gold Context):
- Start by comparing the Primary Gold Sample to the Initial Annotations Sample and correct discrepancies.
- Use Additional Gold Samples only as contextual guidance after aligning with the primary gold sample.
{formatted_samples}

Output Format:
- Your final output MUST be a valid JSON object with the keys "annotations" and "changes".
- The value of "annotations" must be an array of objects using this schema:
{json_schema}
- {rationale_instruction}
- The value of "changes" must be an array of objects: {{"action": string, "reason": string, "guideline_section": string}} describing each addition, removal, merge, or other adjustment in a brief, machine-readable audit trail that ties back to the guidelines.
- If no entities in the text meet the criteria, return an empty array for "annotations" and a "changes" array that explains why nothing was annotated.

ENHANCED AI GUIDELINES:
{enhanced_guidelines}

ORIGINAL TEXT:
{input_text}

INITIAL ANNOTATIONS TO REVIEW:
{initial_annotations}

FINAL CORRECTED JSON OUTPUT:
""".strip(),
    "generate_moderation_principle": """
You are an expert "AI Moderator" for an annotation task.
Your goal is to formulate ONE Core Moderation Principle based on the provided Linguistic Analysis of a single dominant error pattern.

ENTITY DEFINITIONS:
{entity_schema}

LINGUISTIC ANALYSIS (The Problem):
{discrepancy_pattern}

SUPPORTING EXAMPLES (Evidence):
{discrepant_examples}

TASK:
1. Review the Linguistic Analysis to understand the root cause.
2. Synthesize a Single General Principle:
   - Structure: IF [Condition] THEN [Action].
   - Negative Constraint: Explicitly state when this rule does NOT apply.
   - Generalization: Phrase the rule using abstract linguistic terms rather than specific words, so it applies to unseen data.
3. Check validity: ensure the principle contradicts neither the entity definitions nor the current guidelines.
4. Return the output as a Markdown list containing just this single general principle.
""".strip(),
    "refine_guidelines": """
You are an expert AI Moderator.

GOAL:
Update the official annotation guidelines to incorporate new moderation principles discovered from error analysis.

CURRENT GUIDELINES:
{guidelines}

NEW MODERATION PRINCIPLES:
{new_principles}

CONSTRAINT: DO NOT BREAK THESE EXAMPLES:
The following examples are currently handled correctly. Your new guidelines MUST NOT cause these to be annotated incorrectly.
{verified_examples}

INSTRUCTIONS:
1. Read the current guidelines and the new principles.
2. Integrate the new principles into the guidelines naturally.
   - Do NOT just append them at the end unless it makes sense.
   - If an existing rule contradicts the new principle, update it.
   - If the new principle clarifies a specific section, add it there.
3. Review the constraint examples above.
4. Ensure your changes support the new principles without invalidating the constraint examples.
5. Maintain the original formatting and structure.
6. Return the FULL updated guidelines text.
7. Do NOT summarize, omit sections, or use placeholders.
8. Output ONLY the guideline text.
""".strip(),
    "infer_discrepancy_patterns": """
You are an expert Computational Linguist.
Your goal is to analyze ONE dominant discrepancy case to find the underlying linguistic cause.

FOCUS:
You are analyzing ONLY the discrepancy type described below. Do not analyze unrelated errors.

ENTITY SCHEMA:
{entity_schema}

INPUT DATA:
1. Discrepancies (the problem): examples of the specific error type we are solving.
2. True positives (the control): correct examples where the model worked.
3. Raw corpus context: unlabeled text showing similar usage.

DISCREPANCIES TO ANALYZE:
{discrepant_examples}

TRUE POSITIVE EXAMPLES:
{true_positive_examples}

RAW CORPUS CONTEXT:
{raw_examples}

TASK:
Step 1. Contrast the discrepancies against the true positives and identify the single boolean feature that separates them.
Step 2. Isolate the trigger that misled the model.
Step 3. Check whether this trigger explains all discrepancy examples. Refine the pattern if needed.
Step 4. Return a Markdown list with exactly one Pattern Insight containing:
- Pattern Name
- Confusion Trigger
- Contrastive Evidence
- Linguistic Rule (Proposed)
""".strip(),
}


def render_prompt(template_name: str, **kwargs: str) -> str:
    try:
        template = PROMPT_TEMPLATES[template_name]
    except KeyError as exc:
        raise ValueError(f"Unknown prompt template: {template_name}") from exc
    return template.format(**kwargs)
