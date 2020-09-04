from abc import ABC, abstractmethod
from FREx.stores import SparqlQueryable
from rdflib import Graph


class ResultCache(SparqlQueryable, ABC):

    @abstractmethod
    def get_graph(self) -> Graph:
        pass
