from dataclasses import dataclass
from typing import List


@dataclass
class AuthAttribute:
    key: str
    value = None
    auth_attr_type: str = None

    @classmethod
    def parse(cls, data: dict):
        key = data.get("key")
        if key is None:
            raise Exception("auth-attribute object should have 'key' property")
        return cls(key, value=data.get("value"), auth_attr_type=data.get("type"))


@dataclass
class Auth:
    auth_type: str
    no_auth = None
    apikey: List[AuthAttribute] = None
    awsv4: List[AuthAttribute] = None
    basic: List[AuthAttribute] = None
    bearer: List[AuthAttribute] = None
    digest: List[AuthAttribute] = None
    edgegrid: List[AuthAttribute] = None
    hawk: List[AuthAttribute] = None
    noauth: List[AuthAttribute] = None
    oauth1: List[AuthAttribute] = None
    oauth2: List[AuthAttribute] = None
    ntlm: List[AuthAttribute] = None
