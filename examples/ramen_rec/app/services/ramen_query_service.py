from FREx.services import QueryService
from FREx.services.exceptions import *
from FREx.stores import LocalGraph, RemoteGraph, RequestResultCache
from rdflib import URIRef, Namespace, Graph
from rdflib.namespace import RDF, RDFS
from typing import List
from examples.ramen_rec.app.models.ramen import Ramen


class RamenQueryService(QueryService):

    ramen_ns = Namespace('http://www.erf.com/examples/ramenOnto/')

    def get_all_ramens_by_uri(self, *, ramen_uris: List[URIRef], graph_cache: Graph = None) -> List[Ramen]:
        if not graph_cache:
            if isinstance(self.queryable, LocalGraph) and False:
                graph_cache = self.queryable.get_graph()
            else:
                ramen_values = " ".join(ramen_uri.n3() for ramen_uri in ramen_uris)
                graph_cache = RequestResultCache(
                    result=self.queryable.query(sparql=f"""
                    CONSTRUCT {{ ?s ?p ?o }}
                    WHERE {{
                        VALUES ?s {{ {ramen_values} }}
                        ?s ?p ?o.
                    }}
                    """)).get_graph()
        return [self.get_ramen_by_uri(ramen_uri=ramen_uri, graph_cache=graph_cache) for ramen_uri in ramen_uris]

    def get_ramen_by_uri(self, *, ramen_uri: URIRef, graph_cache: Graph = None) -> Ramen:

        if not graph_cache:
            if isinstance(self.queryable, LocalGraph) and False:
                graph_cache = self.queryable.get_graph()
            else:
                graph_cache = RequestResultCache(
                    result=self.queryable.query(sparql=f"""
                    CONSTRUCT {{ ?s ?p ?o }}
                    WHERE {{
                        VALUES ?s {{ {ramen_uri.n3()} }}
                        ?s ?p ?o.
                    }}
                    """)).get_graph()

        if (ramen_uri, RDF['type'], RamenQueryService.ramen_ns['ramen']) not in graph_cache:
            raise DomainObjectNotFoundException(uri=ramen_uri)

        label = graph_cache.value(ramen_uri, RDFS['label'])
        brand = graph_cache.value(ramen_uri, RamenQueryService.ramen_ns['brand'])
        country = graph_cache.value(ramen_uri, RamenQueryService.ramen_ns['country'])
        rating = graph_cache.value(ramen_uri, RamenQueryService.ramen_ns['rating'])
        style = graph_cache.value(ramen_uri, RamenQueryService.ramen_ns['style'])

        if any(ramen_property is None for ramen_property in [label, brand, country, rating, style]):
            raise MalformedDomainObjectException(uri=ramen_uri)

        return Ramen(uri=ramen_uri,
                     label=label.value,
                     brand=brand.value,
                     country=country.value,
                     rating=rating.value,
                     style=style.value)
