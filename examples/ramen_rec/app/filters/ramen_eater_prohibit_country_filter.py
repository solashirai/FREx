from frex.pipeline_stages.filters import CandidateFilterer
from examples.ramen_rec.app.models import RamenEaterContext
from examples.ramen_rec.app.models import RamenCandidate


class RamenEaterProhibitCountryFilter(CandidateFilterer):

    def filter(self, *, candidate: RamenCandidate) -> bool:
        """
        Filter out candidate ramens based on the ramen eater's context, which contains prohibited countries.
        """
        return (
            candidate.context.ramen_eater_profile.prohibit_ramen_from
            == candidate.domain_object.country
        )
