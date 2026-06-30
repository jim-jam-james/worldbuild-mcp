import pytest
import yaml

from worldbuild_core.entities import mint_uid
from worldbuild_core.models import Entity
from worldbuild_core.schema import build_schema
from worldbuild_core.vault import init_vault, read_entity, write_entity


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


def test_file_write_round_trip(tmp_path):
    entity = Entity(
        uid=mint_uid("Character", "Name"),
        type="Character",
        name="Name",
        frontmatter={
            "aliases": "An Alias",
            "member_of": ["[[Faction]]"],
            "located_in": "[[Location]]",
        },
        body="Body",
    )

    character_file = tmp_path / "Name.md"
    write_entity(character_file, entity=entity)
    reloaded = read_entity(character_file)

    assert entity.uid == reloaded.uid
    assert reloaded.name == "Name"
    assert entity.type == reloaded.type
    assert entity.frontmatter == reloaded.frontmatter
    assert entity.body == reloaded.body
