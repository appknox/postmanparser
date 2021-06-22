from dataclasses import dataclass
from typing import List
from typing import Union

from postmanparser.exceptions import MissingRequiredFieldException
from postmanparser.url import Url


@dataclass
class Script:
    id: str = ""
    script_type: str = ""
    script_exec: Union[List[str], str] = ""
    src: Url = None
    name: str = ""

    @classmethod
    def parse(cls, data: dict):
        url = data.get("url")
        if url:
            url = Url.parse(url)
        return cls(
            id=data.get("id", ""),
            script_type=data.get("type", ""),
            script_exec=data.get("exec", ""),
            src=url,
            name=data.get("name", ""),
        )


@dataclass
class Event:
    listen: str
    id: str = ""
    script: Script = None
    disabled: bool = False

    @classmethod
    def parse(cls, data: dict):
        listen = data.get("listen")
        if listen is None:
            raise MissingRequiredFieldException(
                "'event' object must contain 'listen' key"
            )
        return cls(
            listen=listen,
            id=data.get("id", ""),
            script=Script.parse(data.get("script")) if "script" in data else None,
            disabled=data.get("disabled", False),
        )
