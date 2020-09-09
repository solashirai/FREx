from abc import ABC, abstractmethod
from typing import Generator, List
from rdflib import Namespace, Graph, URIRef
from examples.ramen_rec.app.models import Ramen


class RamenQueryService(ABC):
    ramen_ns = Namespace('http://www.frex.com/examples/ramenOnto/')

    def get_ramens_by_uri(self, *, ramen_uris: List[URIRef]) -> Generator[Ramen, None, None]:
        pass

    def get_ramen_by_uri(self, *, ramen_uri: URIRef) -> Ramen:
        pass
