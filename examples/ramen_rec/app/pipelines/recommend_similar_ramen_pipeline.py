from frex.models import Explanation
from frex.pipelines import Pipeline
from frex.pipeline_stages.scorers import CandidateRanker
from examples.ramen_rec.app.scorers import *
from examples.ramen_rec.app.filters import *
from examples.ramen_rec.app.candidate_generators import *
from examples.ramen_rec.app.services import *
from pathlib import Path


class RecommendSimilarRamenPipeline(Pipeline):
    """
    A pipeline to recommend ramens similar to an input ramen context.
    """

    def __init__(
        self, *, vector_file: Path, ramen_query_service: GraphRamenQueryService
    ):
        Pipeline.__init__(
            self,
            stages=(
                SimilarRamenCandidateGenerator(
                    ramen_vector_file=vector_file.resolve(),
                    ramen_query_service=ramen_query_service,
                    generator_explanation=Explanation(
                        explanation_string=f"This ramen is identified as being similar to the target ramen."
                    ),
                ),
                SameBrandFilter(
                    filter_explanation=Explanation(
                        explanation_string="This ramen is from a different brand than the target ramen."
                    )
                ),
                RamenRatingScorer(
                    scoring_explanation=Explanation(
                        explanation_string="This ramen has a high rating score."
                    )
                ),
                RamenStyleScorer(
                    scoring_explanation=Explanation(
                        explanation_string="This ramen is the same style as the target ramen."
                    )
                ),
                CandidateRanker(),
            ),
        )
