from httpx import Response
import respx

mock_api = respx.mock(
    assert_all_mocked=False, assert_all_called=False, base_url="http://api.vwa.com"
)
valid_collection = {
    "info": {
        "name": "invalid collection",
        "_postman_id": "my-collection-id",
        "schema": "https://schema.getpostman.com/#2.0.0",
        "version": {
            "major": "2",
            "minor": "0",
            "patch": "0",
            "prerelease": "draft.1",
        },
    },
    "variable": [
        {"id": "var-1", "type": "string", "value": "hello-world"},
    ],
    "item": [
        {
            "id": "request-200",
            "description": {
                "content": "<h1>This is H1</h1><script>test toString()</script>",
                "version": "2.0.1-abc+efg",
            },
            "name": "200 ok",
            "request": "http://echo.getpostman.com/status/200",
        }
    ],
}
mock_api.get("http://example.postman.com/schema").mock(
    Response(200, headers={"content-type": "application/json"}, json=valid_collection)
)
