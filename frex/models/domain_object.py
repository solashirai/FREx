from dataclasses import dataclass
from dataclasses_json import dataclass_json
from rdflib import URIRef


@dataclass_json
@dataclass(frozen=True)
class DomainObject:
    """
    DomainObject classes should be able to point to some uri that identifies them.
    """
    uri: URIRef
