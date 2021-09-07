from postmanparser.collection import Collection
from postmanparser.constants import AuthType


def test_collection_auth_empty_root_auth_should_return_none():
    coll = {
        "info": {
            "name": "valid collection",
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


def test_collection_auth_parse_root_auth_should_return_apikey_object():
    coll = {
        "info": {
            "name": "valid collection",
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
    assert getattr(collection.auth, AuthType.APIKEY.value) is not None
    assert len(collection.auth.apikey) == 2
    assert collection.auth.apikey[0].key is not None
    assert collection.auth.apikey[1].key is not None

