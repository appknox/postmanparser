from dataclasses import dataclass
from typing import Union

from postmanparser.description import Description
from postmanparser.exceptions import MissingRequiredFieldException


@dataclass
class Version:
    major: str
    minor: str
    patch: str
    identifier: str = ""

    @classmethod
    def parse(cls, data: dict):
        major = data.get("major")
        minor = data.get("minor")
        patch = data.get("patch")
        if not major:
            raise MissingRequiredFieldException(
                "'version' object should have 'major' property"
            )
        if not minor:
            raise MissingRequiredFieldException(
                "'version' object should have 'minor' property"
            )
        if not patch:
            raise MissingRequiredFieldException(
                "'version' object should have 'patch' property"
            )
        return cls(major, minor, patch, identifier=data.get("identifier", ""))


@dataclass
class Info:
    name: str = ""
    schema: str = ""
    postman_id: str = ""
    description: Union[Description, str, None] = None
    version: Union[Version, str, None] = None

    @classmethod
    def parse(cls, data: dict):
        name = data.get("name", "")
        schema = data.get("schema", "")
        if not name:
            raise MissingRequiredFieldException(
                "'info' object should have 'name' property"
            )
        if not schema:
            raise MissingRequiredFieldException(
                "'info' object should have 'schema' property"
            )
        description = data.get("description")
        if isinstance(description, dict):
            description = Description.parse(description)

        version = data.get("version")
        if isinstance(version, dict):
            version = Version.parse(version)

        return cls(
            name=name,
            schema=schema,
            postman_id=data.get("_postman_id", ""),
            description=description,
            version=version,
        )
