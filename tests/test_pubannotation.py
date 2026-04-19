from __future__ import annotations

import unittest

from test_support import SRC_ROOT  # noqa: F401

from llm_guideline_moderation.pubannotation import annotations_to_pubannotation, pubannotation_to_annotations
from llm_guideline_moderation.types import Annotation


class PubAnnotationTests(unittest.TestCase):
    def test_round_trip_annotations(self) -> None:
        annotations = [
            Annotation(start=0, end=8, text="diabetes", entity="Disease"),
        ]

        doc = annotations_to_pubannotation(
            text="diabetes is chronic",
            annotations=annotations,
            sourcedb="PubMed",
            sourceid="123",
            project="https://pubannotation.org/projects/example",
        )
        restored = pubannotation_to_annotations(doc)

        self.assertEqual(len(restored), 1)
        self.assertEqual(restored[0].text, "diabetes")
        self.assertEqual(restored[0].entity, "Disease")


if __name__ == "__main__":
    unittest.main()
