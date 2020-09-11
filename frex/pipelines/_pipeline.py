from abc import ABC
from typing import Generator
from frex.models import Candidate, Context
from abc import ABC, abstractmethod


class _Pipeline(ABC):
    @abstractmethod
    def execute(
        self, *, context: Context, candidates: Generator[Candidate, None, None]
    ) -> Generator[Candidate, None, None]:
        pass
