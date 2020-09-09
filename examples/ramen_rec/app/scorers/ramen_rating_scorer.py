from frex.pipeline_stages.scorers import CandidateScorer
from examples.ramen_rec.app.models.ramen_context import RamenContext
from examples.ramen_rec.app.models.ramen_candidate import RamenCandidate


class RamenRatingScorer(CandidateScorer):
    def score(self, *, context: RamenContext, candidate: RamenCandidate) -> float:
        return candidate.domain_object.rating / 5.0
