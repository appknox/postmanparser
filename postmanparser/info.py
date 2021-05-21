from dataclasses import dataclass


@dataclass
class Info:
    name: str = ""
    schema: str = ""
    postman_id: str = ""

    @classmethod
    def parse(cls, data: dict):
        return cls(
            name=data.get("name", ""),
            schema=data.get("schema", ""),
            postman_id=data.get("_postman_id", ""),
        )