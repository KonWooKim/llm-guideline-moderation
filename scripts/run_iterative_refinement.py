from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from llm_guideline_moderation.artifacts import write_json
from llm_guideline_moderation.evaluation import PubAnnotationEvaluatorOptions
from llm_guideline_moderation.experiment import ExperimentSpec
from llm_guideline_moderation.iterative import run_iterative_refinement
from llm_guideline_moderation.layout import prepare_run_layout
from llm_guideline_moderation.providers.deepseek import DeepSeekProvider
from llm_guideline_moderation.providers.gemini import GeminiProvider
from llm_guideline_moderation.providers.openai import OpenAIProvider
from llm_guideline_moderation.sampling import sample_pubannotation_documents
from llm_guideline_moderation.types import EntityDefinition, OutputConfiguration


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run iterative guideline refinement on a random train subset."
    )
    parser.add_argument("--spec", required=True, help="Path to experiment spec JSON")
    parser.add_argument("--threshold-f1", type=float, help="Override the strict-match micro F1 stopping threshold from the spec")
    parser.add_argument("--n-examples", type=int, help="Override the prompt evidence example count from the spec")
    parser.add_argument(
        "--provider",
        choices=["openai", "gemini", "deepseek"],
        help="Override provider from the spec",
    )
    parser.add_argument("--model", help="Override model from the spec")
    parser.add_argument("--output-dir", help="Override output directory from the spec")
    return parser


def _build_provider(provider_name: str, model_name: str):
    if provider_name == "openai":
        return OpenAIProvider(model=model_name)
    if provider_name == "gemini":
        return GeminiProvider(model=model_name)
    if provider_name == "deepseek":
        return DeepSeekProvider(model=model_name)
    raise ValueError(f"Unsupported provider: {provider_name}")


def main() -> None:
    args = build_parser().parse_args()
    spec = ExperimentSpec.from_json_file(args.spec)

    provider_name = args.provider or spec.model.provider
    model_name = args.model or spec.model.model
    output_root = args.output_dir or spec.paths.output_dir
    source_dir = spec.moderation_sampling.source_dir_path
    sample_size = spec.moderation_sampling.sample_size or 10
    seed = spec.moderation_sampling.seed
    threshold_f1 = args.threshold_f1 if args.threshold_f1 is not None else spec.iterative.threshold_f1
    n_examples = args.n_examples if args.n_examples is not None else spec.iterative.n_examples

    guidelines = Path(spec.paths.guidelines_txt).read_text(encoding="utf-8")
    entity_rows = json.loads(Path(spec.paths.entity_schema_json).read_text(encoding="utf-8"))
    entities = [
        EntityDefinition(name=row) if isinstance(row, str) else EntityDefinition(**row)
        for row in entity_rows
    ]

    sampled_documents = sample_pubannotation_documents(
        source_dir,
        sample_size=sample_size,
        seed=seed,
    )
    provider = _build_provider(provider_name, model_name)
    result = run_iterative_refinement(
        sampled_documents=sampled_documents,
        guidelines=guidelines,
        entities=entities,
        provider=provider,
        threshold_f1=threshold_f1,
        n_examples=n_examples,
        output_configuration=OutputConfiguration(
            include_rationale=True,
            include_guideline_section=True,
        ),
        evaluation_options=PubAnnotationEvaluatorOptions(
            soft_match_characters=0,
            soft_match_words=0,
        ),
    )

    layout = prepare_run_layout(output_root, f"{spec.experiment_id}_iterative")
    write_json(layout["inputs"] / "experiment_spec.json", spec.to_json_dict())
    write_json(
        layout["inputs"] / "sampled_train_documents.json",
        [
            {
                "filename": document.filename,
                "sourceid": document.sourceid,
                "path": document.path,
            }
            for document in sampled_documents
        ],
    )
    Path(layout["inputs"] / "initial_guidelines.txt").write_text(guidelines, encoding="utf-8")
    write_json(layout["inputs"] / "entity_schema.json", entity_rows)
    write_json(layout["final"] / "iterative_refinement_run.json", result)
    Path(layout["final"] / "final_guidelines.txt").write_text(result.final_guidelines, encoding="utf-8")
    write_json(
        layout["links"] / "reader_links.json",
        {
            "pubannotation_evaluation": spec.evaluation_url,
        },
    )

    for snapshot in result.iterations:
        round_dir = layout["rounds"] / f"iteration_{snapshot.iteration:02d}"
        round_dir.mkdir(parents=True, exist_ok=True)
        write_json(round_dir / "snapshot.json", snapshot)
        for prompt_name, prompt_text in snapshot.prompts.items():
            (round_dir / f"{prompt_name}.txt").write_text(prompt_text, encoding="utf-8")


if __name__ == "__main__":
    main()
