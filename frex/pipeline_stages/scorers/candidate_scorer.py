from abc import abstractmethod
from typing import Tuple, Generator, Optional
from frex.models import Explanation, Candidate
from frex.pipeline_stages import _PipelineStage


class CandidateScorer(_PipelineStage):
    def __init__(self, *,
                 scoring_explanation: Explanation,
                 **kwargs):
        self.scoring_explanation = scoring_explanation

    @abstractmethod
    def score(self, *, candidate: Candidate) -> float:
        pass

    def __call__(
        self, *, candidates: Generator[Candidate, None, None]
    ) -> Generator[Candidate, None, None]:
        for candidate in candidates:
            candidate.applied_explanations.append(self.scoring_explanation)
            candidate.applied_scores.append(
                self.score(candidate=candidate)
            )
            yield candidate
