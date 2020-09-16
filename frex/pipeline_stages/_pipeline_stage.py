from abc import ABC
from typing import Generator, Callable
from frex.models import Candidate, Context
from abc import ABC, abstractmethod


class _PipelineStage(ABC, Callable):
    @abstractmethod
    def __call__(self, *args, **kwargs) -> Generator[Candidate, None, None]:
        pass

    # @abstractmethod
    # def __call__(
    #     self, *, context: Context, candidates: Generator[Candidate, None, None]
    # ) -> Generator[Candidate, None, None]:
    #     pass
