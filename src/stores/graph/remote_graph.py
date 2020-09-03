from rdflib import Graph
from rdflib.plugins.stores.sparqlstore import SPARQLStore
from rdflib.query import Result, ResultException
from src.stores.graph.sparql_queryable import SparqlQueryable


class RemoteGraph(SparqlQueryable):

    def __init__(self, *, endpoint: str):
        self.graph = SPARQLStore(endpoint)

    def query(self, *, sparql: str) -> Result:
        try:
            result = self.graph.query(sparql)
        except ResultException:
            # SPARQLStore raises an exception when no result is found
            result = Graph()
        return result
