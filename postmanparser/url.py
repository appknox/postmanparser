from dataclasses import dataclass
from typing import List
from typing import Union

from postmanparser.key_val import KeyVal
from postmanparser.variable import Variable


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

        query = data.get("query", [])
        if query:
            query = [KeyVal.parse(_) for _ in query]

        variable = data.get("variable", [])
        if variable:
            variable = [Variable.parse(_) for _ in variable]

        return cls(
            data.get("raw", ""),
            data.get("protocol", ""),
            port,
            host=data.get("host", ""),
            path=data.get("path", ""),
            query=query,
            url_hash=data.get("hash", ""),
            variable=variable,
        )
