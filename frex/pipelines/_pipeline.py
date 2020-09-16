from abc import ABC
from typing import Generator, Tuple
from frex.models import Candidate, Context
from frex.pipeline_stages import _PipelineStage
from abc import ABC, abstractmethod


class _Pipeline(ABC):
    def __init__(self, *, stages: Tuple[_PipelineStage, ...]):
        self.stages = stages

    def __call__(
        self,
        *,
        context: Context = None,
        candidates: Generator[Candidate, None, None] = ()
    ) -> Generator[Candidate, None, None]:
        for stage in self.stages:
            candidates = stage(context=context, candidates=candidates)
        return candidates
