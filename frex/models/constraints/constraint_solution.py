from typing import Tuple, Dict
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import Candidate, DomainObject
from frex.models.constraints import ConstraintSolutionSectionSet


@dataclass_json
@dataclass(frozen=True)
class ConstraintSolution(DomainObject):
    """
    A constraint solution is the combination of multiple sections, each containing some number of items, that adhere
    to some number of constraints while maximizing the total score of all items contained in the solution.
    """

    overall_score: int
    overall_attribute_values: Dict[str, int]
    solution_section_sets: Tuple[ConstraintSolutionSectionSet, ...]
    items: Tuple[Candidate, ...]
