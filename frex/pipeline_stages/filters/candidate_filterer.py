from abc import abstractmethod
from typing import Generator, Optional
from frex.models import Explanation, Candidate
from frex.pipeline_stages import _PipelineStage


class CandidateFilterer(_PipelineStage):
    """
    CandidateFilterer should implement a filter function to determine which candidates to remove from consideration.
    filter(candidate) -> True will remove the candidate.
    """
    def __init__(self, *, filter_explanation: Explanation, filter_score: float = 0, **kwargs):
        self.filter_explanation = filter_explanation
        self.filter_score = filter_score

    @abstractmethod
    def filter(self, *, candidate: Candidate) -> bool:
        """
        The filter should return True when the candidate that is passed in should be removed from
        consideration as a candidate.

        :param candidate: A domain-specific candidate to filter
        :return: True if the candidate should be removed, False if it should be kept and passed on to later stages.
        """
        pass

    def __call__(
        self, *, candidates: Generator[Candidate, None, None]
    ) -> Generator[Candidate, None, None]:
        for candidate in candidates:
            if not self.filter(candidate=candidate):
                candidate.applied_explanations.append(self.filter_explanation)
                candidate.applied_scores.append(self.filter_score)
                yield candidate
