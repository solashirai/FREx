from frex.models import Explanation, Candidate
from frex.pipelines import _Pipeline
from examples.ramen_rec.app.pipelines import RecommendForEaterPipeline
from examples.ramen_rec.app.candidate_generators import *
from examples.ramen_rec.app.services import *
from pathlib import Path
from typing import Generator, Optional


class RecommendMealPlanForEaterPipeline(_Pipeline):
    """
    A pipeline to recommend a 'meal plan' of ramens for a specific ramen eater.
    """

    def __init__(
        self, *, vector_file: Path, ramen_query_service: GraphRamenQueryService
    ):
        self.ramen_candidate_pipe = RecommendForEaterPipeline(vector_file=vector_file,
                                                              ramen_query_service=ramen_query_service)
        _Pipeline.__init__(
            self,
            candidate_generators=(
                RamenMealPlanCandidateGenerator(
                    num_days=2,
                    ramens_per_day=3,
                    min_daily_rating=7,
                    max_daily_price=7,
                    max_total_price=13,
                    generator_explanation=Explanation(
                        explanation_string="Based on ramens that you might like, a meal plan was generated."
                    )
                ),
            ),
            stages=(),
        )

    def __call__(
        self,
        *,
        candidates: Optional[Generator[Candidate, None, None]] = None,
        context: Optional[object] = None,
    ) -> Generator[Candidate, None, None]:
        return super(RecommendMealPlanForEaterPipeline, self).__call__(
            candidates=self.ramen_candidate_pipe(candidates=candidates, context=context),
            context=context)
