from __future__ import annotations
from dataclasses import dataclass
from typing import List, Union


from .request import Request
from .response import Response
from .description import Description
from .variable import Variable
from .auth import Auth
from .exceptions import (
    InvalidPropertyValueException,
    MissingRequiredFieldException,
    InvalidObjectException,
)


@dataclass
class Item:
    """
    Corresponds to single API endpoint
    """

    request: Union[Request, str]
    id: str = ""
    name: str = ""
    description: Union[Description, str, None] = None
    response: List[Response] = None

    @classmethod
    def parse(cls, data: dict):
        _request = data.get("request")
        if _request is None:
            raise Exception(
                "Invalid postman collection: item must contain 'request' key"
            )
        if isinstance(_request, dict):
            request = Request.parse(data["request"])
        elif isinstance(_request, str):
            request = _request
        else:
            raise InvalidPropertyValueException(
                "value of 'request' property should be string or request object"
            )

        response = None
        if "response" in data:
            response_list = data["response"]
            response = [Response.parse(resp) for resp in response_list]

        description = data.get("description")
        if isinstance(description, dict):
            description = Description.parse(description)

        return cls(
            request,
            id=data.get("id", ""),
            name=data.get("name", ""),
            description=description,
            response=response,
        )


@dataclass
class ItemGroup:
    item: List[Union[Item, ItemGroup]]
    name: str = ""
    description: Description = None
    variable: Variable = None
    auth: Auth = None

    @classmethod
    def parse(cls, data):
        item_list = data.get("item")
        items = []
        if item_list is None:
            raise MissingRequiredFieldException(
                "'item-group' object should have 'item' property"
            )
        items = parse_item_list(item_list)

        description = data.get("description")
        if isinstance(description, dict):
            description = Description.parse(description)

        return cls(
            item=items,
            name=data.get("name", ""),
            description=description,
            variable=Variable.parse(data["variable"]) if "variable" in data else None,
            auth=Auth.parse(data["auth"]) if "auth" in data else None,
        )


def parse_item_list(item_list: List[dict]) -> List[Union[Item, ItemGroup]]:
    items = []
    for item in item_list:
        request = item.get("request")
        _item = item.get("item")
        if _item and request:
            InvalidObjectException(
                "Invalid item in collection. Object cannot be either 'item' or 'item-group' and not both"
            )
        elif request is not None:
            items.append(Item.parse(item))
        elif _item is not None:
            items.append(ItemGroup.parse(item))
        else:
            InvalidObjectException(
                "Invalid item in collection. Object should be either 'item' or 'item-group'"
            )
    return items
