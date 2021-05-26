from dataclasses import dataclass
from typing import Any
from typing import Union

from postmanparser.constants import VariableType
from postmanparser.description import Description
from postmanparser.exceptions import InvalidPropertyValueException
from postmanparser.exceptions import MissingRequiredFieldException


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
        if id is None and key is None:
            raise MissingRequiredFieldException(
                " 'variable' should have either 'id' or 'key' property"
            )
        var_type = data.get("type")
        if var_type is not None:
            if not VariableType.has_value(var_type):
                values = [e.value for e in VariableType]
                raise InvalidPropertyValueException(
                    f"Invalid value of 'type' property of 'Variable' object."
                    f" Must be one of the {','.join(values)}"
                )
        description = data.get("description")
        if isinstance(description, dict):
            description = Description.parse(description)

        return cls(
            id=id,
            key=key,
            value=data.get("value"),
            variable_type=data.get("type", "any"),
            name=data.get("name", ""),
            description=description,
            system=data.get("system", False),
        )
