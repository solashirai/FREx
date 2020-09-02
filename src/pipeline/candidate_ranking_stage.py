from src.pipeline.pipeline_stage import PipelineStage
from src.models.scoring_function import ScoringFunction
from typing import Tuple
from src.models.candidate import Candidate
from src.models.context import Context
from src.models.explanation import Explanation


class CandidateRankingStage(PipelineStage):

    def __init__(self, *, scoring_function: ScoringFunction, scoring_explanation: Explanation):
        self.scoring_function = scoring_function
        self.scoring_explanation = scoring_explanation

    def execute(self, *, context: Context, candidates: Tuple[Candidate, ...]) -> Tuple[Context, Tuple[Candidate, ...]]:
        for candidate in candidates:
            candidate.applied_explanations.append(self.scoring_explanation)
            candidate.applied_scores.append(self.scoring_function.score(context=context, candidate=candidate))

        return context, candidates
