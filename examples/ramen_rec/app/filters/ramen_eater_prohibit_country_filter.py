from frex.pipeline_stages.filters import CandidateFilterer
from examples.ramen_rec.app.models import RamenEaterContext
from examples.ramen_rec.app.models import RamenCandidate


class RamenEaterProhibitCountryFilter(CandidateFilterer):
    context: RamenEaterContext

    def filter(self, *, candidate: RamenCandidate) -> bool:
        return (
            self.context.ramen_eater_profile.prohibit_ramen_from
            == candidate.domain_object.country
        )
