from dataclasses import dataclass


@dataclass
class Description:
    text: str = ""
    desc_type: str = ""
    version: str = ""

    @classmethod
    def parse(cls, data: dict):
        return cls(
            text=data.get("text", ""),
            desc_type=data.get("type", ""),
            version=data.get("version", ""),
        )