from frex.pipeline_stages.filters import CandidateFilterer
from examples.ramen_rec.app.models.ramen_context import RamenContext
from examples.ramen_rec.app.models.ramen_candidate import RamenCandidate


class SameBrandFilter(CandidateFilterer):
    context: RamenContext

    def filter(self, *, candidate: RamenCandidate) -> bool:
        return self.context.target_ramen.brand == candidate.domain_object.brand
