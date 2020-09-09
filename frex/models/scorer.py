from frex.models import Context, Candidate
from abc import ABC, abstractmethod


class Scorer(ABC):

    @abstractmethod
    def score_input(self, *, context: Context, candidate: Candidate) -> float:
        pass
