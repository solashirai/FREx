from typing import Tuple, Dict
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models.constraints import ConstraintSolutionSection


@dataclass_json
@dataclass
class ConstraintSolutionSectionSet:
    """
    A grouping of constraint solution sections that was solved by the constraint solution.
    """

    sections: Tuple[ConstraintSolutionSection, ...]
