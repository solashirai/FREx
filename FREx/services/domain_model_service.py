from FREx.stores import SparqlQueryable


class DomainModelService:

    def __init__(self, *, queryable: SparqlQueryable):
        self.queryable = queryable
