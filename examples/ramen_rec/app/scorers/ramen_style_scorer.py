from frex.pipeline_stages.scorers import CandidateScorer
from examples.ramen_rec.app.models import RamenContext
from examples.ramen_rec.app.models import RamenCandidate


class RamenStyleScorer(CandidateScorer):
    def score(self, *, candidate: RamenCandidate) -> float:
        if candidate.context.target_ramen.style == candidate.domain_object.style:
            return 1
        else:
            return 0
