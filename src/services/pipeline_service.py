from abc import ABC
from typing import Tuple
from src.models.candidate import Candidate
from src.models.context import Context
from abc import ABC, abstractmethod


class PipelineService(ABC):

    @abstractmethod
    def execute(self, *, context: Context, candidates: Tuple[Candidate, ...]) -> \
            Tuple[Context, Tuple[Candidate, ...]]:
        pass
