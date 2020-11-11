from typing import NamedTuple
from frex.utils import ConstraintType


class Constraint(NamedTuple):
    """
    A namedtuple to store Constraints that will be applied in a constraint solver.
    """
    attribute_name: str
    constraint_type: ConstraintType
    constraint_val: int
