from abc import ABC, abstractmethod
from typing import Tuple
from src.models.candidate import Candidate
from src.models.context import Context


class PipelineStage(ABC):

    @abstractmethod
    def execute(self, *, context: Context, candidates: Tuple[Candidate, ...]) -> Tuple[Context, Tuple[Candidate, ...]]:
        pass
