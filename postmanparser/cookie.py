from dataclasses import dataclass
from typing import List
from typing import Union

from postmanparser.exceptions import MissingRequiredFieldException


@dataclass
class Cookie:
    domain: str
    path: str
    expires: Union[str, None] = None
    max_age: str = ""
    host_only: bool = False
    http_only: bool = False
    name: str = ""
    secure: bool = False
    session: bool = False
    value: str = ""
    extensions: List = None

    @classmethod
    def parse(cls, data: dict):
        domain = data.get("domain")
        path = data.get("path")
        if domain is None or path is None:
            raise MissingRequiredFieldException(
                "'cookie' object should have 'domain' and 'path' property."
            )
        return cls(
            domain,
            path,
            expires=data.get("expires"),
            max_age=data.get("maxAge", ""),
            host_only=data.get("hostOnly", False),
            http_only=data.get("httpOnly", False),
            name=data.get("name", ""),
            secure=data.get("secure", False),
            session=data.get("session", False),
            value=data.get("value", ""),
            extensions=data.get("extensions"),
        )
