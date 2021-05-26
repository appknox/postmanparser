from dataclasses import dataclass
from typing import List


@dataclass
class CertificateKey:
    src: str

    @classmethod
    def parse(cls, data: dict):
        return cls(data.get("src", ""))


@dataclass
class Certificate:
    name: str = ""
    matches: List[str] = None
    key: CertificateKey = ""
    passphrase: str = ""

    @classmethod
    def parse(cls, data: dict):
        return cls(
            name=data.get("name", ""),
            matches=data.get("matches", None),
            key=CertificateKey.parse(data.get("key", {})),
            passphrase=data.get("passphrase", ""),
        )
