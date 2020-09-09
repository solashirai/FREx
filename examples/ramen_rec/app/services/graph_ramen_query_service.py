from examples.ramen_rec.app.services.exceptions import *
from frex.stores import LocalGraph, RequestResultCache, SparqlQueryable
from rdflib import URIRef, Graph
from rdflib.namespace import RDF, RDFS
from typing import List, Generator
from examples.ramen_rec.app.models import Ramen
from examples.ramen_rec.app.services import RamenQueryService


class GraphRamenQueryService(RamenQueryService):

    def __init__(self, *, queryable: SparqlQueryable):
        self.queryable = queryable

    def get_cache_graph(self, *, sparql: str) -> Graph:
        return RequestResultCache(result=self.queryable.query(sparql=sparql)).get_graph()

    def get_ramens_by_uri(self, *, ramen_uris: List[URIRef]) -> Generator[Ramen, None, None]:
        if isinstance(self.queryable, LocalGraph):
            cache_graph = self.queryable.get_graph()
        else:
            ramen_values = " ".join(ramen_uri.n3() for ramen_uri in ramen_uris)
            cache_graph = self.get_cache_graph(sparql=f"""
                CONSTRUCT {{ ?s ?p ?o }}
                WHERE {{
                    VALUES ?s {{ {ramen_values} }}
                    ?s ?p ?o.
                }}
                """)

        for ramen_uri in ramen_uris:
            yield self.graph_get_ramen_by_uri(ramen_uri=ramen_uri, cache_graph=cache_graph)

    def get_ramen_by_uri(self, *, ramen_uri: URIRef) -> Ramen:
        if isinstance(self.queryable, LocalGraph) and False:
            cache_graph = self.queryable.get_graph()
        else:
            cache_graph = self.get_cache_graph(sparql=f"""
                CONSTRUCT {{ ?s ?p ?o }}
                WHERE {{
                    VALUES ?s {{ {ramen_uri.n3()} }}
                    ?s ?p ?o.
                }}
                """)
        return self.graph_get_ramen_by_uri(ramen_uri=ramen_uri, cache_graph=cache_graph)

    def graph_get_ramen_by_uri(self, *, ramen_uri: URIRef, cache_graph: Graph = None) -> Ramen:
        if (ramen_uri, RDF['type'], GraphRamenQueryService.ramen_ns['ramen']) not in cache_graph:
            raise DomainObjectNotFoundException(uri=ramen_uri)

        label = cache_graph.value(ramen_uri, RDFS['label'])
        brand = cache_graph.value(ramen_uri, GraphRamenQueryService.ramen_ns['brand'])
        country = cache_graph.value(ramen_uri, GraphRamenQueryService.ramen_ns['country'])
        rating = cache_graph.value(ramen_uri, GraphRamenQueryService.ramen_ns['rating'])
        style = cache_graph.value(ramen_uri, GraphRamenQueryService.ramen_ns['style'])

        if any(ramen_property is None for ramen_property in [label, brand, country, rating, style]):
            raise MalformedDomainObjectException(uri=ramen_uri)

        return Ramen(uri=ramen_uri,
                     label=label.value,
                     brand=brand.value,
                     country=country.value,
                     rating=rating.value,
                     style=style.value)
