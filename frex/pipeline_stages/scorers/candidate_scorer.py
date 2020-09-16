from abc import abstractmethod
from typing import Tuple, Generator
from frex.models import Explanation, Candidate, Context
from frex.pipeline_stages import _PipelineStage


class CandidateScorer(_PipelineStage):
    def __init__(self, *, scoring_explanation: Explanation):
        self.scoring_explanation = scoring_explanation

    @abstractmethod
    def score(self, *, context: Context, candidate: Candidate) -> float:
        pass

    def __call__(
        self, *, context: Context, candidates: Generator[Candidate, None, None]
    ) -> Generator[Candidate, None, None]:
        for candidate in candidates:
            candidate.applied_explanations.append(self.scoring_explanation)
            candidate.applied_scores.append(
                self.score(context=context, candidate=candidate)
            )
            yield candidate
