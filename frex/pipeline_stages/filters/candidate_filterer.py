from abc import abstractmethod
from typing import Generator, Optional, Any
from frex.models import Explanation, Candidate
from frex.pipeline_stages import PipelineStage


class CandidateFilterer(PipelineStage):
    """
    CandidateFilterer is a PipelineStage that determines whether input candidates should be removed from consideration
    or continue on through the FREx Pipeline.

    A new CandidateFilterer class can be minimally defined by creating a new subclass of CandidateFilterer and
    defining the filter() function.
    """

    def __init__(
        self, *, filter_explanation: Explanation, filter_score: float = 0, **kwargs
    ):
        """
        :param filter_explanation: The explanation to add to the Candidate if it passes the filter function.
        :param filter_score: The score to apply to the candidate if it passes the filter. This is 0 by default.
        """
        self.filter_explanation = filter_explanation
        self.filter_score = filter_score

    @abstractmethod
    def filter(self, *, candidate: Candidate) -> bool:
        """
        A filter to determine whether or not the current candidate is suitable to move on through the Pipeline.
        This function should return True when the candidate should be removed and False when it should continue on.

        :param candidate: A domain-specific candidate to filter
        :return: True if the candidate should be removed, False if it should be kept and passed on to later stages.
        """
        pass

    def __call__(
        self, *, candidates: Generator[Candidate, None, None], context: Any
    ) -> Generator[Candidate, None, None]:
        """
        For each of candidate being yielded by the Generator, apply a filtering function to decide whether or not
        to yield the candidate forward to the next PipelineStage.



        :param candidates: A Generator yielding candidates. In the setup of a FREx Pipeline, this is typically another
        PipelineStage that is yielding candidates into the next stage.
        :param context: The current context being used to execute the Pipeline.
        :return: A Generator, yielding updated Candidate objects that have not been caught by this stage's filtering
         function.
        """
        for candidate in candidates:
            if not self.filter(candidate=candidate):
                candidate.applied_explanations.append(self.filter_explanation)
                candidate.applied_scores.append(self.filter_score)
                yield candidate
