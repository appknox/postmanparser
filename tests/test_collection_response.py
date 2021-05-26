from postmanparser.item import ItemGroup


def test_collection_item_resp_should_match_json_item_resp(collection, json_data):
    json_item = json_data["item"]
    for idx, itm in enumerate(collection.item):
        if type(itm) is ItemGroup:
            continue
        json_resp = json_item[idx].get("response")
        if not json_resp:
            assert itm.response == None
        for i, resp in enumerate(json_resp):
            assert itm.response[i].id == resp.get("id", "")
            assert itm.response[i].response_time == resp.get("responseTime")
            assert itm.response[i].header == resp.get("header")
            assert itm.response[i].body == resp.get("body")
            assert itm.response[i].status == resp.get("status", "")
            assert itm.response[i].code == resp.get("code", 0)


def test_collection_item_resp_cookie_should_match_json_item_resp_cookie(
    collection, json_data
):
    json_item = json_data["item"]
    for idx, itm in enumerate(collection.item):
        if type(itm) is ItemGroup:
            continue
        json_resp = json_item[idx].get("response")
        if not json_resp:
            assert itm.response == None
        for i, resp in enumerate(json_resp):
            json_resp_cookie = resp.get("cookie")
            if not json_resp_cookie:
                assert itm.response[i].cookie == None
            for j, cookie in enumerate(json_resp_cookie):
                assert itm.response[i].cookie[j].domain == cookie["domain"]
                assert itm.response[i].cookie[j].path == cookie["path"]
                assert itm.response[i].cookie[j].expires == cookie.get("expires")
                assert itm.response[i].cookie[j].max_age == cookie.get("maxAge", "")
                assert itm.response[i].cookie[j].host_only == cookie.get(
                    "hostOnly", False
                )
                assert itm.response[i].cookie[j].http_only == cookie.get(
                    "httpOnly", False
                )
                assert itm.response[i].cookie[j].name == cookie.get("name", "")
                assert itm.response[i].cookie[j].secure == cookie.get("secure", False)
                assert itm.response[i].cookie[j].session == cookie.get("session", False)
                assert itm.response[i].cookie[j].value == cookie.get("value", "")
