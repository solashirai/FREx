from typing import Tuple
from src.pipeline.pipeline_stage import PipelineStage
from src.models.candidate import Candidate
from src.models.context import Context


class Pipeline:

    def __init__(self, *, stages: Tuple[PipelineStage, ...]):
        self.stages = stages

    def execute(self, *, context: Context, candidates: Tuple[Candidate, ...]) -> Tuple[Context, Tuple[Candidate, ...]]:
        for stage in self.stages:
            context, candidates = stage.execute(context=context, candidates=candidates)
        return context, candidates
