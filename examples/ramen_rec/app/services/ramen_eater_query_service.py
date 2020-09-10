from abc import ABC, abstractmethod
from typing import Generator, List
from rdflib import Namespace, Graph, URIRef
from examples.ramen_rec.app.models import RamenEater


class RamenEaterQueryService(ABC):

    def get_ramen_eater_by_uri(self, *, ramen_eater_uri: URIRef) -> RamenEater:
        pass
