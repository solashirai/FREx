from frex.pipeline_stages.scorers import CandidateBoolScorer
from examples.ramen_rec.app.models import RamenEaterContext
from examples.ramen_rec.app.models import RamenCandidate
from typing import Tuple


class RamenEaterLikesCountryScorer(CandidateBoolScorer):
    def score(self, *, candidate: RamenCandidate) -> Tuple[bool, float]:
        if (
            candidate.context.ramen_eater_profile.likes_ramen_from
            == candidate.domain_object.country
        ):
            return True, 1
        else:
            return False, 0
