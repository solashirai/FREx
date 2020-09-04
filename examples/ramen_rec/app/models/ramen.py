from typing import NamedTuple
from rdflib import URIRef
from FREx.models import DomainObject


class Ramen(NamedTuple, DomainObject):
    uri: URIRef
    label: str
    brand: str
    country: str
    style: str
    rating: float
