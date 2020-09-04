from FREx.stores import ResultCache
from rdflib import Graph
from rdflib.query import Result


class RequestResultCache(ResultCache):

    def __init__(self, *, result: Result):
        # Per HTTP request ResultsCache
        self.cache_graph = Graph().parse(data=result.serialize(format='xml'))

    def get_graph(self) -> Graph:
        return self.cache_graph

    def query(self, *, sparql: str) -> Result:
        return self.graph.query(sparql)
