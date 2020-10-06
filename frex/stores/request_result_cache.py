from frex.stores import ResultCache
from rdflib import Graph
from rdflib.query import Result


class RequestResultCache(ResultCache):
    """
    RequestResultCache stores a local graph whose contents are the result of a query to some sparql queryable.
    After a single call to the graph containing relevant data, the contents of RequestResultCache should be used
    by the system for the remaining data formatting and retrieval functions.
    """
    def __init__(self, *, result: Result):
        # Per HTTP request ResultsCache
        self.cache_graph = Graph().parse(data=result.serialize(format="xml"))

    def get_graph(self) -> Graph:
        return self.cache_graph

    def query(self, *, sparql: str) -> Result:
        return self.cache_graph.query(sparql)
