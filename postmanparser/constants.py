from enum import Enum


class BaseEnum(Enum):
    @classmethod
    def has_value(cls, value):
        for enum in cls:
            if enum.value == value:
                return True
        return False


class RequestBodyMode(BaseEnum):
    RAW = "raw"
    URLENCODED = "urlencoded"
    FORMDATA = "formdata"
    FILE = "file"
    GRAPHQL = "graphql"


class VariableType(BaseEnum):
    STRING = "string"
    BOOLEAN = "boolean"
    ANY = "any"
    NUMBER = "number"


class AuthType(BaseEnum):
    APIKEY = "apikey"
    AWSV4 = "awsv4"
    BASIC = "basic"
    BEARER = "bearer"
    DIGEST = "digest"
    EDGEGRID = "edgegrid"
    HAWK = "hawk"
    NOAUTH = "noauth"
    OAUTH1 = "oauth1"
    OAUTH2 = "oauth2"
    NTLM = "ntlm"
