from abc import ABC, abstractmethod
from src.models.candidate import Candidate
from src.models.context import Context


class ScoringFunction(ABC):

    @abstractmethod
    def score(self, *, candidate: Candidate, context: Context) -> float:
        pass
