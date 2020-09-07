from FREx.services import QueryService
from FREx.services.exceptions import *
from FREx.stores import LocalGraph, RemoteGraph, RequestResultCache
from rdflib import URIRef, Namespace, Graph
from rdflib.namespace import RDF, RDFS
from typing import List
from examples.ramen_rec.app.models import Ramen


class RamenQueryService(QueryService):

    ramen_ns = Namespace('http://www.erf.com/examples/ramenOnto/')

    def get_all_ramens_by_uri(self, *, ramen_uris: List[URIRef], cache_graph: Graph = None) -> List[Ramen]:
        if not cache_graph:
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
        return [self.get_ramen_by_uri(ramen_uri=ramen_uri, cache_graph=cache_graph) for ramen_uri in ramen_uris]

    def get_ramen_by_uri(self, *, ramen_uri: URIRef, cache_graph: Graph = None) -> Ramen:

        if not cache_graph:
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

        if (ramen_uri, RDF['type'], RamenQueryService.ramen_ns['ramen']) not in cache_graph:
            raise DomainObjectNotFoundException(uri=ramen_uri)

        label = cache_graph.value(ramen_uri, RDFS['label'])
        brand = cache_graph.value(ramen_uri, RamenQueryService.ramen_ns['brand'])
        country = cache_graph.value(ramen_uri, RamenQueryService.ramen_ns['country'])
        rating = cache_graph.value(ramen_uri, RamenQueryService.ramen_ns['rating'])
        style = cache_graph.value(ramen_uri, RamenQueryService.ramen_ns['style'])

        if any(ramen_property is None for ramen_property in [label, brand, country, rating, style]):
            raise MalformedDomainObjectException(uri=ramen_uri)

        return Ramen(uri=ramen_uri,
                     label=label.value,
                     brand=brand.value,
                     country=country.value,
                     rating=rating.value,
                     style=style.value)
