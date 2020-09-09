from abc import abstractmethod
from typing import Generator
from frex.models import Explanation, Candidate, Context
from frex.pipeline_stages import _PipelineStage


class CandidateFilterer(_PipelineStage):

    def __init__(self, *, filter_explanation: Explanation,
                 filter_score: float = 0):
        self.filter_explanation = filter_explanation
        self.filter_score = filter_score

    @abstractmethod
    def filter(self, *, context: Context, candidate: Candidate) -> bool:
        pass

    def execute(self, *, context: Context, candidates: Generator[Candidate, None, None]) ->\
            Generator[Candidate, None, None]:
        for candidate in candidates:
            if not self.filter(context=context, candidate=candidate):
                candidate.applied_explanations.append(self.filter_explanation)
                candidate.applied_scores.append(self.filter_score)
                yield candidate
