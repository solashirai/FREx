from typing import NamedTuple, List
from src.models.explanation import Explanation


class Candidate(NamedTuple):
    domain_object: NamedTuple
    applied_explanations: List[Explanation]
    applied_scores: List[float]

    @property
    def total_score(self) -> float:
        return sum(self.applied_scores)
