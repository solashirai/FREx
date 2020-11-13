from typing import Tuple, Dict
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import ConstraintSectionSolution


@dataclass_json
@dataclass
class ConstraintSolution:
    """
    A constraint solution is the combination of multiple sections, each containing some number of items, that adhere
    to some number of constraints while maximizing the total score of all items contained in the solution.
    """

    overall_score: int
    overall_attribute_values: Dict[str, int]
    sections: Tuple[ConstraintSectionSolution, ...]
