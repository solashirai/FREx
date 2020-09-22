from abc import ABC
from typing import Generator, Callable, Optional
from frex.models import Candidate
from abc import ABC, abstractmethod


class _PipelineStage(ABC):

    @abstractmethod
    def __call__(self, *, candidates: Generator[Candidate, None, None]) -> Generator[Candidate, None, None]:
        pass
