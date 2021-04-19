from abc import abstractmethod
from typing import Tuple, Generator, Any
from frex.models import Explanation, Candidate
from frex.pipeline_stages import PipelineStage


class CandidateScorer(PipelineStage):
    """
    CandidateScorer is a PipelineStage that applies some score to candidates. The scoring function must be defined
    in the particular application that is utilizing FREx.

    A new CandidateScorer class can be minimally defined by creating a new subclass of CandidateScorer
    and defining the score() function.
    """

    def __init__(self, *, scoring_explanation: Explanation, **kwargs):
        """
        :param scoring_explanation: The explanation to add to the Candidate after applying the scoring function.
        """
        self.scoring_explanation = scoring_explanation

    @abstractmethod
    def score(self, *, candidate: Candidate) -> float:
        """
        Apply a custom scoring function to the input candidate.

        :param candidate: A domain-specific candidate to apply the scoring function
        :return: A score applied to be applied the candidate based on the implemented scoring function.
        """
        pass

    def __call__(
        self, *, candidates: Generator[Candidate, None, None], context: Any
    ) -> Generator[Candidate, None, None]:
        """
        For each of candidate being yielded by the Generator, apply a scoring function to the candidate and
        yield it as output.

        :param candidates: A Generator yielding candidates. In the setup of a FREx Pipeline, this is typically another
            PipelineStage that is yielding candidates into the next stage.
        :param context: The current context being used to execute the Pipeline.
        :return: A Generator, yielding updated Candidate objects that have this stage's scoring function applied.
        """
        for candidate in candidates:
            candidate.applied_explanations.append(self.scoring_explanation)
            candidate.applied_scores.append(self.score(candidate=candidate))
            yield candidate
