# postmanparser

## Introduction

Postman collection parser written in python3 to extract HTTP requests/responses.
Currently supports reading JSON schema two ways
- Read from `.json` file
- Fetch from url where schema is exposed

## Installation
 - Using pip

        pip install postmanparser

- Using poetry

        poetry add postmanparser

## Getting Started

### Parsing API Schema
You can parse API schema from file or from url as below.
- From file

```python
from postmanparser import Collection
collection = Collection()
collection.parse_from_file("path/to/postman/schema.json")
```

- From url

```python
from postmanparser import Collection
collection = Collection()
collection.parse_from_url("http://example.com/schema")
```
URL should be a `GET` request.

postmanparser also validates for the required fields mentioned by postman schema documentation which is available at https://schema.postman.com/

### Reading the data
Postman collection contains group of requests and one or more folders having group of requests and/or nested folders in it.

You can access requests in the collections as shown in below.
```python
for item in collection.item:
        if isinstance(item, ItemGroup):
                continue #skip folders
        print(item.request)
```
`item.request` could be a string or of type `Request` with all the attributes of requests according to schema.

### Validation
If schema found to be invalid following exception will be thrown.
- `MissingRequiredFieldException`
- `InvalidPropertyValueException`
- `InvalidObjectException`

## Schema Support
postmanparser is still in early stages and will be updated with missing schema components soon.

### Version
postmanparser supports collection schema v2.0.0 and v2.1.0.

### Object support
postmanparser currently does not support parsing of following objects. Might be added in future.

- events
- protocolProfileBehavior