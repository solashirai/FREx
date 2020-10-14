from examples.ramen_rec.app.services.exceptions import *
from frex.stores import LocalGraph, RequestResultCache, SparqlQueryable
from rdflib import URIRef, Graph
from rdflib.namespace import RDF, RDFS
from typing import List, Generator
from examples.ramen_rec.app.models import Ramen
from examples.ramen_rec.app.utils import RamenUtils
from examples.ramen_rec.app.services import RamenQueryService, _GraphQueryService


class GraphRamenQueryService(_GraphQueryService, RamenQueryService):
    def get_ramens_by_uri(
        self, *, ramen_uris: List[URIRef]
    ) -> Generator[Ramen, None, None]:
        if isinstance(self.queryable, LocalGraph):
            self.cache_graph = self.queryable.get_graph()
        else:
            ramen_values = " ".join(ramen_uri.n3() for ramen_uri in ramen_uris)
            self.get_cache_graph(
                sparql=f"""
                CONSTRUCT {{ ?s ?p ?o }}
                WHERE {{
                    VALUES ?s {{ {ramen_values} }}
                    ?s ?p ?o.
                }}
                """
            )

        for ramen_uri in ramen_uris:
            yield self.graph_get_ramen_by_uri(ramen_uri=ramen_uri)

    def get_ramen_by_uri(self, *, ramen_uri: URIRef) -> Ramen:
        if isinstance(self.queryable, LocalGraph) and False:
            self.cache_graph = self.queryable.get_graph()
        else:
            self.get_cache_graph(
                sparql=f"""
                CONSTRUCT {{ ?s ?p ?o }}
                WHERE {{
                    VALUES ?s {{ {ramen_uri.n3()} }}
                    ?s ?p ?o.
                }}
                """
            )
        return self.graph_get_ramen_by_uri(ramen_uri=ramen_uri)

    def graph_get_ramen_by_uri(self, *, ramen_uri: URIRef) -> Ramen:
        if (
            ramen_uri,
            RDF["type"],
            RamenUtils.ramen_onto_ns["ramen"],
        ) not in self.cache_graph:
            raise DomainObjectNotFoundException(uri=ramen_uri)

        label = self.cache_graph.value(ramen_uri, RDFS["label"])
        brand = self.cache_graph.value(ramen_uri, RamenUtils.ramen_onto_ns["brand"])
        country = self.cache_graph.value(ramen_uri, RamenUtils.ramen_onto_ns["country"])
        rating = self.cache_graph.value(ramen_uri, RamenUtils.ramen_onto_ns["rating"])
        style = self.cache_graph.value(ramen_uri, RamenUtils.ramen_onto_ns["style"])

        if any(
            ramen_property is None
            for ramen_property in [label, brand, country, rating, style]
        ):
            raise MalformedDomainObjectException(uri=ramen_uri)

        return Ramen(
            uri=ramen_uri,
            label=label.value,
            brand=brand.value,
            country=country.value,
            rating=rating.value,
            style=style.value,
        )
