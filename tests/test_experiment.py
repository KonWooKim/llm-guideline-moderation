from __future__ import annotations

import json
import unittest
from pathlib import Path

from test_support import SRC_ROOT  # noqa: F401
from workspace import workspace_tmpdir

from llm_guideline_moderation.experiment import ExperimentSpec
from llm_guideline_moderation.layout import prepare_run_layout

EXPERIMENTS_DIR = Path(__file__).resolve().parents[1] / "experiments"


class ExperimentTests(unittest.TestCase):
    def test_experiment_spec_loads_from_json(self) -> None:
        payload = {
            "experiment_id": "exp_001",
            "dataset_name": "NCBI Disease",
            "split": "test",
            "pubannotation": {
                "collection_url": "https://pubannotation.org/collections/a",
                "project_url": "https://pubannotation.org/projects/a",
                "evaluation_url": "https://pubannotation.org/projects/b",
            },
            "paths": {
                "input_pubannotation": "input.json",
                "guidelines_txt": "guidelines.txt",
                "entity_schema_json": "entities.json",
                "output_dir": "outputs",
            },
            "moderation_sampling": {
                "source_project_url": "",
                "source_archive_path": "data/archives/ncbi-train.zip",
                "source_split": "train",
                "sampling_method": "random",
                "sample_size": 10,
                "seed": 42,
                "shared_across_models": True,
                "selection_note": "Randomly sample 10 training examples and reuse them across models.",
            },
        }

        with workspace_tmpdir() as tmpdir:
            path = Path(tmpdir) / "spec.json"
            path.write_text(json.dumps(payload), encoding="utf-8")
            spec = ExperimentSpec.from_json_file(path)

        self.assertEqual(spec.experiment_id, "exp_001")
        self.assertEqual(spec.dataset_name, "NCBI Disease")
        self.assertEqual(spec.pubannotation.collection_url, "https://pubannotation.org/collections/a")
        self.assertEqual(spec.pubannotation.project_url, "https://pubannotation.org/projects/a")
        self.assertEqual(spec.moderation_sampling.sample_size, 10)
        self.assertEqual(spec.moderation_sampling.sampling_method, "random")
        self.assertEqual(spec.moderation_sampling.source_split, "train")
        self.assertTrue(spec.moderation_sampling.shared_across_models)

    def test_prepare_run_layout_creates_expected_directories(self) -> None:
        with workspace_tmpdir() as tmpdir:
            layout = prepare_run_layout(tmpdir, "exp_001")

            self.assertTrue(layout["run_root"].exists())
            self.assertTrue(layout["inputs"].exists())
            self.assertTrue(layout["rounds"].exists())
            self.assertTrue(layout["final"].exists())
            self.assertTrue(layout["links"].exists())

    def test_runnable_experiment_specs_load_as_valid_specs(self) -> None:
        spec_names = [
            "ncbi_disease_valid_round1.spec.json",
            "bc5cdr_valid_round1.spec.json",
            "biored_valid_round1.spec.json",
        ]

        for spec_name in spec_names:
            with self.subTest(spec_name=spec_name):
                spec = ExperimentSpec.from_json_file(EXPERIMENTS_DIR / spec_name)
                self.assertTrue(spec.experiment_id.endswith("round1"))
                self.assertEqual(spec.model.rounds, 1)
                self.assertTrue(spec.paths.guidelines_txt.startswith("data/guidelines/"))
                self.assertIsNotNone(spec.moderation_sampling.sample_size)
                self.assertTrue(spec.moderation_sampling.shared_across_models)


if __name__ == "__main__":
    unittest.main()
