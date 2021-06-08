from dataclasses import dataclass
from dataclasses import field
import json
from typing import List
from typing import Union

import httpx

from postmanparser.auth import Auth
from postmanparser.exceptions import FolderNotFoundError, MissingRequiredFieldException
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

    @staticmethod
    def _get_requests_from_items(items: List[Union[Item, ItemGroup]]):
        requests = []
        for itm in items:
            if isinstance(itm, Item):
                requests.append(itm.request)
                continue
        return requests

    @staticmethod
    def _get_requests_map_from_items(items: List[Union[Item, ItemGroup]], folder: str):
        requests = {}
        if folder == "":
            folder = "/"
        requests[folder] = []
        for itm in items:
            if isinstance(itm, Item):
                requests[folder].append(itm.request)
                continue

            _folder = itm.name if folder == "/" else f"{folder}/{itm.name}"

            requests.update(Collection._get_requests_map_from_items(itm.item, _folder))
        return requests

    @staticmethod
    def get_item_groups(items: List[Union[Item, ItemGroup]]) -> List[ItemGroup]:
        result = []
        for item in items:
            if isinstance(item, ItemGroup):
                result.append(item)
        return result

    def get_requests(self, folder: str = "", recursive: bool = False):
        if not folder:
            if recursive:
                return self._get_requests_map_from_items(self.item, folder)

            return self._get_requests_from_items(self.item)

        nested_folders = folder.split("/")
        items = self.item
        for _folder in nested_folders:
            next_item_group = None
            item_groups = self.get_item_groups(items)
            for itm_group in item_groups:
                if _folder == itm_group.name:
                    next_item_group = itm_group
                    break
            if next_item_group is None:
                raise FolderNotFoundError(
                    f"Folder with name {_folder} does not exists."
                )
            items = next_item_group.item
        if not recursive:
            return self._get_requests_from_items(items)

        return self._get_requests_map_from_items(items, folder)
