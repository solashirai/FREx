from abc import abstractmethod
from typing import Tuple, Generator, Optional, Type
from frex.models import Explanation, Candidate
from frex.pipeline_stages import _PipelineStage


class CandidateBoolScorer(_PipelineStage):
    """
    CandidateBoolScorer is a scoring pipeline stage that scores based on whether or not the candidate matches some
    given condition. The score function for this class returns a bool indicating whether the condition was matched,
    and an appropriate explanation is attached to the candidate.
    """
    def __init__(
        self,
        *,
        success_scoring_explanation: Explanation,
        failure_scoring_explanation: Explanation,
        **kwargs
    ):
        self.success_scoring_explanation = success_scoring_explanation
        self.failure_scoring_explanation = failure_scoring_explanation

    @abstractmethod
    def score(self, *, candidate: Candidate) -> Tuple[bool, float]:
        """
        score should return True if the candidate matches some success condition. Regardless of whether the candidate
        passes the success, the score function should also return a score to applied.
        """
        pass

    def __call__(
        self, *, candidates: Generator[Candidate, None, None]
    ) -> Generator[Candidate, None, None]:
        for candidate in candidates:
            success, score = self.score(candidate=candidate)
            if success:
                candidate.applied_explanations.append(self.success_scoring_explanation)
            else:
                candidate.applied_explanations.append(self.failure_scoring_explanation)
            candidate.applied_scores.append(score)
            yield candidate
