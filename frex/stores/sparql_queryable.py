from abc import ABC, abstractmethod
from rdflib.query import Result


class SparqlQueryable(ABC):
    """
    SparqlQueryable is the base class for stores that can be queried in some way using SPARQL queries.
    """

    @abstractmethod
    def query(self, *, sparql: str) -> Result:
        """
        Query the sparql queryable and retrieve a result.

        :param sparql: A string containing valid SPARQL to query.
        :return: A Result containing the result from calling the SPARQL query.
        """
        pass
