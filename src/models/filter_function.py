from abc import ABC, abstractmethod
from typing import NamedTuple
from src.models.candidate import Candidate
from src.models.context import Context


class FilterFunction(ABC):

    @abstractmethod
    def filter(self, *, candidate: Candidate, context: Context) -> bool:
        pass
