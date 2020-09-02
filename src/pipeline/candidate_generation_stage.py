from src.pipeline.pipeline_stage import PipelineStage
from src.models.candidate import Candidate
from src.models.context import Context
from src.services.generator_service import GeneratorService
from typing import Tuple


class CandidateGenerationStage(PipelineStage):

    """
    ? something doesn't smell right
    """

    def __init__(self, *, candidate_generator: GeneratorService):
        self.candidate_generator = candidate_generator

    def execute(self, *, context: Context, candidates: Tuple[Candidate, ...]) -> Tuple[Context, Tuple[Candidate, ...]]:
        output_candidates = self.candidate_generator.get_candidates(context=context)

        return context, output_candidates
