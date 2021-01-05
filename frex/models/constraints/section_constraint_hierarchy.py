from __future__ import annotations
from typing import Tuple, Optional
from rdflib import URIRef
from dataclasses import dataclass
from dataclasses_json import dataclass_json


@dataclass_json
@dataclass
class SectionConstraintHierarchy:
    """
    The SectionConstraintHierarchy is used to capture a hierarchy of relations among sections. This primarily
    is used to capture logical AND / OR operators among relations.
    This currently only correctly supports hierarchies of sections as trees (?)
    """

    root_uri: URIRef
    dependency_and: Optional[Tuple[SectionConstraintHierarchy, ...]] = ()
    dependency_or: Optional[Tuple[SectionConstraintHierarchy, ...]] = ()
