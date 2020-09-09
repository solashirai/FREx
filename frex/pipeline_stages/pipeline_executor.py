from typing import Tuple, Generator
from frex.pipeline_stages import _Pipeline
from frex.models import Context, Candidate


class PipelineExecutor(_Pipeline):

    def __init__(self, *, stages: Tuple[_Pipeline, ...]):
        self.stages = stages

    def execute(self, *, context: Context = None, candidates: Generator[Candidate, None, None] = ()) -> \
            Generator[Candidate, None, None]:
        for stage in self.stages:
            candidates = stage.execute(context=context, candidates=candidates)
        return candidates
