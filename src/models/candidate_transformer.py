from abc import ABC, abstractmethod
from typing import Tuple, NamedTuple
from src.models.candidate import Candidate


class CandidateTransformer(ABC):

    """
    ? why am i here
    """

    @abstractmethod
    def transform_candidates(self, *, candidates: Tuple[Candidate, ...]) -> \
            Tuple[Candidate, ...]:
        pass
