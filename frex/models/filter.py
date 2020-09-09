from frex.models import Context, Candidate
from abc import ABC, abstractmethod


class Filter(ABC):

    @abstractmethod
    def filter_input(self, *, context: Context, candidate: Candidate) -> bool:
        pass
