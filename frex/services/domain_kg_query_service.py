from rdflib import URIRef
from frex.services import _GraphQueryService
from frex.models import Explanation, DomainObject
from dataclasses import dataclass
from frex.services.exceptions import *
from typing import Generator, Type, TypeVar, Generic

T = TypeVar("T", bound=DomainObject)


class DomainKgQueryService(_GraphQueryService):
    """
    DomainKgQueryService is a basic implementation for a querying service over a knowledge graph. The functions
    implemented here do not consider any optimization or complicated queries, but rather it provides the most basic
    baseline to get triples directly connected to a given target URI and convert the results into the appropriate
    domain model.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def get_all_objects_by_class(
        self, *, target_class_uri: URIRef, object_type: Type[T]
    ) -> Generator[T, None, None]:
        """
        Query the KG for all entities of a specified class, then convert them to their corresponding python objects
        and return them.

        :param target_class_uri: The URI of the target class for which you want to retrieve all entities
        :param object_type: The type of the domain object that you want to return.
        :return: a generator that produces DomainObjects of the specified type for all entities of the specified class
        """
        self.get_cache_graph(
            sparql=f"""
            CONSTRUCT {{ ?s ?p ?o }}
            WHERE {{
                ?s a {target_class_uri.n3()} ;
                  ?p ?o.
            }}
            """
        )

        for ent_uri in self.cache_graph.subjects():
            yield self._get_object_by_uri(target_uri=ent_uri, object_type=object_type)

    def get_object_by_uri(self, *, target_uri: URIRef, object_type: Type[T]) -> T:
        """
        Query the KG for a target URI, and return a python object corresponding to the result of that query.

        The implementation for automatically going from a query result to python object relies on a dictionary
        of property URIs and their corresponding argument names in to populate in the DomainObject dataclass.
        This dictionary is produced by the ClassGenerator utility. If the class for your domain objects were
        made by hand, the corresponding methods for converting the results into an appropriate form should probably
        also be implemented manually as well.

        :param target_uri: The URI of the target object for which you want to retrieve information
        :param object_type: The type of the domain object that you want to return.
        :return: a DomainObject, of type specified by the input arguments, corresponding to the target URI.
        """
        self.get_cache_graph(
            sparql=f"""
            CONSTRUCT {{ {target_uri.n3()} ?p ?o }}
            WHERE {{
                {target_uri.n3()} ?p ?o.
            }}
            """
        )

        if (target_uri, None, None) not in self.cache_graph:
            raise NotFoundException(uri=target_uri)

        return self._get_object_by_uri(target_uri=target_uri, object_type=object_type)

    def _get_object_by_uri(self, *, target_uri: URIRef, object_type: Type[T]) -> T:
        """
        Produce a domain object for a target URI, given that the cache graph is already populated with query results.
        """
        if not hasattr(object_type, "prop_to_uri"):
            raise MalformedContentException(
                uri=target_uri,
                message="The object type you've specified does not "
                "contain a mapping dict for URIs to attribute "
                "names.",
            )
        properties_dict = {"uri": target_uri}
        try:
            for prop_uri_key, prop_name in object_type.prop_to_uri.items():
                # any property that isn't found in the query result is just set to None.
                # this isn't the most elegant solution, since some properties perhaps should be "required"
                # in the results, but this is a compromise to let the automatic code generation work more smoothly.
                vals = [
                    v.value if not isinstance(v, URIRef) else v
                    for v in self.cache_graph.objects(target_uri, prop_uri_key)
                ]
                if not vals:
                    vals = None
                elif len(vals) == 1:
                    vals = vals[0]
                else:
                    vals = frozenset(vals)
                properties_dict[prop_name] = vals

            target_object = object_type(**properties_dict)
        except ValueError:
            raise MalformedContentException(
                uri=target_uri,
                message="A value error occurred when trying to produce "
                "the dataclass. This can be caused by the query "
                "result missing some required attributes, or "
                "conversely the dataclass may be requiring some "
                "attributes that are not necessarily included in "
                "the KG data.",
            )

        return target_object
