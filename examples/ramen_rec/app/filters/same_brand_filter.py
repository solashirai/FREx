from frex.filters import CandidateFilterer
from examples.ramen_rec.app.models.ramen_context import RamenContext
from examples.ramen_rec.app.models.ramen_candidate import RamenCandidate


class SameBrandFilter(CandidateFilterer):

    def filter(self, *, context: RamenContext, candidate: RamenCandidate) -> bool:
        return context.target_ramen.brand == candidate.domain_object.brand
