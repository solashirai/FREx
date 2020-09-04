from abc import abstractmethod
from FREx.models.context import Context
from typing import Tuple
from FREx.models import Candidate
from FREx.services import PipelineService


class CandidateGeneratorService(PipelineService):

    @abstractmethod
    def get_candidates(self, *, context: Context) -> Tuple[Candidate, ...]:
        pass

    def execute(self, *, context: Context, candidates: Tuple[Candidate, ...]) -> \
            Tuple[Context, Tuple[Candidate, ...]]:
        output_candidates = self.get_candidates(context=context)

        return context, output_candidates
