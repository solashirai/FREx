from src.stores.graph.sparql_queryable import SparqlQueryable


class DomainModelService:

    def __init__(self, *, queryable: SparqlQueryable):
        self.queryable = queryable
