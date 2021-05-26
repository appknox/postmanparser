def test_collection_variable(collection, json_data):
    variable = collection.variable
    assert len(variable) == 5
    i = 0
    for var in json_data["variable"]:
        variable[i].id == var["id"]
        if "type" in var:
            variable[i].variable_type = var["type"]
        if "value" in var:
            variable[i].variable_type = var["value"]
        i = +1
