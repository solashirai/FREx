from frex.models import Explanation, Context
from frex.stores import LocalGraph
from frex.pipelines import _Pipeline
from frex.pipeline_stages.scorers import CandidateRanker
from examples.ramen_rec.app import *
from rdflib import URIRef
from typing import List
import sys
from pathlib import Path


class RecommendSimilarRamenPipeline(_Pipeline):
    def __init__(
        self, *, vector_file: Path, ramen_query_service: GraphRamenQueryService
    ):
        _Pipeline.__init__(
            self,
            stages=(
                SimilarRamenCandidateGenerator(
                    ramen_vector_file=vector_file.resolve(),
                    ramen_query_service=ramen_query_service,
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
