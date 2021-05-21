from dataclasses import dataclass
from typing import List, Union

from .description import Description


@dataclass
class FormParameter:
    key: str
    value: str = ""
    src: Union[List, str, None] = None
    disabled: bool = False
    form_param_type: str = ""
    content_type: str = ""  # should override content-type in header
    description: Union[Description, None, str] = None