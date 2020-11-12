from typing import Tuple, Dict
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import ConstraintSectionSolution


@dataclass_json
@dataclass
class ConstraintSolution:
    overall_score: int
    overall_attribute_values: Dict[str, int]
    sections: Tuple[ConstraintSectionSolution, ...]
