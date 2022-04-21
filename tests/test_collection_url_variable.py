from postmanparser.collection import Collection


def test_get_url_variables():
    _collection = {
        "info": {
            "_postman_id": "9c76aeae-011c-4327-96c4-17146aacd14d",
            "name": "example",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [{
            "name": "example",
            "request": {
                "method": "GET",
                "header": [],
                "url": {
                    "raw": "https://example.com/status/:id",
                    "protocol": "https",
                    "host": ["example", "com"],
                    "path": ["status", ":id"],
                    "variable": [{
                        "key": "id",
                        "value": "1"
                    }]
                }
            },
            "response": []
        }]
    }

    collection = Collection()
    collection.parse(_collection)

    assert len(collection.item) == 1

    url = collection.item[0].request.url
    assert isinstance(url.variable, list) and len(url.variable) == 1
    assert url.variable[0].key == "id"
    assert url.variable[0].value == "1"


def test_empty_variabes_should_return_none(collection):
    _collection = {
        "info": {
            "_postman_id": "9c76aeae-011c-4327-96c4-17146aacd14d",
            "name": "example",
            "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json"
        },
        "item": [{
            "name": "example",
            "request": {
                "method": "GET",
                "header": [],
                "url": {
                    "raw": "https://example.com/status/",
                    "protocol": "https",
                    "host": ["example", "com"],
                    "path": ["status"]
                }
            },
            "response": []
        }]
    }

    collection = Collection()
    collection.parse(_collection)

    assert len(collection.item) == 1

    url = collection.item[0].request.url
    assert url.variable is None