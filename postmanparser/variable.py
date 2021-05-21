from dataclasses import dataclass
from postmanparser.constants import VariableType
from postmanparser.description import Description
from typing import Any, Union


@dataclass
class Variable:
    id: str
    key: str
    value: Union[str, bool, int, Any] = None
    variable_type: str = "any"
    name: str = ""
    description: Description = None
    system: bool = False

    @classmethod
    def parse(cls, data: dict):
        id = data.get("id")
        key = data.get("key")
        if id is None or key is None:
            raise Exception("variable should have 'id' and 'key'")
        var_type = data.get("type")
        if var_type is not None:
            if not VariableType.has_value(var_type):
                values = [e.value for e in VariableType]
                raise Exception(
                    f"Invalid value of 'type' property of 'Variable' object. Must be one of the {','.join(values)}"
                )

        return cls(
            id=id,
            key=key,
            value=data.get("value"),
            variable_type=data.get("type", "any"),
            name=data.get("name", ""),
            description=Description.parse(data.get("description", {})),
            system=data.get("system", False),
        )
