from dataclasses import dataclass
from typing import List
from typing import Union

from postmanparser.description import Description
from postmanparser.exceptions import InvalidObjectException
from postmanparser.exceptions import MissingRequiredFieldException


@dataclass
class FormParameter:
    key: str
    value: str = ""
    src: Union[List, str, None] = None
    disabled: bool = False
    form_param_type: str = ""
    content_type: str = ""  # should override content-type in header
    description: Union[Description, None, str] = None

    @classmethod
    def parse(cls, data: dict):
        key = data.get("key")
        if key is None:
            raise MissingRequiredFieldException(
                "'formparameter' object should have 'key' property"
            )
        value = data.get("value", "")
        src = data.get("src")
        if value and src is not None:
            raise InvalidObjectException(
                "'formparamter' object can eiher have src or value and not both."
            )
        description = data.get("description")
        if isinstance(description, dict):
            description = Description.parse(description)
        return cls(
            key,
            value=value,
            src=src,
            disabled=data.get("disabled", False),
            form_param_type=data.get("type", ""),
            content_type=data.get("contentType", ""),
            description=description,
        )
