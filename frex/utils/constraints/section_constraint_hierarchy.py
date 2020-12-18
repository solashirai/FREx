from __future__ import annotations
from typing import NamedTuple, Optional
from rdflib import URIRef
from frex.utils.constraints import ConstraintType


class SectionConstraintHierarchy(NamedTuple):
    """
    The SectionConstraintHierarchy is used to capture a hierarchy of relations among sections. This primarily
    is used to capture logical AND / OR operators among relations.
    This currently only correctly supports hierarchies of sections as trees (?)
    """
    root_uri: URIRef
    dependency_and: Optional[SectionConstraintHierarchy] = None
    dependency_or: Optional[SectionConstraintHierarchy] = None
