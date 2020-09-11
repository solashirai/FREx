from typing import NamedTuple, List
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import Explanation, DomainObject


@dataclass_json
@dataclass
class Candidate:
    domain_object: DomainObject
    applied_explanations: List[Explanation]
    applied_scores: List[float]

    @property
    def total_score(self) -> float:
        return sum(self.applied_scores)
