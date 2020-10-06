from typing import Any, List
from dataclasses import dataclass
from dataclasses_json import dataclass_json
from frex.models import Explanation, DomainObject


@dataclass_json
@dataclass
class Candidate:
    """
    Candidate classes should store some context for the current setting, a domain-specific object that is the
    candidate to return as part of the recommendation, and lists of applied explanations and scores.
    We expect applied explanations and scores to always have the same length, as pipeline stages should apply
    both when they are passed through.
    """
    context: Any
    domain_object: DomainObject
    applied_explanations: List[Explanation]
    applied_scores: List[float]

    @property
    def total_score(self) -> float:
        """
        Get the sum of scores in applied_scores for this candidate.
        :return: The sum of self.applied_scores
        """
        return sum(self.applied_scores)
