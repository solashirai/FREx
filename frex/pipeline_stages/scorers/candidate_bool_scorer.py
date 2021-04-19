from abc import abstractmethod
from typing import Tuple, Generator, Any
from frex.models import Explanation, Candidate
from frex.pipeline_stages import PipelineStage


class CandidateBoolScorer(PipelineStage):
    """
    CandidateBoolScorer is a scoring pipeline stage that scores based on whether or not the candidate matches some
    given condition. The score function for this class returns a bool indicating whether the condition was matched,
    and an appropriate explanation is attached to the candidate.
    """

    def __init__(
        self,
        *,
        success_scoring_explanation: Explanation,
        failure_scoring_explanation: Explanation,
        **kwargs
    ):
        """
        :param success_scoring_explanation: The explanation to add to the Candidate after applying the scoring function
            if the score function indicates True.
        :param failure_scoring_explanation: The explanation to add to the Candidate after applying the scoring function
            if the score function indicates False.
        """
        self.success_scoring_explanation = success_scoring_explanation
        self.failure_scoring_explanation = failure_scoring_explanation

    @abstractmethod
    def score(self, *, candidate: Candidate) -> Tuple[bool, float]:
        """
        Apply a custom scoring function to the input candidate that also checks for the success of some condition.

        :param candidate: A domain-specific candidate to apply the scoring function
        :return: A tuple (x, y) where x is a boolean indicating whether the candidate passed some condition and y
            is the score applied to the candidate.
        """
        pass

    def __call__(
        self, *, candidates: Generator[Candidate, None, None], context: Any
    ) -> Generator[Candidate, None, None]:
        """
        For each of candidate being yielded by the Generator, apply a scoring function to the candidate and
        yield it as output. Based on whether or not the scoring function passed some condition, different explanations
        are applied.

        :param candidates: A Generator yielding candidates. In the setup of a FREx Pipeline, this is typically another
            PipelineStage that is yielding candidates into the next stage.
        :param context: The current context being used to execute the Pipeline.
        :return: A Generator, yielding updated Candidate objects that have this stage's scoring function applied.
        """
        for candidate in candidates:
            success, score = self.score(candidate=candidate)
            if success:
                candidate.applied_explanations.append(self.success_scoring_explanation)
            else:
                candidate.applied_explanations.append(self.failure_scoring_explanation)
            candidate.applied_scores.append(score)
            yield candidate
