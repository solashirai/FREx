from rdflib import Graph
from FREx.stores import SparqlQueryable, RequestResultCache


class QueryService:

    def __init__(self, *, queryable: SparqlQueryable):
        self.queryable = queryable

    def get_cache_graph(self, *, sparql: str) -> Graph:
        return RequestResultCache(result=self.queryable.query(sparql=sparql)).get_graph()
