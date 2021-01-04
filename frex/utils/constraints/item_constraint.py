from typing import NamedTuple
from rdflib import URIRef
from frex.utils.constraints import ConstraintType


class ItemConstraint(NamedTuple):
    """
    A namedtuple to store Constraints over how items are assigned/selected.
    """
    constraint_type: ConstraintType
    item_a_uri: URIRef
    item_b_uri: URIRef
