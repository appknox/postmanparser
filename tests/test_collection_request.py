import pytest

from postmanparser.collection import Collection
from postmanparser.exceptions import FolderNotFoundError
from postmanparser.item import ItemGroup


def test_collection_item_req_fields_should_match_json_item_req(
    collection,
    json_data,
):
    json_item = json_data["item"]
    for idx, itm in enumerate(collection.item):
        if type(itm) is ItemGroup:
            continue
        json_req = json_item[idx].get("request")
        if isinstance(json_req, str):
            assert itm.request == json_req
            continue
        assert itm.request.method == json_req["method"]
        assert itm.request.url == json_req["url"]
        json_req_header = json_req.get("header", "")
        if isinstance(json_req_header, list):
            for idx, header in enumerate(json_req_header):
                assert itm.request.header[idx].key == header["key"]
                assert itm.request.header[idx].value == header["value"]
        else:
            assert itm.request.header == json_req_header


def test_collection_item_req_body_should_match_json_item_req_body(
    collection, json_data
):
    json_item = json_data["item"]
    for idx, itm in enumerate(collection.item):
        if type(itm) is ItemGroup:
            continue
        json_req = json_item[idx].get("request")
        if isinstance(json_req, str):
            assert itm.request == json_req
            continue
        json_req_body = json_req.get("body")
        if not json_req_body:
            assert itm.request.body is None
            continue
        assert itm.request.body.mode == json_req_body["mode"]
        if json_req_body["mode"] == "raw":
            assert itm.request.body.raw == json_req_body["raw"]
        if json_req_body["mode"] == "urlencoded":
            for idx, keyval in enumerate(json_req_body["urlencoded"]):
                assert itm.request.body.urlencoded[idx].key == keyval["key"]
                assert itm.request.body.urlencoded[idx].value == keyval["value"]


def test_collection_item_req_auth_should_match_json_item_req_auth(
    collection, json_data
):
    json_items = json_data["item"]
    for idx, itm in enumerate(collection.item):
        if type(itm) is not ItemGroup:
            continue
        json_item = json_items[idx]
        for i, item in enumerate(itm.item):
            if type(item) is ItemGroup:
                continue
            json_req = json_item["item"][i].get("request")
            if isinstance(json_req, str):
                assert item.request == json_req
                continue
            json_req_auth = json_req.get("auth")
            if not json_req_auth:
                assert item.request.auth is None
                continue
            json_req_auth_type = json_req_auth["type"]
            assert item.request.auth.auth_type == json_req_auth_type
            auth_attrs = getattr(item.request.auth, json_req_auth_type)
            keyval = json_req_auth.get(json_req_auth_type)
            if auth_attrs is None:
                continue
            for auth_attr in auth_attrs:
                assert auth_attr.key in keyval
                assert auth_attr.value == keyval[auth_attr.key]
                assert auth_attr.auth_attr_type == keyval.get("type", "")


def test_collection_get_requests_should_return_all_requests_at_root_lvl(collection):
    assert len(collection.get_requests()) == 2
    assert len(collection.get_requests("This is a folder")) == 3


def test_get_requests_with_folder_should_return_all_request_at_folder_lvl(collection):
    assert len(collection.get_requests(folder="This is a folder/my-folder-2")) == 0


def test_get_requests_with_invalid_folder_name_should_raise_exception(collection):
    with pytest.raises(FolderNotFoundError):
        collection.get_requests(folder="InvalidFolderName")


def test_get_requests_with_recursive_true_should_return_req_map(collection):
    req_map = collection.get_requests(folder="This is a folder", recursive=True)
    assert "This is a folder" in req_map
    assert "This is a folder/my-folder-2" in req_map
    assert "This is a folder/my-folder-2/This is a blank" in req_map
    assert "This is a folder/my-folder-2/Solo Folder" in req_map
    assert len(req_map["This is a folder"]) == 3
    assert len(req_map["This is a folder/my-folder-2"]) == 0
    assert len(req_map["This is a folder/my-folder-2/This is a blank"]) == 1
    assert len(req_map["This is a folder/my-folder-2/Solo Folder"]) == 1


def test_get_requests_with_recursive_true_should_return_req_map_root_lvl(collection):
    req_map = collection.get_requests(recursive=True)
    assert "/" in req_map
    assert "This is a folder" in req_map
    assert "This is a folder/my-folder-2" in req_map
    assert "This is a folder/my-folder-2/This is a blank" in req_map
    assert "This is a folder/my-folder-2/Solo Folder" in req_map
    assert len(req_map["/"]) == 2
    assert len(req_map["This is a folder"]) == 3
    assert len(req_map["This is a folder/my-folder-2"]) == 0
    assert len(req_map["This is a folder/my-folder-2/This is a blank"]) == 1
    assert len(req_map["This is a folder/my-folder-2/Solo Folder"]) == 1


def test_collection_get_requests_should_return_0_requests_for_empty_item():
    _collection = {
        "info": {
            "name": "invalid collection",
            "id": "my-collection-id",
            "schema": "https://schema.getpostman.com/#2.0.0",
            "version": {
                "minor": "0",
                "patch": "0",
                "major": "1",
                "prerelease": "draft.1",
            },
        },
        "variable": [
            {"id": "var-1", "type": "string", "value": "hello-world"},
        ],
        "item": [],
    }
    collection = Collection()
    collection.parse(_collection)
    assert len(collection.get_requests()) == 0
