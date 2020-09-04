from src.services.candidate_generator_service import CandidateGeneratorService
from examples.ramen_rec.app.models.ramen_eater_context import RamenEaterContext
from src.stores.graph.sparql_queryable import SparqlQueryable
from typing import Tuple
from src.models.candidate import Candidate


class RamenCandidateGeneratorService(CandidateGeneratorService):

    def get_candidates(self, *, context: RamenEaterContext) -> Tuple[Candidate, ...]:
        return []
