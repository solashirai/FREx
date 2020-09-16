from abc import ABC
from typing import Generator, Callable, Optional
from frex.models import Candidate
from abc import ABC, abstractmethod


class _PipelineStage(ABC):

    def __init__(self, *, context: Optional[object] = None):
        self.context = context

    def set_context(self, *, context: object):
        self.context = context

    @abstractmethod
    def __call__(self, *, candidates: Generator[Candidate, None, None]) -> Generator[Candidate, None, None]:
        pass
