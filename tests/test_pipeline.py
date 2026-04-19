from __future__ import annotations

import json
import unittest

from test_support import SRC_ROOT  # noqa: F401

from llm_guideline_moderation.pipeline import simulate_moderation_iterations, simulate_moderation_round
from llm_guideline_moderation.types import EntityDefinition, ModerationRoundInput


class FakeProvider:
    def __init__(self) -> None:
        self.calls: list[tuple[str, str]] = []

    def complete(self, task: str, prompt: str) -> str:
        self.calls.append((task, prompt))
        if task == "infer_discrepancy_patterns":
            return "- Pattern Name: Numeric modifier confusion"
        if task == "generate_moderation_principle":
            return "- IF a numeric modifier narrows the disease mention THEN keep the narrower span."
        if task == "refine_guidelines":
            return "Refined guideline text"
        if task == "moderate_annotations":
            return json.dumps(
                {
                    "annotations": [
                        {
                            "start": 0,
                            "end": 8,
                            "text": "diabetes",
                            "entity": "Disease",
                            "rationale": "Matches disease span",
                            "guideline_section": "Specific span rules",
                        }
                    ],
                    "changes": [
                        {
                            "action": "keep",
                            "reason": "Original span already matches refined rule",
                            "guideline_section": "Specific span rules",
                        }
                    ],
                }
            )
        raise AssertionError(f"Unexpected task: {task}")


class PipelineTests(unittest.TestCase):
    def setUp(self) -> None:
        self.provider = FakeProvider()
        self.round_input = ModerationRoundInput(
            text="diabetes is chronic",
            guidelines="Original guideline text",
            initial_annotations=[],
            entities=[EntityDefinition(name="Disease", description="Disease mention")],
            discrepancy_examples="Example discrepancy",
            true_positive_examples="Example true positive",
            raw_examples="Raw example",
            verified_examples="Verified example",
        )

    def test_simulate_single_round_returns_refined_result(self) -> None:
        result = simulate_moderation_round(1, self.round_input, self.provider)

        self.assertEqual(result.round_index, 1)
        self.assertEqual(result.refined_guidelines, "Refined guideline text")
        self.assertEqual(len(result.moderated_annotations), 1)
        self.assertEqual(result.moderated_annotations[0].entity, "Disease")
        self.assertEqual(len(result.audit_trail), 1)
        self.assertIn("infer_discrepancy_patterns", result.prompts)
        self.assertEqual([task for task, _ in self.provider.calls], [
            "infer_discrepancy_patterns",
            "generate_moderation_principle",
            "refine_guidelines",
            "moderate_annotations",
        ])

    def test_simulate_multiple_rounds_updates_guidelines(self) -> None:
        result = simulate_moderation_iterations(self.round_input, self.provider, num_rounds=2)

        self.assertEqual(len(result.rounds), 2)
        self.assertEqual(result.final_guidelines, "Refined guideline text")
        self.assertEqual(result.final_annotations[0].text, "diabetes")


if __name__ == "__main__":
    unittest.main()
