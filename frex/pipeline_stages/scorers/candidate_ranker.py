from typing import Tuple, Generator
from frex.models import Explanation, Candidate
from frex.pipeline_stages import _PipelineStage


class CandidateRanker(_PipelineStage):
    def __call__(
        self, *, candidates: Generator[Candidate, None, None]
    ) -> Generator[Candidate, None, None]:
        all_candidates = list(candidates)

        sorted_candidates = sorted(
            all_candidates, key=lambda c: c.total_score, reverse=True
        )
        for sorted_candidate in sorted_candidates:
            yield sorted_candidate
