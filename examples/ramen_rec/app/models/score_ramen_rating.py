from FREx.models import ScoringFunction
from examples.ramen_rec.app.models.ramen_context import RamenContext
from examples.ramen_rec.app.models.ramen_candidate import RamenCandidate


class ScoreRamenRating(ScoringFunction):

    def score_input(self, *, context: RamenContext, candidate: RamenCandidate) -> float:
        return candidate.domain_object.rating / 5.0
