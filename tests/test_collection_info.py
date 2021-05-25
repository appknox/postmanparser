def test_collection_info(collection, json_data):
    info = collection.info
    assert info.name == json_data["info"]["name"]
    assert info.schema == json_data["info"]["schema"]
    assert info.version.major == json_data["info"]["version"]["major"]
    assert info.version.minor == json_data["info"]["version"]["minor"]
    assert info.version.patch == json_data["info"]["version"]["patch"]
