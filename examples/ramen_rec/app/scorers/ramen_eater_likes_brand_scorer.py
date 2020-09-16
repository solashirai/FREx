from frex.pipeline_stages.scorers import CandidateBoolScorer
from frex.models import Explanation
from examples.ramen_rec.app.models import RamenEaterContext
from examples.ramen_rec.app.models import RamenCandidate
from typing import Tuple


class RamenEaterLikesBrandScorer(CandidateBoolScorer):
    context: RamenEaterContext

    def score(
        self, *, candidate: RamenCandidate
    ) -> Tuple[bool, float]:
        if (
            self.context.ramen_eater_profile.likes_ramen_brand
            == candidate.domain_object.brand
        ):
            return True, 0.9
        else:
            return False, 0
