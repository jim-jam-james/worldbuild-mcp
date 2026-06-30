import pytest

from worldbuild_core.schema import SchemaError, build_schema


def test_build_minimal_schema():
    schema = build_schema({"version": 1, "types": {"Lore": {"folder": "Lore"}}})
    assert schema.version == 1
    lore = schema.get_type("Lore")
    assert lore is not None
    assert lore.folder == "Lore"
    assert "name" in lore.required


def test_relationship_parsing():
    schema = build_schema(
        {
            "version": 1,
            "types": {
                "Character": {
                    "folder": "Characters",
                    "relationships": {
                        "member_of": {
                            "target": "Faction",
                            "cardinality": "many",
                            "inverse": "members"
                        }
                    },
                },
                "Faction": {
                    "folder": "Factions",
                }
            },
        }
    )
    assert schema.version == 1
    character = schema.get_type("Character")
    assert character is not None
    relationships = character.relationships
    member_of = relationships["member_of"]
    assert member_of.target == "Faction"
    assert member_of.cardinality == "many"
    assert member_of.inverse == "members"
    assert member_of.derived is False


def test_missing_version_rejected():
    with pytest.raises(SchemaError):
        build_schema({"types": {"Lore": {"folder": "Lore"}}})
