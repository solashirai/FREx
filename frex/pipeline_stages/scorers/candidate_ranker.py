from typing import Tuple, Generator, Any
from frex.models import Explanation, Candidate
from frex.pipeline_stages import _PipelineStage


class CandidateRanker(_PipelineStage):
    """
    CandidateRanker is a helper pipeline stage that will sort the current candidates.
    Sorting needs to collect all candidates coming in from the generator, so it should be used infrequently.
    """

    def __call__(
        self, *, candidates: Generator[Candidate, None, None], context: Any
    ) -> Generator[Candidate, None, None]:
        all_candidates = list(candidates)

        sorted_candidates = sorted(
            all_candidates, key=lambda c: c.total_score, reverse=True
        )
        for sorted_candidate in sorted_candidates:
            yield sorted_candidate
