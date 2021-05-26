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
                itm.request.header[idx].key == header["key"]
                itm.request.header[idx].value == header["value"]
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
            for idx, auth_attr in enumerate(auth_attrs):
                assert auth_attr.key in keyval
                assert auth_attr.value == keyval[auth_attr.key]
                assert auth_attr.auth_attr_type == keyval.get("type", "")
