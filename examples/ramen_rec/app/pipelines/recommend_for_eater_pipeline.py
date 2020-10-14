from frex.models import Explanation
from frex.pipelines import _Pipeline
from frex.pipeline_stages.scorers import CandidateRanker
from examples.ramen_rec.app import *
from pathlib import Path


class RecommendForEaterPipeline(_Pipeline):
    """
    A pipeline to recommend ramens for a specific ramen eater.
    """

    def __init__(
        self, *, vector_file: Path, ramen_query_service: GraphRamenQueryService
    ):
        _Pipeline.__init__(
            self,
            candidate_generators=(
                MatchEaterLikesRamenCandidateGenerator(
                    ramen_vector_file=vector_file.resolve(),
                    ramen_query_service=ramen_query_service,
                    generator_explanation=Explanation(
                        explanation_string=f"This ramen is identified as being similar to all of the user's favorite ramens."
                    ),
                ),
            ),
            stages=(
                RamenEaterProhibitCountryFilter(
                    filter_explanation=Explanation(
                        explanation_string="This ramen is not from a country that is prohibited by the eater."
                    )
                ),
                RamenRatingScorer(
                    scoring_explanation=Explanation(
                        explanation_string="This ramen has a high rating score."
                    )
                ),
                RamenEaterLikesBrandScorer(
                    success_scoring_explanation=Explanation(
                        explanation_string="This ramen is from a brand that the user likes."
                    ),
                    failure_scoring_explanation=Explanation(
                        explanation_string="This ramen is from not a brand that the user likes."
                    ),
                ),
                RamenEaterLikesStyleScorer(
                    success_scoring_explanation=Explanation(
                        explanation_string="This ramen is a style that the user likes."
                    ),
                    failure_scoring_explanation=Explanation(
                        explanation_string="This ramen is not a style that the user likes."
                    ),
                ),
                RamenEaterLikesCountryScorer(
                    success_scoring_explanation=Explanation(
                        explanation_string="This ramen is from a country that the user likes."
                    ),
                    failure_scoring_explanation=Explanation(
                        explanation_string="This ramen is from not a country that the user likes."
                    ),
                ),
                CandidateRanker(),
            ),
        )
