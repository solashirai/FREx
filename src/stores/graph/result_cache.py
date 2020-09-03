from abc import ABC, abstractmethod
from src.stores.graph.sparql_queryable import SparqlQueryable
from rdflib import Graph


class ResultCache(ABC, SparqlQueryable):

    @abstractmethod
    def get_graph(self) -> Graph:
        pass
