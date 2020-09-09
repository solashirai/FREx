from dataclasses import dataclass
from rdflib import URIRef


@dataclass
class DomainObject:
    uri: URIRef
