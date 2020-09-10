from abc import abstractmethod
from typing import Tuple, Generator
from frex.models import Explanation, Candidate, Context
from frex.pipeline_stages import _PipelineStage


class CandidateBoolScorer(_PipelineStage):
    def __init__(self, *, success_scoring_explanation: Explanation,
                 failure_scoring_explanation: Explanation):
        self.success_scoring_explanation = success_scoring_explanation
        self.failure_scoring_explanation = failure_scoring_explanation

    @abstractmethod
    def score(self, *, context: Context, candidate: Candidate) -> Tuple[bool, float]:
        pass

    def execute(
        self, *, context: Context, candidates: Generator[Candidate, None, None]
    ) -> Generator[Candidate, None, None]:
        for candidate in candidates:
            success, score = self.score(context=context, candidate=candidate)
            if success:
                candidate.applied_explanations.append(self.success_scoring_explanation)
            else:
                candidate.applied_explanations.append(self.failure_scoring_explanation)
            candidate.applied_scores.append(
                score
            )
            yield candidate
