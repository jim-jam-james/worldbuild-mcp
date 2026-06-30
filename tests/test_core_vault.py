import pytest
import yaml

from worldbuild_core.schema import build_schema
from worldbuild_core.vault import init_vault


def test_init_vault_creates_structure(tmp_path):
    init_vault(tmp_path)

    assert (tmp_path / ".worldbuild" / "schema.yaml").exists()

    assert (tmp_path / "Characters").is_dir()
    assert (tmp_path / "Factions").is_dir()
    assert (tmp_path / "Locations").is_dir()
    assert (tmp_path / "Events").is_dir()
    assert (tmp_path / "Items").is_dir()
    assert (tmp_path / "Lore").is_dir()

    reloaded = build_schema(yaml.safe_load((tmp_path / ".worldbuild" / "schema.yaml").read_text()))
    assert reloaded.get_type("Character") is not None


def test_init_vault_refuses_existing(tmp_path):
    init_vault(tmp_path)

    with pytest.raises(FileExistsError):
        init_vault(tmp_path)
