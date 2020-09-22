from abc import abstractmethod
from typing import Tuple, Generator, Optional, Type
from frex.models import Explanation, Candidate
from frex.pipeline_stages import _PipelineStage


class CandidateBoolScorer(_PipelineStage):
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
