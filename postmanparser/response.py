from dataclasses import dataclass
from typing import List
from typing import Union

from postmanparser.cookie import Cookie
from postmanparser.key_val import KeyVal
from postmanparser.request import Request


@dataclass
class Response:
    id: str = ""
    original_request: Request = None
    response_time: Union[str, int, None] = None
    timings: Union[dict, None] = None
    header: Union[List[Union[KeyVal, str]], str, None] = None
    cookie: Union[List[Cookie], None] = None
    body: Union[str, None] = None
    status: str = ""
    code: int = 0

    @classmethod
    def parse(cls, data: dict):
        header = data.get("header")
        header_list = []
        if header and isinstance(header, list):
            for _header in header:
                if isinstance(_header, dict):
                    header_list.append(KeyVal.parse(_header))
                else:
                    header_list.append(_header)
        cookie = data.get("cookie")
        cookie_list = []
        if cookie:
            for _cookie in cookie:
                cookie_list.append(Cookie.parse(_cookie))

        return cls(
            id=data.get("id", ""),
            original_request=data.get("original-request", ""),
            response_time=data.get("responseTime"),
            timings=data.get("timings"),
            header=header_list if header_list else header,
            cookie=cookie_list if cookie_list else None,
            body=data.get("body"),
            status=data.get("status", ""),
            code=data.get("code", 0),
        )
