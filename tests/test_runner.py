from __future__ import annotations

import importlib.util
import unittest
from pathlib import Path

from test_support import REPO_ROOT


SCRIPT_PATH = REPO_ROOT / "scripts" / "run_moderation_round.py"
SPEC = importlib.util.spec_from_file_location("run_moderation_round", SCRIPT_PATH)
MODULE = importlib.util.module_from_spec(SPEC)
assert SPEC is not None and SPEC.loader is not None
SPEC.loader.exec_module(MODULE)


class RunnerTests(unittest.TestCase):
    def test_parser_accepts_spec_without_direct_inputs(self) -> None:
        parser = MODULE.build_parser()
        args = parser.parse_args(["--spec", "examples/experiment_spec.example.json"])

        self.assertEqual(args.spec, "examples/experiment_spec.example.json")
        self.assertIsNone(args.input)
        self.assertIsNone(args.guidelines)
        self.assertIsNone(args.entities)
        self.assertIsNone(args.output_dir)

    def test_build_provider_supports_known_backends(self) -> None:
        with self.assertRaises(ValueError):
            MODULE._build_provider("unknown", "model")


if __name__ == "__main__":
    unittest.main()
