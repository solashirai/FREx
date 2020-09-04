from abc import ABC, abstractmethod
from src.models.context import Context
from src.stores.graph.sparql_queryable import SparqlQueryable
from typing import Tuple, Optional
from src.models.candidate import Candidate
from src.services.pipeline_service import PipelineService


class CandidateGeneratorService(PipelineService):

    @abstractmethod
    def get_candidates(self, *, context: Context) -> Tuple[Candidate, ...]:
        pass

    def execute(self, *, context: Context, candidates: Tuple[Candidate, ...]) -> \
            Tuple[Context, Tuple[Candidate, ...]]:
        output_candidates = self.get_candidates(context=context)

        return context, output_candidates
