from abc import abstractmethod
from frex.models import Explanation
from typing import Generator, Optional
from frex.models import Candidate
from frex.pipeline_stages import _PipelineStage


class CandidateGenerator(_PipelineStage):
    def __init__(self, *,
                 generator_explanation: Explanation,
                 **kwargs):
        self.generator_explanation = generator_explanation
        _PipelineStage.__init__(self, **kwargs)

    @abstractmethod
    def __call__(
        self, *, candidates: Generator[Candidate, None, None] = None
    ) -> Generator[Candidate, None, None]:
        pass
