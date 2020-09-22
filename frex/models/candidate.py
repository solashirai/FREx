from typing import Any, List
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import Explanation, DomainObject


@dataclass_json
@dataclass
class Candidate:
    context: Any
    domain_object: DomainObject
    applied_explanations: List[Explanation]
    applied_scores: List[float]

    @property
    def total_score(self) -> float:
        return sum(self.applied_scores)
