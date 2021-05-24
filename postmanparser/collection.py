import json
from postmanparser.auth import Auth
from postmanparser.variable import Variable
from typing import List, Union
from dataclasses import dataclass, field

from .info import Info
from .item import Item, ItemGroup, parse_item_list


@dataclass
class Collection:
    file_path: str = ""
    variable: List[Variable] = None
    auth: Auth = None
    info: Info = field(init=False)
    item: List[Union[Item, ItemGroup]] = field(init=False)

    def validate(self, data):
        if "info" not in data or "item" not in data:
            raise Exception(
                "Invalid Postman collection: Required 'info' and 'item' properties in 'collection' object"
            )

    def parse(self, data: dict):
        self.item = parse_item_list(data.get("item"))
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
        data = {}
        # request to url
        self.validate(data)
        self.parse(data)
