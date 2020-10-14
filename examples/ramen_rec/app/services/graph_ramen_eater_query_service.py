from examples.ramen_rec.app.services.exceptions import *
from frex.stores import LocalGraph, RequestResultCache, SparqlQueryable
from rdflib import URIRef, Graph
from rdflib.namespace import RDF, RDFS
from typing import List, Generator
from examples.ramen_rec.app.utils import RamenUtils
from examples.ramen_rec.app.models import RamenEater
from examples.ramen_rec.app.services import RamenQueryService, _GraphQueryService


class GraphRamenEaterQueryService(_GraphQueryService, RamenQueryService):
    def get_ramen_eater_by_uri(self, *, ramen_eater_uri: URIRef) -> RamenEater:
        if isinstance(self.queryable, LocalGraph) and False:
            self.cache_graph = self.queryable.get_graph()
        else:
            self.get_cache_graph(
                sparql=f"""
                CONSTRUCT {{ ?s ?p ?o }}
                WHERE {{
                    VALUES ?s {{ {ramen_eater_uri.n3()} }}
                    ?s ?p ?o.
                }}
                """
            )
        return self.graph_get_ramen_eater_by_uri(ramen_eater_uri=ramen_eater_uri)

    def graph_get_ramen_eater_by_uri(self, *, ramen_eater_uri: URIRef) -> RamenEater:
        if (
            ramen_eater_uri,
            RDF["type"],
            RamenUtils.ramen_onto_ns["ramenEater"],
        ) not in self.cache_graph:
            raise DomainObjectNotFoundException(uri=ramen_eater_uri)

        likes_ramen_from = self.cache_graph.value(
            ramen_eater_uri, RamenUtils.ramen_onto_ns["likesRamenFrom"]
        )
        likes_ramen_brand = self.cache_graph.value(
            ramen_eater_uri, RamenUtils.ramen_onto_ns["likesRamenBrand"]
        )
        likes_ramen_style = self.cache_graph.value(
            ramen_eater_uri, RamenUtils.ramen_onto_ns["likesRamenStyle"]
        )
        prohibit_ramen_from = self.cache_graph.value(
            ramen_eater_uri, RamenUtils.ramen_onto_ns["prohibitRamenFrom"]
        )
        favorite_ramen_uris = self.cache_graph.objects(
            ramen_eater_uri, RamenUtils.ramen_onto_ns["favoriteRamen"]
        )

        if any(
            ramen_eater_property is None
            for ramen_eater_property in [
                likes_ramen_from,
                likes_ramen_style,
                likes_ramen_brand,
                prohibit_ramen_from,
            ]
        ):
            raise MalformedDomainObjectException(uri=ramen_eater_uri)

        return RamenEater(
            uri=ramen_eater_uri,
            likes_ramen_from=likes_ramen_from.value,
            likes_ramen_brand=likes_ramen_brand.value,
            likes_ramen_style=likes_ramen_style.value,
            prohibit_ramen_from=prohibit_ramen_from.value,
            favorite_ramen_uris=frozenset(favorite_ramen_uris),
        )
