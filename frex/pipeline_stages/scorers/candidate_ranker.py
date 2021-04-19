from typing import Tuple, Generator, Any
from frex.models import Explanation, Candidate
from frex.pipeline_stages import PipelineStage


class CandidateRanker(PipelineStage):
    """
    CandidateRanker is a PipelineStage that will sort the current candidates. Sorting is performed based on the
    total_score property of candidates, which sums up the applied_scores currently applied to the candidate.

    Sorting needs to collect all candidates coming in from the generator, so it should be used infrequently.
    """

    def __call__(
        self, *, candidates: Generator[Candidate, None, None], context: Any
    ) -> Generator[Candidate, None, None]:
        """
        Collect all candidates being yielded by an input Generator, sort them based on their total_score, and yield
        the sorted candidates in descending order.

        :param candidates: A Generator yielding candidates. In the setup of a FREx Pipeline, this is typically another
            PipelineStage that is yielding candidates into the next stage.
        :param context: The current context being used to execute the Pipeline.
        :return: A Generator, yielding Candidate objects in order based on their total_score property.
        """
        all_candidates = list(candidates)

        sorted_candidates = sorted(
            all_candidates, key=lambda c: c.total_score, reverse=True
        )
        for sorted_candidate in sorted_candidates:
            yield sorted_candidate
