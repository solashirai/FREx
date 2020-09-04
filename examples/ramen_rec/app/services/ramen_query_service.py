from FREx.services import QueryService
from FREx.services.exceptions import *
from rdflib import URIRef, Namespace, Graph
from rdflib.namespace import RDF, RDFS
from examples.ramen_rec.app.models.ramen import Ramen


class RamenQueryService(QueryService):

    ramen_ns = Namespace('http://www.erf.com/examples/ramenOnto/')

    def __init__(self, *, ramen_graph: Graph):
        self.ramen_graph = ramen_graph

    def get_ramen_by_uri(self, *, ramen_uri: URIRef) -> Ramen:

        if (ramen_uri, RDF['type'], RamenQueryService.ramen_ns['ramen']) not in self.ramen_graph:
            raise DomainObjectNotFoundException(uri=ramen_uri)

        label = self.ramen_graph.value(ramen_uri, RDFS['label'])
        brand = self.ramen_graph.value(ramen_uri, RamenQueryService.ramen_ns['brand'])
        country = self.ramen_graph.value(ramen_uri, RamenQueryService.ramen_ns['country'])
        rating = self.ramen_graph.value(ramen_uri, RamenQueryService.ramen_ns['rating'])
        style = self.ramen_graph.value(ramen_uri, RamenQueryService.ramen_ns['style'])

        if any(ramen_property is None for ramen_property in [label, brand, country, rating, style]):
            raise MalformedDomainObjectException(uri=ramen_uri)

        return Ramen(uri=ramen_uri,
                     label=label.value,
                     brand=brand.value,
                     country=country.value,
                     rating=rating.value,
                     style=style.value)
