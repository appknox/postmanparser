import pytest

from postmanparser.collection import Collection
from postmanparser.exceptions import MissingRequiredFieldException


def test_collection_events_should_match_with_json_coll_events(collection, json_data):
    assert len(collection.event) == len(json_data["event"])


def test_collection_event_values_should_match_with_json_coll_event_values(
    collection, json_data
):
    json_event = json_data["event"]
    for i, event in enumerate(collection.event):
        assert event.listen == json_event[i]["listen"]
        assert event.id == json_event[i].get("id", "")
        assert event.disabled == json_event[i].get("disabled", False)
        assert event.script.script_type == json_event[i]["script"]["type"]
        assert event.script.script_exec == json_event[i]["script"]["exec"]
        assert event.script.id == json_event[i]["script"].get("id", "")
        assert event.script.name == json_event[i]["script"].get("name", "")


def test_collection_event_should_be_none_if_no_event_present():
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
    assert collection.event is None


def test_collection_event_sould_have_listen_prop():
    invalid_coll = {
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
        "event": [
            {
                "id": "my-global-script-1",
                "script": {"type": "text/javascript", "exec": 'console.log("hello");'},
            }
        ],
    }
    collection = Collection()
    with pytest.raises(MissingRequiredFieldException):
        collection.parse(invalid_coll)
