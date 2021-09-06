from postmanparser.collection import Collection
from postmanparser.constants import AuthType


def test_collection_auth_empty_root_auth_should_return_none():
    coll = {
        "info": {
            "name": "invalid collection",
            "id": "my-collection-id",
            "schema": "https://schema.getpostman.com/#2.0.0",
        },
        "variable": [
            {"id": "var-1", "type": "string", "value": "hello-world"},
        ],
        "item": [
            {
                "id": "request-200",
                "description": {
                    "content": "<script>test toString()</script>",
                    "version": "2.0.1-abc+efg",
                },
                "name": "200 ok",
                "request": "http://echo.getpostman.com/status/200",
            }
        ],
    }
    collection = Collection()
    collection.parse(coll)
    assert collection.auth is None


def test_collection_auth_empty_root_auth_should_return_none():
    coll = {
        "info": {
            "name": "invalid collection",
            "id": "my-collection-id",
            "schema": "https://schema.getpostman.com/#2.0.0",
        },
        "variable": [
            {"id": "var-1", "type": "string", "value": "hello-world"},
        ],
        "auth": {
            "type": "apikey",
            "apikey": [
                {
                    "key": "value",
                    "value": "API_VALUE",
                    "type": "string"
                },
                {
                    "key": "key",
                    "value": "API_KEY",
                    "type": "string"
                }
            ]
        },
        "item": [
            {
                "id": "request-200",
                "description": {
                    "content": "<script>test toString()</script>",
                    "version": "2.0.1-abc+efg",
                },
                "name": "200 ok",
                "request": "http://echo.getpostman.com/status/200",
            }
        ],
    }
    collection = Collection()
    collection.parse(coll)
    assert collection.auth is not None
    assert collection.auth.auth_type == AuthType.APIKEY.value
    for auth_type in AuthType:
        if auth_type.value == AuthType.APIKEY.value:
            assert collection.auth.auth_type is not None
        else:
            assert getattr(collection.auth, auth_type.value) is None
