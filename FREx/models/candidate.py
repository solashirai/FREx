from typing import NamedTuple, List
from FREx.models import Explanation, DomainObject


class Candidate(NamedTuple):
    domain_object: DomainObject
    applied_explanations: List[Explanation]
    applied_scores: List[float]

    @property
    def total_score(self) -> float:
        return sum(self.applied_scores)
