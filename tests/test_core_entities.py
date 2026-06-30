from worldbuild_core.entities import mint_uid, parse_entity, serialize_entity, slugify
from worldbuild_core.models import Entity


def test_slugify():
    assert slugify("James") == "james"
    assert slugify("Aldric the Gray") == "aldric_the_gray"
    assert slugify("K'sh'tal") == "k_sh_tal"


def test_mint_uid():
    assert mint_uid("Character", "James").startswith("character_")
    assert mint_uid("Faction", "The Graybeards").startswith("faction_")
    assert mint_uid("Character", "Sauron") != mint_uid("Character", "Sauron")


def test_build_entity():
    entity = Entity(mint_uid("Character", "Mario"), "Character", "Mario", {}, "")

    assert entity.uid is not None
    assert entity.type == "Character"
    assert entity.name == "Mario"
    assert entity.frontmatter is not None
    assert entity.body is not None


def test_entity_round_trip():
    entity = Entity(
        uid=mint_uid("Character", "Name"),
        type="Character",
        name="Name",
        frontmatter={
            "aliases": "[An Alias]",
            "member_of": ["[[Faction]]"],
            "located_in": "[[Location]]",
        },
        body="Body",
    )

    serial = serialize_entity(entity)
    parsed = parse_entity(serial, "Name")

    assert entity.uid == parsed.uid
    assert entity.type == parsed.type
    assert entity.name == parsed.name
    assert entity.frontmatter == parsed.frontmatter
    assert entity.body == parsed.body
