from importlib.resources import files
from pathlib import Path

import yaml

from worldbuild_core.schema import build_schema


def default_schema_text() -> str:
    return files("worldbuild_core").joinpath("default_schema.yaml").read_text(encoding="utf-8")


def init_vault(path: Path) -> None:
    schema_text = default_schema_text()
    schema = build_schema(yaml.safe_load(schema_text))

    worldbuild_dir = path / ".worldbuild"
    schema_file = worldbuild_dir / "schema.yaml"
    if schema_file.exists():
        raise FileExistsError(f"Vault already initialized: {schema_file}")

    worldbuild_dir.mkdir(parents=True, exist_ok=True)
    schema_file.write_text(schema_text, encoding="utf-8")

    for type_spec in schema.types.values():
        (path / type_spec.folder).mkdir(parents=True, exist_ok=True)
