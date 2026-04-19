from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
SRC_ROOT = REPO_ROOT / "src"
if str(SRC_ROOT) not in sys.path:
    sys.path.insert(0, str(SRC_ROOT))

from llm_guideline_moderation.dataset_annotation import annotate_pubannotation_directory
from llm_guideline_moderation.providers.deepseek import DeepSeekProvider
from llm_guideline_moderation.providers.gemini import GeminiProvider
from llm_guideline_moderation.providers.openai import OpenAIProvider
from llm_guideline_moderation.types import EntityDefinition


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Annotate every PubAnnotation JSON file in a directory with the final refined guidelines."
    )
    parser.add_argument("--input-dir", required=True, help="Directory containing PubAnnotation JSON files")
    parser.add_argument("--guidelines", required=True, help="Path to the final guidelines text file")
    parser.add_argument("--entities", required=True, help="Path to the entity schema JSON file")
    parser.add_argument("--output-dir", required=True, help="Directory where annotated PubAnnotation JSON files will be written")
    parser.add_argument("--provider", default="openai", choices=["openai", "gemini", "deepseek"], help="LLM provider")
    parser.add_argument("--model", default="gpt-5", help="Model name")
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
    guidelines = Path(args.guidelines).read_text(encoding="utf-8")
    entity_rows = json.loads(Path(args.entities).read_text(encoding="utf-8"))
    entities = [
        EntityDefinition(name=row) if isinstance(row, str) else EntityDefinition(**row)
        for row in entity_rows
    ]
    provider = _build_provider(args.provider, args.model)
    annotate_pubannotation_directory(
        input_dir=args.input_dir,
        output_dir=args.output_dir,
        guidelines=guidelines,
        entities=entities,
        provider=provider,
    )


if __name__ == "__main__":
    main()
