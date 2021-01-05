from abc import ABC
from typing import Generator, Tuple, Optional
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
        candidate_generators: Tuple[CandidateGenerator, ...],
        stages: Tuple[_PipelineStage, ...],
    ):
        self.generators = candidate_generators
        self.stages = stages

    def __call__(
        self,
        *,
        candidates: Optional[Generator[Candidate, None, None]] = None,
        context: Optional[object] = None,
    ) -> Generator[Candidate, None, None]:
        for generator in self.generators:
            candidates = generator(context=context, candidates=candidates)
        for stage in self.stages:
            candidates = stage(candidates=candidates)
        return candidates
