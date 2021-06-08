# postmanparser
![Build](https://github.com/appknox/postmanparser/actions/workflows/test.yml/badge.svg)
[![codecov](https://codecov.io/gh/appknox/postmanparser/branch/main/graph/badge.svg?token=BXCg5XODJw)](https://codecov.io/gh/appknox/postmanparser)

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

#### Getting requests from the collection at root level

You can retreive all the requests present in the collection at root level using `get_requests()` method.

```python
collection = Collection()
collection.parse_from_file("path/to/postman/schema.json")
requests = collection.get_requests()
for request in requests:
        print(request) #Either a Request object or str
```

#### Getting requests by folder in the collection

You can retrieve the requests inside specific folder by using `folder="folder_name"` in `get_requests` method. To get requests from the nested folder, use folder path separated by `/`

For e.g. to get requests inside folder2 which is nested in folder1


```python
collection = Collection()
collection.parse_from_file("path/to/postman/schema.json")
requests = collection.get_requests(folder="folder1")
requests = collection.get_requests(folder="folder1/folder2")

```


#### Getting requests recursively from specified path

You can access requests in the collections as requests map using `recursive=True`. The key of the dict is path to the folder separated by backlash and value is list of requests of type `Request` or `str`.
```python
collection = Collection()
collection.parse_from_file("path/to/postman/schema.json")
requests = collection.get_requests(folder="folder1", recursive=True)

```

### Validation
If schema found to be invalid following exception will be thrown.
- `MissingRequiredFieldException`
- `InvalidPropertyValueException`
- `InvalidObjectException`
- `FolderNotFoundException`

## Schema Support
postmanparser is still in early stages and will be updated with missing schema components soon.

### Version
postmanparser supports collection schema v2.0.0 and v2.1.0.

### Object support
postmanparser currently does not support parsing of following objects. Might be added in future.

- events
- protocolProfileBehavior