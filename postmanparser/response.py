from dataclasses import dataclass
from typing import List, Union

from .request import Request
from .key_val import KeyVal


@dataclass
class Response:
    id: str = ""
    original_request: Request = None
    response_time: Union[str, int, None] = None
    timings: Union[dict, None] = None
    header: Union[List[KeyVal], List[str], str, None] = None
    cookie: Union[List[KeyVal], None] = None
    body: Union[str, None] = None
    status: str = ""
    code: int = -1

    @classmethod
    def parse(cls, data: dict):
        return cls(
            id=data.get("id", ""), original_request=data.get("original-request", "")
        )
