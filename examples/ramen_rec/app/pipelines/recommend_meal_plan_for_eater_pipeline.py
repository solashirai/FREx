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
        self, *, vector_file: Path, ramen_query_service: GraphRamenQueryService,
        num_days: int = 2,
        ramens_per_day: int = 3,
        min_daily_rating: int = 7,
        max_daily_price: int = 7,
        max_total_price: int = 13,
    ):
        self.ramen_candidate_pipe = RecommendForEaterPipeline(vector_file=vector_file,
                                                              ramen_query_service=ramen_query_service)
        _Pipeline.__init__(
            self,
            candidate_generators=(
                RamenMealPlanCandidateGenerator(
                    num_days=num_days,
                    ramens_per_day=ramens_per_day,
                    min_daily_rating=min_daily_rating,
                    max_daily_price=max_daily_price,
                    max_total_price=max_total_price,
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
