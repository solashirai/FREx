from abc import ABC, abstractmethod
from rdflib.query import Result


class SparqlQueryable(ABC):

    @abstractmethod
    def query(self, *, sparql: str) -> Result:
        pass
