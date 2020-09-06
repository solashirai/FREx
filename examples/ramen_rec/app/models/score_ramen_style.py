from FREx.models import ScoringFunction
from examples.ramen_rec.app.models.ramen_context import RamenContext
from examples.ramen_rec.app.models.ramen_candidate import RamenCandidate


class ScoreRamenStyle(ScoringFunction):

    def score_input(self, *, context: RamenContext, candidate: RamenCandidate) -> float:
        if context.target_ramen.style == candidate.domain_object.style:
            return 1
        else:
            return 0
