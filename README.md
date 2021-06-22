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

#### Getting requests from the collection

You can retreive all the requests present in the collection using `get_requests()` method.
This method will recursively search for the requests inside folders is present.

```python
collection = Collection()
collection.parse_from_file("path/to/postman/schema.json")
requests = collection.get_requests()
for request in requests:
        print(request) #Either a Request object or str
```

You can retrieve the requests inside specific folder by using `folder="folder_name"` in `get_requests` method. To get requests from the nested folder, use folder path separated by `/`

For e.g. to get requests inside folder2 which is nested in folder1
```python
requests = collection.get_requests(folder="folder/sub_folder")
```

You can pass `recursive=False` to `get_requests()` if you don't want to do recusrive lookup. In this case
you will get all the requests present at the root level of collection or at the folder level is folder is specified.

```python
requests = collection.get_requests(recursive=False)
```

#### Getting requests mapped by folder in the collection
You can access requests in the collections as requests map using `get_requests_map()`. The key of the dict is path to the folder separated by backlash and value is list of requests of type `Request` or `str`.
This will be recursive search for all the folders and sub folders inside it.

```python
collection = Collection()
collection.parse_from_file("path/to/postman/schema.json")
requests = collection.get_requests_map()
requests = collection.get_requests_map(folder="folder/sub_folder")
```

### Validation
If schema found to be invalid following exception will be thrown.
- `MissingRequiredFieldException`
- `InvalidPropertyValueException`
- `InvalidObjectException`
- `FolderNotFoundException`

## Schema Support
postmanparser is still in early stages and will be updated with missing schema components soon.

Following are the objects which are not supported yet but will be added in the future.
- protocolProfileBehavior

## Collection SDK Compatibility

Currently postmanparser is not aligned with collection SDK node module. http://www.postmanlabs.com/postman-collection/

This Might be added in future. Feel free to raise the PR.


## Version Compatibility
postmanparser supports collection schema v2.0.0 and v2.1.0.