from dataclasses import dataclass
from typing import Any
from typing import List

from postmanparser.constants import AuthType
from postmanparser.exceptions import InvalidPropertyValueException
from postmanparser.exceptions import MissingRequiredFieldException


@dataclass
class AuthAttribute:
    key: str
    value: Any = None
    auth_attr_type: str = ""

    @classmethod
    def parse(cls, data: dict):
        key = data.get("key")
        if key is None:
            raise MissingRequiredFieldException(
                "auth-attribute object should have 'key' property"
            )
        return cls(key, value=data.get("value"), auth_attr_type=data.get("type", ""))


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

    @classmethod
    def parse(cls, data: dict):
        auth_type = data.get("type")
        if auth_type is None:
            MissingRequiredFieldException(" 'auth' object should have 'type' property.")
        auth_type_values = [e.value for e in AuthType]
        if not AuthType.has_value(auth_type):
            InvalidPropertyValueException(
                f"Invalid value of 'type' property of 'auth' object."
                f" Must be one of the {auth_type_values}"
            )
        cls_instance = cls(auth_type)
        for key in data:
            if key not in auth_type_values:
                continue
            auth_data = data[key]
            is_list = isinstance(auth_data, list)
            is_dict = isinstance(auth_data, dict)
            if not is_list and not is_dict:
                InvalidPropertyValueException(
                    f"Invalid value of '{key}' property' of 'auth' object. "
                    f"Must be an object or list of objects."
                )
            attr_list = []
            if is_list:
                # It should be supporting auth attribute object
                for _data in auth_data:
                    attr_list.append(AuthAttribute.parse(_data))
            if is_dict:
                for auth_key in auth_data:
                    attr_list.append(
                        AuthAttribute(
                            auth_key,
                            value=auth_data[auth_key],
                            auth_attr_type=(auth_data.get("type", "")),
                        )
                    )
            setattr(cls_instance, key, attr_list)
        return cls_instance
