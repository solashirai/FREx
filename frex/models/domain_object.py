from dataclasses import dataclass
from dataclasses_json import dataclass_json
from rdflib import URIRef


@dataclass_json
@dataclass(frozen=True)
class DomainObject:
    """
    DomainObject is the base class for objects related to a recommendation application that have some URI.
    """

    uri: URIRef
