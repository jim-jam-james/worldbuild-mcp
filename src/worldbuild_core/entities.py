import re
import secrets
from typing import Any

import yaml

from worldbuild_core.models import Entity


def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_")


def mint_uid(type_name: str, name: str) -> str:
    return f"{type_name.lower()}_{slugify(name)}_{secrets.token_hex(2)}"


def serialize_entity(entity: Entity) -> str:
    fm = {"type": entity.type, "uid": entity.uid, **entity.frontmatter}
    fm_text = yaml.safe_dump(fm, sort_keys=False, allow_unicode=True)
    return f"---\n{fm_text}---\n\n{entity.body}".rstrip() + "\n"


def parse_entity(text: str, name: str) -> Entity:
    _, fm_text, body = text.split("---", 2)
    fm: dict[str, Any] = yaml.safe_load(fm_text) or {}
    type_ = fm.pop("type")
    uid = fm.pop("uid")
    return Entity(uid=uid, type=type_, name=name, frontmatter=fm, body=body.strip("\n"))
