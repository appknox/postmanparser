from dataclasses import dataclass
from typing import Union

from postmanparser.description import Description


@dataclass
class KeyVal:
    key: str
    value: str
    disabled: bool = False
    description: Union[Description, None, str] = None

    @classmethod
    def parse(cls, data: dict):
        description = data.get("description")
        if isinstance(description, dict):
            description = Description.parse(description)
        return cls(
            data.get("key", ""),
            data.get("value", ""),
            disabled=data.get("disabled", False),
            description=description,
        )
