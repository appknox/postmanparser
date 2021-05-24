from dataclasses import dataclass


@dataclass
class Description:
    content: str = ""
    desc_type: str = ""
    version: str = ""

    @classmethod
    def parse(cls, data: dict):
        return cls(
            content=data.get("content", ""),
            desc_type=data.get("type", ""),
            version=data.get("version", ""),
        )
