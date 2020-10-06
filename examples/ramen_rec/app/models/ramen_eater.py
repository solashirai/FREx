from typing import FrozenSet
from rdflib import URIRef
from frex.models import DomainObject
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass(frozen=True)
class RamenEater(DomainObject):
    """
    RamenEater profiles have a set of favorite ramens, a favorite country (likes_ramen_from), a favorite brand,
    a favorite style, and a country to prohibit (prohibit_ramen_from).
    """
    likes_ramen_from: str
    likes_ramen_brand: str
    likes_ramen_style: str
    prohibit_ramen_from: str
    favorite_ramen_uris: FrozenSet[URIRef]
