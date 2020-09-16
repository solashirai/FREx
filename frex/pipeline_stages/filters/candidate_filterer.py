from abc import abstractmethod
from typing import Generator, Optional
from frex.models import Explanation, Candidate
from frex.pipeline_stages import _PipelineStage


class CandidateFilterer(_PipelineStage):
    def __init__(self, *, filter_explanation: Explanation, filter_score: float = 0, **kwargs):
        self.filter_explanation = filter_explanation
        self.filter_score = filter_score
        _PipelineStage.__init__(self,
                                **kwargs)

    @abstractmethod
    def filter(self, *, candidate: Candidate) -> bool:
        pass

    def __call__(
        self, *, candidates: Generator[Candidate, None, None], **kwargs
    ) -> Generator[Candidate, None, None]:
        for candidate in candidates:
            if not self.filter(candidate=candidate):
                candidate.applied_explanations.append(self.filter_explanation)
                candidate.applied_scores.append(self.filter_score)
                yield candidate
