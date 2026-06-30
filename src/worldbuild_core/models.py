from dataclasses import dataclass, field
from typing import Any


@dataclass
class Entity:
    uid: str
    type: str
    name: str
    frontmatter: dict[str, Any] = field(default_factory=dict)
    body: str = ""
