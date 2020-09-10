from frex.pipeline_stages.scorers import CandidateBoolScorer
from examples.ramen_rec.app.models import RamenEaterContext
from examples.ramen_rec.app.models import RamenCandidate
from typing import Tuple


class RamenEaterLikesBrandScorer(CandidateBoolScorer):
    def score(self, *, context: RamenEaterContext, candidate: RamenCandidate) -> Tuple[bool, float]:
        if context.ramen_eater_profile.likes_ramen_brand == candidate.domain_object.brand:
            return True, 1
        else:
            return False, 0
