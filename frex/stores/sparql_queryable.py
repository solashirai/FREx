from abc import ABC, abstractmethod
from rdflib.query import Result


class SparqlQueryable(ABC):
    """
    SparqlQueryable is the base class for stores that can be queried in some way using SPARQL queries.
    """
    @abstractmethod
    def query(self, *, sparql: str) -> Result:
        pass
