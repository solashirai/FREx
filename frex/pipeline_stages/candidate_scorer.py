from typing import Tuple, Generator
from frex.models import Explanation, Candidate, Context, Scorer
from frex.pipeline_stages import _Pipeline


class CandidateScorer(_Pipeline):

    def __init__(self, *, scoring_function: Scorer, scoring_explanation: Explanation):
        self.scoring_function = scoring_function
        self.scoring_explanation = scoring_explanation

    def score(self, *, context: Context, candidate: Candidate) -> float:
        return self.scoring_function.score_input(context=context, candidate=candidate)

    def execute(self, *, context: Context, candidates: Generator[Candidate, None, None]) -> \
            Generator[Candidate, None, None]:
        for candidate in candidates:
            candidate.applied_explanations.append(self.scoring_explanation)
            candidate.applied_scores.append(self.score(context=context, candidate=candidate))
            yield candidate
