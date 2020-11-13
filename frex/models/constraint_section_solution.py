from typing import Tuple, Dict
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import Candidate


@dataclass_json
@dataclass
class ConstraintSectionSolution:
    """
    A 'section' of a constraint solution. Exactly what a section represents may differ based on the application,
    but an example of a section is a 'day' within a solution that is generated for a week-long meal plan.
    Sections have their own score, and store the candidates assigned to this section. Values of attributes of the
    domain objects are also stored, if they were relevant to solving constraints.
    """

    section_score: int
    section_attribute_values: Dict[str, int]
    section_candidates: Tuple[Candidate, ...]
