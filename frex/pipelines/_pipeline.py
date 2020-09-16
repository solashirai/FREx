from abc import ABC
from typing import Generator, Tuple, Optional
from frex.models import Candidate
from frex.pipeline_stages import _PipelineStage
from abc import ABC, abstractmethod


class _Pipeline(ABC):
    def __init__(self, *, context: Optional[object] = None, stages: Tuple[_PipelineStage, ...]):
        self.context = context
        for stage in stages:
            stage.set_context(context=context)
        self.stages = stages

    def __call__(
        self,
        *,
        candidates: Optional[Generator[Candidate, None, None]] = ()
    ) -> Generator[Candidate, None, None]:
        for stage in self.stages:
            candidates = stage(candidates=candidates)
        return candidates
