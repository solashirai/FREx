from frex.stores.exceptions import NotFoundException
from rdflib import URIRef
from typing import Optional


class DomainObjectNotFoundException(NotFoundException):

    def __init__(self, *, uri: URIRef, message: Optional[str] = None):
        if not message:
            message = f"Object not found for URI: {uri}"
        NotFoundException.__init__(self, uri=uri, message=message)
