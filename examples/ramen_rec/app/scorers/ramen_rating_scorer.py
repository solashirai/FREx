from frex.pipeline_stages.scorers import CandidateScorer
from examples.ramen_rec.app.models import RamenCandidate


class RamenRatingScorer(CandidateScorer):

    def score(self, *, candidate: RamenCandidate) -> float:
        return candidate.domain_object.rating / 5.0
