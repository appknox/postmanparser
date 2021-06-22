from __future__ import annotations

from dataclasses import dataclass
from typing import List
from typing import Union

from postmanparser.auth import Auth
from postmanparser.description import Description
from postmanparser.event import Event
from postmanparser.exceptions import InvalidObjectException
from postmanparser.exceptions import InvalidPropertyValueException
from postmanparser.exceptions import MissingRequiredFieldException
from postmanparser.request import Request
from postmanparser.response import Response
from postmanparser.variable import Variable


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
    event: List[Event] = None

    @classmethod
    def parse(cls, data: dict):
        _request = data.get("request")
        event = data.get("event", [])
        if _request is None:
            raise MissingRequiredFieldException(
                "'item' object must contain 'request' key"
            )
        if isinstance(_request, dict):
            request = Request.parse(data["request"])
        elif isinstance(_request, str):
            request = _request
        else:
            raise InvalidPropertyValueException(
                "Value of 'request' property should be string or request object"
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
            event=[Event.parse(_) for _ in event] if event else None,
        )


@dataclass
class ItemGroup:
    item: List[Union[Item, ItemGroup]]
    name: str = ""
    description: Description = None
    variable: Variable = None
    auth: Auth = None
    event: List[Event] = None

    @classmethod
    def parse(cls, data):
        item_list = data.get("item")
        items = []
        if item_list is None:
            raise MissingRequiredFieldException(
                "'item-group' object should have 'item' property"
            )
        items = parse_item_list(item_list)
        event = data.get("event", [])
        description = data.get("description")
        if isinstance(description, dict):
            description = Description.parse(description)

        return cls(
            item=items,
            name=data.get("name", ""),
            description=description,
            variable=Variable.parse(data["variable"]) if "variable" in data else None,
            auth=Auth.parse(data["auth"]) if "auth" in data else None,
            event=[Event.parse(_) for _ in event] if event else None,
        )


def parse_item_list(item_list: List[dict]) -> List[Union[Item, ItemGroup]]:
    items = []
    for item in item_list:
        request = item.get("request")
        _item = item.get("item")
        if _item and request:
            InvalidObjectException(
                "Invalid item in collection. "
                "Object cannot be either 'item' or 'item-group' and not both"
            )
        elif request is not None:
            items.append(Item.parse(item))
        elif _item is not None:
            items.append(ItemGroup.parse(item))
        else:
            InvalidObjectException(
                "Invalid item in collection. "
                "Object should be either 'item' or 'item-group'"
            )
    return items
