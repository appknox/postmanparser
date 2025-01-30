import pytest

from postmanparser.collection import Collection
from postmanparser.exceptions import MissingRequiredFieldException
from postmanparser.item import Item
from postmanparser.item import ItemGroup


def test_collection_no_of_item_should_match_with_json_items(collection, json_data):
    item_group = collection.item[2]
    json_item = json_data["item"]
    assert len(collection.item) == 3
    assert isinstance(item_group, ItemGroup)
    assert item_group.name == json_item[2]["name"]
    assert len(item_group.item) == 4


def test_collection_valid_item_fields_should_match_with_json_item(
    collection, json_data
):
    json_item = json_data["item"]
    for i, itm in enumerate(collection.item):
        if type(itm) is ItemGroup:
            continue
        assert itm.id == json_item[i].get("id", "")
        assert itm.name == json_item[i].get("name", "")


def test_collection_valid_item_description_should_match_with_json_item(
    collection, json_data
):
    json_item = json_data["item"]
    for i, itm in enumerate(collection.item):
        if type(itm) is ItemGroup:
            continue
        json_desc = json_item[i].get("description")
        if not json_desc:
            assert itm.descrption is None
        elif isinstance(json_desc, str):
            assert itm.description == json_desc
        else:
            assert itm.description.content == json_desc.get("content", "")
            assert itm.description.desc_type == json_desc.get("type", "")
            assert itm.description.version == json_desc.get("version", "")


def test_collection_valid_item_should_have_request(collection, json_data):
    json_item = json_data["item"]
    for i, itm in enumerate(collection.item):
        if type(itm) is ItemGroup:
            continue
        json_req = json_item[i].get("request")
        if isinstance(json_req, str):
            assert itm.request == json_req
        else:
            assert itm.request is not None


def test_collection_valid_item_no_of_responses_should_match_with_json_item(
    collection, json_data
):
    json_item = json_data["item"]
    for i, itm in enumerate(collection.item):
        if type(itm) is ItemGroup:
            continue
        json_resp = json_item[i].get("response")
        if json_resp:
            assert len(itm.response) == len(json_resp)
        else:
            assert itm.response is None


def test_collection_missing_item_should_throws_exception():
    invalid_collection = {
        "info": {
            "name": "invalid collection",
            "id": "my-collection-id",
            "schema": "https://schema.getpostman.com/#2.0.0",
            "version": {
                "major": "2",
                "minor": "0",
                "patch": "0",
                "prerelease": "draft.1",
            },
        },
        "variable": [
            {"id": "var-1", "type": "string", "value": "hello-world"},
        ],
    }
    collection = Collection()
    with pytest.raises(MissingRequiredFieldException):
        collection.parse(invalid_collection)


def test_collection_missing_info_should_throws_exception():
    invalid_collection = {
        "variable": [
            {"id": "var-1", "type": "string", "value": "hello-world"},
        ],
        "item": [
            {
                "id": "request-200",
                "description": {
                    "content": "<h1>This is H1</h1> <script>test toString()</script>",
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


def test_collection_item_event_should_match_with_json_coll_itm_events(
    collection, json_data
):
    json_item = json_data["item"]
    for i, itm in enumerate(collection.item):
        if isinstance(itm, Item):
            assert len(itm.event) == len(json_item[i]["event"])


def test_collection_item_grp_event_should_be_none_if_no_json_coll_itm_grp_events(
    collection,
):
    for itm in collection.item:
        if isinstance(itm, ItemGroup):
            assert itm.event is None
