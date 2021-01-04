from typing import NamedTuple
from rdflib import URIRef
from frex.models.constraints import ConstraintType


class SectionAssignmentConstraint(NamedTuple):
    """
    A namedtuple to store Constraints over how items are assigned to sections.
    The constraints will be applied to all items in each section. e.g., if the constraint type if EQ,
    then for section_a and section_b, all item assignments must be equal.
    """
    constraint_type: ConstraintType
    section_a_uri: URIRef
    section_b_uri: URIRef
