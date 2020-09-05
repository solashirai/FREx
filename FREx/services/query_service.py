from abc import ABC
from FREx.stores import SparqlQueryable


class QueryService:

    def __init__(self, *, queryable: SparqlQueryable):
        self.queryable = queryable
