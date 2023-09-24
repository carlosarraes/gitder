from dataclasses import dataclass, field
from typing import Self


@dataclass
class Repos:
    full_name: str
    description: str
    language: str
    created_at: str
    updated_at: str
    size: int
    stargazers_count: int
    watchers_count: int
    forks_count: int
    languages: dict[str, int] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, json_dict: dict) -> Self:
        field_names = {f.name for f in cls.__dataclass_fields__.values()}
        filtered_json = {k: v for k, v in json_dict.items() if k in field_names}
        return cls(**filtered_json)
