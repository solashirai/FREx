from abc import abstractmethod
from frex.models import Explanation
from typing import Generator, Optional, Any
from frex.models import Candidate
from frex.pipeline_stages import PipelineStage


class CandidateGenerator(PipelineStage):
    """
    CandidateGenerator pipeline stages should implement logic in the __call__ method to generate domain-specific
    candidates for the current context.
    """

    def __init__(self, *, generator_explanation: Explanation, **kwargs):
        self.generator_explanation = generator_explanation

    @abstractmethod
    def __call__(
        self,
        *,
        candidates: Optional[Generator[Candidate, None, None]] = None,
        context: Any
    ) -> Generator[Candidate, None, None]:
        pass
