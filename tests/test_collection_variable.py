def test_collection_variable(collection, json_data):
    variable = collection.variable
    assert len(variable) == 5
    for i, var in enumerate(json_data["variable"]):
        assert variable[i].id == var["id"]
        if "type" in var:
            assert variable[i].variable_type == var["type"]
        if "value" in var:
            assert variable[i].value == var["value"]
