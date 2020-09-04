from abc import abstractmethod
from typing import Tuple, Callable
from src.models.explanation import Explanation
from src.models.candidate import Candidate
from src.models.context import Context
from src.services.pipeline_service import PipelineService


class ScoringService(PipelineService):

    def __init__(self, *, scoring_function: Callable[[Candidate, Context], float],scoring_explanation: Explanation):
        self.scoring_function = scoring_function
        self.scoring_explanation = scoring_explanation

    def score(self, *, candidate: Candidate, context: Context) -> float:
        return self.scoring_function(candidate, context)

    def execute(self, *, context: Context, candidates: Tuple[Candidate, ...]) -> Tuple[Context, Tuple[Candidate, ...]]:
        for candidate in candidates:
            candidate.applied_explanations.append(self.scoring_explanation)
            candidate.applied_scores.append(self.score(context=context, candidate=candidate))

        return context, candidates
