from __future__ import annotations
from abc import ABC
from typing import Generator, Tuple, Optional, Union
from frex.models import Candidate
from frex.pipeline_stages import PipelineStage, CandidateGenerator
from abc import ABC, abstractmethod


class Pipeline:
    """
    The base Pipeline class that will run a recommendation pipeline.

    Custom Pipelines should be implemented by extending this base class.
    """

    def __init__(
        self,
        *,
        stages: Tuple[Union[PipelineStage, Pipeline], ...],
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
