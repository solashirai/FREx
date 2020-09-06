from typing import Tuple
from FREx.models import Explanation, Candidate, Context, ScoringFunction
from FREx.services import PipelineService


class ScoringService(PipelineService):

    def __init__(self, *, scoring_function: ScoringFunction,scoring_explanation: Explanation):
        self.scoring_function = scoring_function
        self.scoring_explanation = scoring_explanation

    def score(self, *, context: Context, candidate: Candidate) -> float:
        return self.scoring_function.score_input(context=context, candidate=candidate)

    def execute(self, *, context: Context, candidates: Tuple[Candidate, ...]) -> \
            Tuple[Context, Tuple[Candidate, ...]]:
        for candidate in candidates:
            candidate.applied_explanations.append(self.scoring_explanation)
            candidate.applied_scores.append(self.score(context=context, candidate=candidate))

        # sort candidates with new scores before outputting
        output_candidates = sorted(candidates, key=lambda c: c.total_score, reverse=True)
        return context, tuple(output_candidates)
