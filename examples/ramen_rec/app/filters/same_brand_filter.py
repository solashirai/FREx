from frex.pipeline_stages.filters import CandidateFilterer
from examples.ramen_rec.app.models.ramen_context import RamenContext
from examples.ramen_rec.app.models.ramen_candidate import RamenCandidate


class SameBrandFilter(CandidateFilterer):

    def filter(self, *, candidate: RamenCandidate) -> bool:
        """
        Filter out candidate ramens with the same brand as the input context ramen.
        """
        return candidate.context.target_ramen.brand == candidate.domain_object.brand
