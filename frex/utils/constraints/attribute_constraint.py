from typing import NamedTuple
from frex.utils.constraints import ConstraintType


class AttributeConstraint(NamedTuple):
    """
    A namedtuple to store Constraints that will be applied in a constraint solver.
    """

    attribute_name: str
    constraint_type: ConstraintType
    constraint_value: int
