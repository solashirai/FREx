from typing import Tuple
from FREx.models import Explanation, Candidate, Context, FilteringFunction
from FREx.services import PipelineService


class FilterService(PipelineService):

    def __init__(self, *, filter_function: FilteringFunction,
                 filter_explanation: Explanation,
                 filter_score: float = 0):
        self.filter_function = filter_function
        self.filter_explanation = filter_explanation
        self.filter_score = filter_score

    def filter(self, *, context: Context, candidate: Candidate) -> bool:
        return self.filter_function.filter_input(context=context, candidate=candidate)

    def execute(self, *, context: Context, candidates: Tuple[Candidate, ...]) -> Tuple[Context, Tuple[Candidate, ...]]:
        output_candidates = []
        for candidate in candidates:
            if not self.filter(context=context, candidate=candidate):
                candidate.applied_explanations.append(self.filter_explanation)
                candidate.applied_scores.append(self.filter_score)
                output_candidates.append(candidate)

        return context, tuple(output_candidates)

