from postmanparser.collection import Collection
from .mock_server import mock_api
from .mock_server import valid_collection


@mock_api
def test_valid_collection_should_be_parsed_from_url():
    collection = Collection()
    collection.parse_from_url("http://example.postman.com/schema")
    assert collection.info.postman_id == valid_collection["info"]["_postman_id"]
