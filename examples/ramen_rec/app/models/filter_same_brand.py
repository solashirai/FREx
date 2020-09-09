from frex.models import Filter
from examples.ramen_rec.app.models.ramen_context import RamenContext
from examples.ramen_rec.app.models.ramen_candidate import RamenCandidate


class FilterSameBrand(Filter):

    def filter_input(self, *, context: RamenContext, candidate: RamenCandidate) -> bool:
        return context.target_ramen.brand == candidate.domain_object.brand
