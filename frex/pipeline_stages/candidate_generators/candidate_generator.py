from abc import abstractmethod
from frex.models.context import Context
from typing import Generator, List, Callable
from frex.models import Candidate
from frex.pipeline_stages import _PipelineStage


class CandidateGenerator(_PipelineStage):
    @abstractmethod
    def __call__(
        self, *, context: Context, candidates: Generator[Candidate, None, None] = None
    ) -> Generator[Candidate, None, None]:
        pass
