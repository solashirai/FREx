from typing import FrozenSet
from rdflib import URIRef
from frex.models import DomainObject
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class RamenEater(DomainObject):
    likes_ramen_from: str
    likes_ramen_brand: str
    likes_ramen_style: str
    prohibit_ramen_from: str
    favorite_ramen_uris: FrozenSet[URIRef]
