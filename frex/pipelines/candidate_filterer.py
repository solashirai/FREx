from typing import Generator
from frex.models import Explanation, Candidate, Context, Filter
from frex.pipelines import _Pipeline


class CandidateFilterer(_Pipeline):

    def __init__(self, *, filter_function: Filter,
                 filter_explanation: Explanation,
                 filter_score: float = 0):
        self.filter_function = filter_function
        self.filter_explanation = filter_explanation
        self.filter_score = filter_score

    def filter(self, *, context: Context, candidate: Candidate) -> bool:
        return self.filter_function.filter_input(context=context, candidate=candidate)

    def execute(self, *, context: Context, candidates: Generator[Candidate, None, None]) ->\
            Generator[Candidate, None, None]:
        for candidate in candidates:
            if not self.filter(context=context, candidate=candidate):
                candidate.applied_explanations.append(self.filter_explanation)
                candidate.applied_scores.append(self.filter_score)
                yield candidate
        return
