from rdflib import URIRef
from typing import Optional


class NotFoundException(Exception):
    def __init__(self, *, uri: URIRef, message: Optional[str] = None):
        self.__uri = uri
        if not message:
            message = f"URI not found: {uri}"
        Exception.__init__(self, message)

    @property
    def uri(self) -> URIRef:
        return self.__uri
