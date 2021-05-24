from __future__ import annotations
from dataclasses import dataclass
from postmanparser.constants import RequestBodyMode
from typing import List, Union

from postmanparser.key_val import KeyVal
from postmanparser.description import Description
from postmanparser.form_parameter import FormParameter
from postmanparser.url import Url
from postmanparser.auth import Auth
from postmanparser.proxy_config import ProxyConfig
from postmanparser.certificate import Certificate


@dataclass
class Request:
    url: Union[Url, str]
    method: str
    auth: Auth = None
    proxy: ProxyConfig = None
    certificate: Certificate = None
    header: Union[List[KeyVal], str] = ""
    body: Union[RequestBody, None] = None
    description: Description = None

    @classmethod
    def parse(cls, data: dict):
        header = ""
        headers = data.get("header")
        if headers:
            if isinstance(headers, list):
                header = [KeyVal.parse(_) for _ in headers]
        body = None
        if "body" in data:
            body = RequestBody.parse(data["body"])
        auth = Auth.parse(data["auth"]) if "auth" in data else None
        proxy = ProxyConfig.parse(data["proxy"]) if "proxy" in data else None
        certificate = Auth.parse(data["certificate"]) if "certificate" in data else None

        url = data.get("url", "")
        if isinstance(url, dict):
            url = Url.parse(url)

        description = data.get("description")
        if isinstance(description, dict):
            description = Description.parse(description)

        return cls(
            url,
            data.get("method", ""),
            auth=auth,
            proxy=proxy,
            certificate=certificate,
            header=header,
            body=body,
            description=description,
        )


@dataclass
class RequestBody:
    mode: str  # [raw, urlencoded, formdata, file, graphql]
    raw: str = ""
    urlencoded: List[KeyVal] = None
    graphql: dict = None
    formdata: Union[List[FormParameter]] = None
    request_body_file: Union[RequestBodyFile, None] = None
    options: dict = None
    disabled: bool = False

    @classmethod
    def parse(cls, data: dict):
        if "mode" not in data:
            raise Exception("Request body should have 'mode' property")
        mode = data["mode"]
        if not RequestBodyMode.has_value(mode):
            values = [e.value for e in RequestBodyMode]
            raise Exception(
                f"Invalid value of 'mode' property. Must be one of the {','.join(values)}"
            )
        raw = ""
        urlencoded = None
        if mode == "raw":
            raw = data.get("raw", "")
        elif mode == "urlencoded":
            urlencoded = [
                KeyVal.parse(key_val) for key_val in data.get("urlencoded", [])
            ]
        return cls(mode=mode, raw=raw, urlencoded=urlencoded)


@dataclass
class RequestBodyFile:
    src: Union[str, None] = None
    content: str = ""

    @classmethod
    def parse(cls, data: dict):
        return cls()
