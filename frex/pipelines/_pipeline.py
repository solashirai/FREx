from __future__ import annotations
from abc import ABC
from typing import Generator, Tuple, Optional, Union
from frex.models import Candidate
from frex.pipeline_stages import _PipelineStage, CandidateGenerator
from abc import ABC, abstractmethod


class _Pipeline(ABC):
    """
    Pipelines should be implemented using _Pipeline, separately specifying candidate generator and
    stages to pass all candidates through.
    """

    def __init__(
        self,
        *,
        stages: Tuple[Union[_PipelineStage, _Pipeline], ...],
    ):
        self.stages = stages

    def __call__(
        self,
        *,
        candidates: Optional[Generator[Candidate, None, None]] = None,
        context: Optional[object] = None,
    ) -> Generator[Candidate, None, None]:
        for stage in self.stages:
            candidates = stage(context=context, candidates=candidates)
        return candidates
