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
from llm_guideline_moderation.experiment import ExperimentSpec
from llm_guideline_moderation.layout import prepare_run_layout
from llm_guideline_moderation.pipeline import simulate_moderation_iterations
from llm_guideline_moderation.providers.gemini import GeminiProvider
from llm_guideline_moderation.providers.openai import OpenAIProvider
from llm_guideline_moderation.pubannotation import (
    annotations_to_pubannotation,
    pubannotation_to_annotations,
)
from llm_guideline_moderation.types import (
    EntityDefinition,
    ModerationRoundInput,
    OutputConfiguration,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run guideline refinement / moderation simulation on one PubAnnotation document."
    )
    parser.add_argument("--spec", help="Path to experiment spec JSON")
    parser.add_argument("--input", help="Path to input PubAnnotation JSON")
    parser.add_argument("--guidelines", help="Path to current guidelines text file")
    parser.add_argument("--entities", help="Path to entity schema JSON")
    parser.add_argument("--output-dir", help="Directory for artifacts")
    parser.add_argument("--provider", default="openai", choices=["openai", "gemini"], help="LLM provider")
    parser.add_argument("--model", default="gpt-5", help="OpenAI model name")
    parser.add_argument("--rounds", type=int, default=1, help="Number of moderation rounds")
    parser.add_argument("--project-link", default="", help="PubAnnotation project URL for readers")
    parser.add_argument("--evaluation-link", default="", help="PubAnnotation evaluation URL for readers")
    parser.add_argument("--discrepancy-examples", default="", help="Optional discrepancy evidence text")
    parser.add_argument("--true-positive-examples", default="", help="Optional true-positive evidence text")
    parser.add_argument("--raw-examples", default="", help="Optional raw corpus context text")
    parser.add_argument("--verified-examples", default="", help="Optional protected examples text")
    return parser


def _build_provider(provider_name: str, model_name: str):
    if provider_name == "openai":
        return OpenAIProvider(model=model_name)
    if provider_name == "gemini":
        return GeminiProvider(model=model_name)
    raise ValueError(f"Unsupported provider: {provider_name}")


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.spec:
        spec = ExperimentSpec.from_json_file(args.spec)
        input_path = spec.paths.input_pubannotation
        guidelines_path = spec.paths.guidelines_txt
        entities_path = spec.paths.entity_schema_json
        output_dir_arg = spec.paths.output_dir
        model_name = spec.model.model
        provider_name = spec.model.provider
        rounds = spec.model.rounds
        project_link = spec.pubannotation.project_url
        evaluation_link = spec.pubannotation.evaluation_url
        collection_link = spec.pubannotation.collection_url
        discrepancy_examples = spec.evidence.discrepancy_examples
        true_positive_examples = spec.evidence.true_positive_examples
        raw_examples = spec.evidence.raw_examples
        verified_examples = spec.evidence.verified_examples
        experiment_id = spec.experiment_id
        experiment_meta = spec.to_json_dict()
    else:
        missing = [
            name
            for name, value in (
                ("--input", args.input),
                ("--guidelines", args.guidelines),
                ("--entities", args.entities),
                ("--output-dir", args.output_dir),
            )
            if not value
        ]
        if missing:
            parser.error(
                "the following arguments are required unless --spec is provided: "
                + ", ".join(missing)
            )
        input_path = args.input
        guidelines_path = args.guidelines
        entities_path = args.entities
        output_dir_arg = args.output_dir
        model_name = args.model
        provider_name = args.provider
        rounds = args.rounds
        project_link = args.project_link
        evaluation_link = args.evaluation_link
        collection_link = ""
        discrepancy_examples = args.discrepancy_examples
        true_positive_examples = args.true_positive_examples
        raw_examples = args.raw_examples
        verified_examples = args.verified_examples
        experiment_id = Path(input_path).stem
        experiment_meta = None

    input_doc = json.loads(Path(input_path).read_text(encoding="utf-8"))
    guidelines = Path(guidelines_path).read_text(encoding="utf-8")
    entity_rows = json.loads(Path(entities_path).read_text(encoding="utf-8"))

    entities = [EntityDefinition(**row) for row in entity_rows]
    initial_annotations = pubannotation_to_annotations(input_doc)

    provider = _build_provider(provider_name, model_name)
    round_input = ModerationRoundInput(
        text=input_doc["text"],
        guidelines=guidelines,
        initial_annotations=initial_annotations,
        entities=entities,
        discrepancy_examples=discrepancy_examples,
        true_positive_examples=true_positive_examples,
        raw_examples=raw_examples,
        verified_examples=verified_examples,
        output_configuration=OutputConfiguration(
            include_rationale=True,
            include_guideline_section=True,
        ),
    )

    result = simulate_moderation_iterations(
        initial_input=round_input,
        provider=provider,
        num_rounds=rounds,
    )

    layout = prepare_run_layout(output_dir_arg, experiment_id)

    write_json(layout["inputs"] / "input.pubann.json", input_doc)
    Path(layout["inputs"] / "guidelines.txt").write_text(guidelines, encoding="utf-8")
    write_json(layout["inputs"] / "entity_schema.json", entity_rows)
    if experiment_meta is not None:
        write_json(layout["inputs"] / "experiment_spec.json", experiment_meta)

    for round_result in result.rounds:
        round_dir = layout["rounds"] / f"round_{round_result.round_index:02d}"
        round_dir.mkdir(parents=True, exist_ok=True)
        write_json(round_dir / "result.json", round_result)
        for prompt_name, prompt_text in round_result.prompts.items():
            Path(round_dir / f"{prompt_name}.txt").write_text(prompt_text, encoding="utf-8")

    write_json(layout["final"] / "moderation_run.json", result)
    Path(layout["final"] / "final_guidelines.txt").write_text(
        result.final_guidelines,
        encoding="utf-8",
    )
    write_json(
        layout["final"] / "final_annotations.pubann.json",
        annotations_to_pubannotation(
            text=input_doc["text"],
            annotations=result.final_annotations,
            sourcedb=input_doc.get("sourcedb", "unknown"),
            sourceid=input_doc.get("sourceid", "unknown"),
            project=input_doc.get("project"),
            target=input_doc.get("target"),
        ),
    )
    write_json(
        layout["links"] / "reader_links.json",
        {
            "pubannotation_collection": collection_link,
            "pubannotation_project": project_link,
            "pubannotation_evaluation": evaluation_link,
        },
    )


if __name__ == "__main__":
    main()
