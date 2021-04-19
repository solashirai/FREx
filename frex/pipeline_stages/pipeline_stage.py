from abc import ABC
from typing import Generator, Callable, Optional, Any
from frex.models import Candidate
from abc import ABC, abstractmethod


class PipelineStage(ABC):
    """
    This is the base class for custom stages that will be run in a pipeline.

    PipelineStages are callable classes which should take input candidates and context and yield out candidates.
    Candidates yielded by a PipelineStage might be entirely new (e.g., a generator stage generated new candidates) or
    they may be updated in some way (e.g., a scorer stage added a new score to an existing candidate that was passed
    in).
    """

    @abstractmethod
    def __call__(
        self, *, candidates: Generator[Candidate, None, None], context: Any
    ) -> Generator[Candidate, None, None]:
        """
        Execute some function to apply and yield new or updated candidates.

        :param candidates: A Generator yielding candidates. In the setup of a FREx Pipeline, this is typically another
            PipelineStage that is yielding candidates into the next stage.
        :param context: The current context being used to execute the Pipeline.
        :return: A Generator, yielding new Candidate objects.
        """
        pass
