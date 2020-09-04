from typing import Tuple
from FREx.services import PipelineService
from FREx.models import Context, Candidate


class PipelineExecutorService(PipelineService):

    def __init__(self, *, stages: Tuple[PipelineService, ...]):
        self.stages = stages

    def execute(self, *, context: Context = None, candidates: Tuple[Candidate, ...] = ()) -> \
            Tuple[Context, Tuple[Candidate, ...]]:
        for stage in self.stages:
            context, candidates = stage.execute(context=context, candidates=candidates)
        return context, candidates
