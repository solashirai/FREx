from frex.stores import SparqlQueryable, RequestResultCache
from abc import ABC


class _GraphQueryService(ABC):
    def __init__(self, *, queryable: SparqlQueryable):
        self.queryable = queryable
        self.cache_graph = None

    def get_cache_graph(self, *, sparql: str):
        self.cache_graph = RequestResultCache(
            result=self.queryable.query(sparql=sparql)
        ).get_graph()
