from dataclasses import dataclass
from typing import Union

from .description import Description


@dataclass
class KeyVal:
    key: str
    value: str
    disabled: bool = False
    description: Union[Description, None, str] = None

    @classmethod
    def parse(cls, data: dict):
        desc = data.get("description", None)
        if desc:
            desc = Description.parse(desc)
        return cls(
            data.get("key", ""),
            data.get("value", ""),
            disabled=data.get("disabled", False),
            description=desc,
        )
