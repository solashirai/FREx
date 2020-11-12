from typing import Tuple, Dict
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import Candidate


@dataclass_json
@dataclass
class ConstraintSectionSolution:
    section_score: int
    section_attribute_values: Dict[str, int]
    section_candidates: Tuple[Candidate, ...]
