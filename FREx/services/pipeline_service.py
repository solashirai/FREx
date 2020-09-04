from abc import ABC
from typing import Tuple
from FREx.models import Candidate, Context
from abc import ABC, abstractmethod


class PipelineService(ABC):

    @abstractmethod
    def execute(self, *, context: Context, candidates: Tuple[Candidate, ...]) -> \
            Tuple[Context, Tuple[Candidate, ...]]:
        pass
