import json

import pytest

from postmanparser import Collection

COLLECTION_V2_FILE = "tests/data/collection-request.json"


@pytest.fixture
def collection():
    collection = Collection()
    collection.parse_from_file(COLLECTION_V2_FILE)
    return collection


@pytest.fixture
def json_data():
    with open(COLLECTION_V2_FILE, "r") as f:
        return json.loads(f.read())
