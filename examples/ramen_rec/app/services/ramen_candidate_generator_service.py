from src.services.candidate_generator_service import CandidateGeneratorService
from examples.ramen_rec.app.models.ramen_eater_context import RamenEaterContext
from src.stores.graph.sparql_queryable import SparqlQueryable
from typing import Tuple, Optional
from src.models.candidate import Candidate
from src.models.context import Context


class RamenCandidateGeneratorService(CandidateGeneratorService):

    def __init__(self):
        pass

    def get_candidates(self, *, context: Context) -> Tuple[Candidate, ...]:
        return ()
