from dataclasses import dataclass


@dataclass
class ProxyConfig:
    match: str = "http+https://*/*"
    host: str = ""
    port: int = 8080
    tunnel: bool = False
    disabled: bool = False

    @classmethod
    def parse(cls, data):
        cls(
            match=data.get("match", "http+https://*/*"),
            host=data.get("host", ""),
            port=data.get("port", 8080),
            tunnel=data.get("tunnel", False),
            disabled=data.get("disabled", False),
        )

    def get_proxy_url(self):
        return f"{self.host}:{self.port}"
