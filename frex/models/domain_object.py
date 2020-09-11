from dataclasses import dataclass
from dataclasses_json import dataclass_json
from rdflib import URIRef


@dataclass_json
@dataclass(frozen=True)
class DomainObject:
    uri: URIRef
