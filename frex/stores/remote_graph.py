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
        try:
            result = self.graph.query(sparql)
        except ResultException:
            # SPARQLStore raises an exception when no result is found
            result = Graph()
        return result
