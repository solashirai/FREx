from frex.pipeline_stages.scorers import CandidateScorer
from frex.models import Context
from examples.ramen_rec.app.models import RamenContext
from examples.ramen_rec.app.models import RamenCandidate


class RamenRatingScorer(CandidateScorer):
    def score(self, *, context: Context, candidate: RamenCandidate) -> float:
        return candidate.domain_object.rating / 5.0
