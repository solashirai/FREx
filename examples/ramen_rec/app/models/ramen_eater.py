from typing import NamedTuple
from frex.models import DomainObject
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class RamenEater(DomainObject):
    likesRamenFrom: str
    likesRamenStyle: str
