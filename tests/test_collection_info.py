import pytest

from postmanparser.collection import Collection
from postmanparser.exceptions import MissingRequiredFieldException


def test_collection_info(collection, json_data):
    info = collection.info
    assert info.name == json_data["info"]["name"]
    assert info.schema == json_data["info"]["schema"]
    assert info.version.major == json_data["info"]["version"]["major"]
    assert info.version.minor == json_data["info"]["version"]["minor"]
    assert info.version.patch == json_data["info"]["version"]["patch"]


def test_collection_info_missing_major_ver_should_throw_error():
    invalid_collection = {
        "info": {
            "name": "invalid collection",
            "id": "my-collection-id",
            "schema": "https://schema.getpostman.com/#2.0.0",
            "version": {
                "minor": "0",
                "patch": "0",
                "prerelease": "draft.1",
            },
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
    with pytest.raises(MissingRequiredFieldException):
        collection.parse(invalid_collection)


def test_collection_info_missing_minor_ver_should_throw_error():
    invalid_collection = {
        "info": {
            "name": "invalid collection",
            "id": "my-collection-id",
            "schema": "https://schema.getpostman.com/#2.0.0",
            "version": {
                "major": "2",
                "patch": "0",
                "prerelease": "draft.1",
            },
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
    with pytest.raises(MissingRequiredFieldException):
        collection.parse(invalid_collection)


def test_collection_info_missing_patch_ver_should_throw_error():
    invalid_collection = {
        "info": {
            "name": "invalid collection",
            "id": "my-collection-id",
            "schema": "https://schema.getpostman.com/#2.0.0",
            "version": {
                "major": "2",
                "minor": "0",
                "prerelease": "draft.1",
            },
        },
        "variable": [
            {"id": "var-1", "type": "string", "value": "hello-world"},
        ],
        "item": [
            {
                "id": "request-200",
                "description": {
                    "content": "<script>this will be dropped in toString()</script>",
                    "version": "2.0.1-abc+efg",
                },
                "name": "200 ok",
                "request": "http://echo.getpostman.com/status/200",
            }
        ],
    }
    collection = Collection()
    with pytest.raises(MissingRequiredFieldException):
        collection.parse(invalid_collection)
