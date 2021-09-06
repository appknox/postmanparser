from dataclasses import dataclass
from dataclasses import field
import json
from typing import List
from typing import Union

import httpx

from postmanparser.auth import Auth
from postmanparser.event import Event
from postmanparser.exceptions import FolderNotFoundError
from postmanparser.exceptions import MissingRequiredFieldException
from postmanparser.info import Info
from postmanparser.item import Item
from postmanparser.item import ItemGroup
from postmanparser.item import parse_item_list
from postmanparser.request import Request
from postmanparser.variable import Variable


@dataclass
class Collection:
    file_path: str = ""
    variable: List[Variable] = None
    auth: Auth = None
    info: Info = field(init=False)
    item: List[Union[Item, ItemGroup]] = field(init=False)
    event: List[Event] = None

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
        self.auth = Auth.parse(data["auth"]) if "auth" in data else None
        var = data.get("variable", [])
        if var:
            self.variable = [Variable.parse(_) for _ in var]
        event = data.get("event", [])
        if event:
            self.event = [Event.parse(_) for _ in event]

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
    def _get_requests_from_items(
        items: List[Union[Item, ItemGroup]], recursive: bool = True
    ) -> List[Union[Request, str]]:
        requests = []
        for itm in items:
            if isinstance(itm, Item):
                requests.append(itm.request)
                continue
            if recursive:
                requests.extend(Collection._get_requests_from_items(itm.item))
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

    def get_items_of_folder(self, folder: str) -> List[Union[Item, ItemGroup]]:
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
        return items

    def get_requests(
        self, folder: str = "", recursive: bool = True
    ) -> List[Union[Request, str]]:
        if not folder:
            return self._get_requests_from_items(self.item, recursive=recursive)

        items = self.get_items_of_folder(folder)
        return self._get_requests_from_items(items, recursive=recursive)

    def get_requests_map(self, folder: str = ""):
        if folder:
            items = self.get_items_of_folder(folder)
            return self._get_requests_map_from_items(items, folder)
        return self._get_requests_map_from_items(self.item, folder)
