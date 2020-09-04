from typing import Tuple
from src.services.pipeline_service import PipelineService
from src.models.candidate import Candidate
from src.models.context import Context


class PipelineExecutorService(PipelineService):

    def __init__(self, *, stages: Tuple[PipelineService, ...]):
        self.stages = stages

    def execute(self, *, context: Context, candidates: Tuple[Candidate, ...]) -> Tuple[Context, Tuple[Candidate, ...]]:
        for stage in self.stages:
            context, candidates = stage.execute(context=context, candidates=candidates)
        return context, candidates
