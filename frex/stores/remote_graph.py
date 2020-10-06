from rdflib import Graph
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from rdflib.query import Result, ResultException
from frex.stores import SparqlQueryable


class RemoteGraph(SparqlQueryable):
    """
    RemoteGraph is used for accessing remote SPARQL endpoints.
    """

    def __init__(self, *, endpoint: str):
        self.graph = SPARQLStore(endpoint)

    def query(self, *, sparql: str) -> Result:
        """
        Query the remote graph using the API endpoint.

        :param sparql: A string containing valid SPARQL to query the graph.
        :return: A Result containing the result from calling the SPARQL query.
        """
        try:
            result = self.graph.query(sparql)
        except ResultException:
            # SPARQLStore raises an exception when no result is found
            result = Graph()
        return result
