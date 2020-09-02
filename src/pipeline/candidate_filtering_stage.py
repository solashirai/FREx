from src.pipeline.pipeline_stage import PipelineStage
from src.models.filter_function import FilterFunction
from typing import Tuple
from src.models.candidate import Candidate
from src.models.context import Context
from src.models.explanation import Explanation


class CandidateFilteringStage(PipelineStage):

    def __init__(self, *, filter_function: FilterFunction, filter_explanation: Explanation, filter_score: float = 0):
        self.filter_function = filter_function
        self.filter_explanation = filter_explanation
        self.filter_score = filter_score

    def execute(self, *, context: Context, candidates: Tuple[Candidate, ...]) -> Tuple[Context, Tuple[Candidate, ...]]:
        output_candidates = []
        for candidate in candidates:
            if not self.filter_function.filter(context=context, candidate=candidate):
                candidate.applied_explanations.append(self.filter_explanation)
                candidate.applied_scores.append(self.filter_score)
                output_candidates.append(candidate)

        return context, tuple(output_candidates)
