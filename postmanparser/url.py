from dataclasses import dataclass
from typing import List, Union

from .key_val import KeyVal
from .variable import Variable


@dataclass
class Url:
    raw: str
    protocol: str
    port: str
    host: Union[str, List[str]] = ""
    path: Union[str, List[str]] = ""
    query: List[KeyVal] = None
    url_hash: str = ""
    variable: List[Variable] = None

    @classmethod
    def parse(cls, data: dict):
        protocol = data.get("protocol", "")
        port = ""
        if protocol == "http":
            port = "80"
        if protocol == "https":
            port = "443"
        query = data.get("query", None)
        if query:
            query = [KeyVal.parse(_) for _ in query]
        return cls(
            data.get("raw", ""),
            data.get("protocol", ""),
            port,
            host=data.get("host", ""),
            path=data.get("path", ""),
            query=query,
            url_hash=data.get("hash", ""),
        )
