from postmanparser.collection import Collection
import pytest


def test_collection_request():
    collection = Collection()
    collection.parse_from_file("tests/data/collection-request.json")
    print(collection)
