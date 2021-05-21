import json
from typing import List, Union
from dataclasses import dataclass, field

from .info import Info
from .item import Item, ItemGroup, parse_item_list


@dataclass
class Collection:
    file_path: str = ""
    info: Info = field(init=False)
    item: List[Union[Item, ItemGroup]] = field(init=False)

    def validate(self, data):
        if "info" not in data or "item" not in data:
            raise Exception(
                "Invalid Postman collection: Required 'info' and 'item' properties in 'collection' object"
            )

    def parse(self, data):
        items = data.get("item")
        self.item = parse_item_list(items)
        self.info = Info.parse(data["info"])

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
