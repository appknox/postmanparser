from dataclasses import dataclass
from dataclasses import field
import json
from typing import List
from typing import Union

import httpx

from postmanparser.auth import Auth
from postmanparser.exceptions import MissingRequiredFieldException
from postmanparser.info import Info
from postmanparser.item import Item
from postmanparser.item import ItemGroup
from postmanparser.item import parse_item_list
from postmanparser.variable import Variable


@dataclass
class Collection:
    file_path: str = ""
    variable: List[Variable] = None
    auth: Auth = None
    info: Info = field(init=False)
    item: List[Union[Item, ItemGroup]] = field(init=False)

    def validate(self, data):
        if "info" not in data or "item" not in data:
            raise MissingRequiredFieldException(
                "Invalid Postman collection: Required 'info' and 'item' "
                "properties in 'collection' object"
            )

    def parse(self, data: dict):
        self.validate(data)
        self.item = parse_item_list(data["item"])
        self.info = Info.parse(data["info"])
        var_list = data.get("variable", [])
        if not var_list:
            return
        self.variable = []
        for var in var_list:
            self.variable.append(Variable.parse(var))

    def parse_from_file(self, file_path):
        self.file_path = file_path
        with open(self.file_path, "r") as f:
            data = json.loads(f.read())
            self.validate(data)
            self.parse(data)

    def parse_from_url(self, url):
        response = None
        try:
            response = httpx.get(url)
        except Exception:
            pass
        if response is None:
            return
        self.validate(response.json())
        self.parse(response.json())
