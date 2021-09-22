from rdflib import URIRef
from typing import Optional


class MalformedContentException(Exception):
    def __init__(self, *, uri: URIRef, message: Optional[str] = None):
        self.__uri = uri
        if not message:
            message = f"Content malformed: {uri}. This error is caused by the entity that was queried in the KG " \
                      f"missing some property that is required in its corresponding Python dataclass."
        Exception.__init__(self, message)

    @property
    def uri(self) -> URIRef:
        return self.__uri
