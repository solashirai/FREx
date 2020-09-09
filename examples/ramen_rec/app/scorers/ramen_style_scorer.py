from frex.scorers import CandidateScorer
from examples.ramen_rec.app.models.ramen_context import RamenContext
from examples.ramen_rec.app.models.ramen_candidate import RamenCandidate


class RamenStyleScorer(CandidateScorer):

    def score(self, *, context: RamenContext, candidate: RamenCandidate) -> float:
        if context.target_ramen.style == candidate.domain_object.style:
            return 1
        else:
            return 0
