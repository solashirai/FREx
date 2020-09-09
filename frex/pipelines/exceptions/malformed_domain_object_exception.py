from frex.pipelines.exceptions import MalformedContentException
from rdflib import URIRef
from typing import Optional


class MalformedDomainObjectException(MalformedContentException):

    def __init__(self, *, uri: URIRef, message: Optional[str] = None):
        if not message:
            message = f"Object content malformed for URI: {uri}"
        MalformedContentException.__init__(self, uri=uri, message=message)
