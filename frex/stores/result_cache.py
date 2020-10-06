from abc import ABC, abstractmethod
from frex.stores import SparqlQueryable
from rdflib import Graph


class ResultCache(SparqlQueryable, ABC):
    @abstractmethod
    def get_graph(self) -> Graph:
        """
        Get the local Graph object.

        :return: The local Graph object
        """
        pass
