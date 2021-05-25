from postmanparser.proxy_config import ProxyConfig
from postmanparser.item import ItemGroup
from postmanparser.description import Description


def test_collection_no_of_item_should_match_with_json_items(collection, json_data):
    item_group = collection.item[2]
    json_item = json_data["item"]
    assert len(collection.item) == 3
    assert type(item_group) == ItemGroup
    assert item_group.name == json_item[2]["name"]
    assert len(item_group.item) == 4


def test_collection_valid_item_fields_should_match_with_json_item(
    collection, json_data
):
    json_item = json_data["item"]
    i = 0
    for itm in collection.item:
        if type(itm) is ItemGroup:
            continue
        assert itm.id == json_item[i].get("id", "")
        assert itm.name == json_item[i].get("name", "")
        i += 1


def test_collection_valid_item_description_should_match_with_json_item(
    collection, json_data
):
    json_item = json_data["item"]
    i = 0
    for itm in collection.item:
        if type(itm) is ItemGroup:
            continue
        json_desc = json_item[i].get("description")
        if not json_desc:
            assert itm.descrption == None
        elif isinstance(json_desc, str):
            assert itm.description == json_desc
        else:
            assert itm.description.content == json_desc.get("content", "")
            assert itm.description.desc_type == json_desc.get("type", "")
            assert itm.description.version == json_desc.get("version", "")
        i += 1


def test_collection_valid_item_should_have_request(collection, json_data):
    json_item = json_data["item"]
    i = 0
    for itm in collection.item:
        if type(itm) is ItemGroup:
            continue
        json_req = json_item[i].get("request")
        if isinstance(json_req, str):
            assert itm.request == json_req
        else:
            assert itm.request is not None
        i += 1


def test_collection_valid_item_no_of_responses_should_match_with_json_item(
    collection, json_data
):
    json_item = json_data["item"]
    i = 0
    for itm in collection.item:
        if type(itm) is ItemGroup:
            continue
        json_resp = json_item[i].get("response")
        if json_resp:
            assert len(itm.response) == len(json_resp)
        else:
            assert itm.response == None
        i += 1
