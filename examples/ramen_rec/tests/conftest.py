import pytest
import rdflib
from rdflib import Namespace, URIRef
from examples.ramen_rec.app import *
from frex.stores import LocalGraph
from frex.models import Explanation
from frex.pipeline_stages.scorers import CandidateScorer, CandidateBoolScorer
from frex.pipeline_stages.filters import CandidateFilterer

ramen_onto_ns = Namespace("http://www.frex.com/examples/ramenOnto/")
ramen_ns = Namespace("http://www.frex.com/examples/ramen/")
ex_ns = Namespace("http://www.frex.com/examples/")
data_files = (
    (RamenUtils.DATA_DIR / "ramen-ratings.ttl").resolve(),
    (RamenUtils.DATA_DIR / "ramen-users.ttl").resolve(),
)
vector_file = (RamenUtils.DATA_DIR / "ramen-vectors.pkl").resolve()


@pytest.fixture(scope="session")
def ramen_graph() -> LocalGraph:
    g = LocalGraph(file_paths=data_files)
    return g


@pytest.fixture(scope="session")
def graph_ramen_query_service(ramen_graph) -> GraphRamenQueryService:
    ramen_q = GraphRamenQueryService(queryable=ramen_graph)
    return ramen_q


@pytest.fixture(scope="session")
def graph_ramen_eater_query_service(ramen_graph) -> GraphRamenEaterQueryService:
    ramen_q = GraphRamenEaterQueryService(queryable=ramen_graph)
    return ramen_q


@pytest.fixture(scope="session")
def ramen_candidate_generator(
    graph_ramen_query_service, test_ramen_101
) -> SimilarRamenCandidateGenerator:
    return SimilarRamenCandidateGenerator(
        ramen_vector_file=vector_file,
        ramen_query_service=graph_ramen_query_service,
        generator_explanation=Explanation(
            explanation_string=f"This ramen is identified as being similar to the target ramen."
        ),
        context=RamenContext(target_ramen=test_ramen_101),
    )


@pytest.fixture(scope="session")
def ramen_eater_candidate_generator(
    graph_ramen_query_service,
) -> MatchEaterLikesRamenCandidateGenerator:
    return MatchEaterLikesRamenCandidateGenerator(
        ramen_vector_file=vector_file,
        ramen_query_service=graph_ramen_query_service,
    )


@pytest.fixture(scope="session")
def rating_scorer() -> CandidateScorer:
    return RamenRatingScorer(
        scoring_explanation=Explanation(
            explanation_string="This ramen has a high rating score."
        )
    )


@pytest.fixture(scope="session")
def style_scorer() -> CandidateScorer:
    return RamenStyleScorer(
        scoring_explanation=Explanation(
            explanation_string="This ramen is the same style as the target ramen."
        )
    )


@pytest.fixture(scope="session")
def same_brand_filterer() -> CandidateFilterer:
    return SameBrandFilter(
        filter_explanation=Explanation(
            explanation_string="This ramen is from a different brand than the target ramen"
        )
    )


@pytest.fixture(scope="session")
def prohibited_country_filterer() -> CandidateFilterer:
    return RamenEaterProhibitCountryFilter(
        filter_explanation=Explanation(
            explanation_string="This ramen is not from a prohibited country."
        )
    )


@pytest.fixture(scope="session")
def likes_style_scorer() -> CandidateBoolScorer:
    return RamenEaterLikesStyleScorer(
        success_scoring_explanation=Explanation(
            explanation_string="This ramen is a style that the user likes."
        ),
        failure_scoring_explanation=Explanation(
            explanation_string="This ramen is not a style that the user likes."
        ),
    )


@pytest.fixture(scope="session")
def likes_country_scorer() -> CandidateBoolScorer:
    return RamenEaterLikesCountryScorer(
        success_scoring_explanation=Explanation(
            explanation_string="This ramen is from a country that the user likes."
        ),
        failure_scoring_explanation=Explanation(
            explanation_string="This ramen is from not a country that the user likes."
        ),
    )


@pytest.fixture(scope="session")
def likes_brand_scorer() -> CandidateBoolScorer:
    return RamenEaterLikesBrandScorer(
        success_scoring_explanation=Explanation(
            explanation_string="This ramen is from a brand that the user likes."
        ),
        failure_scoring_explanation=Explanation(
            explanation_string="This ramen is not from a brand that the user likes."
        ),
    )


@pytest.fixture(scope="session")
def sim_ramen_pipe(
    graph_ramen_query_service, test_ramen_101
) -> RecommendSimilarRamenPipeline:
    return RecommendSimilarRamenPipeline(
        ramen_query_service=graph_ramen_query_service, vector_file=vector_file
    )


@pytest.fixture(scope="session")
def mealplan_pipe(graph_ramen_query_service) -> RecommendMealPlanForEaterPipeline:
    return RecommendMealPlanForEaterPipeline(
        vector_file=vector_file,
        ramen_query_service=graph_ramen_query_service,
        num_days=2,
        ramens_per_day=3,
        min_daily_rating=7,
        max_daily_price=7,
        max_total_price=13,
    )


@pytest.fixture(scope="session")
def test_ramen_101() -> Ramen:
    return Ramen(
        uri=ramen_ns["101"],
        label="Artificial Sesame Chicken",
        brand="Ve Wong",
        rating=4.25,
        country="Taiwan",
        style="Pack",
        price=2.8,
    )


@pytest.fixture(scope="session")
def test_ramen_202() -> Ramen:
    return Ramen(
        uri=ramen_ns["202"],
        label="Bowl Noodle Cabbage Kimchi",
        brand="Nongshim",
        rating=3.25,
        country="USA",
        style="Bowl",
        price=2.65,
    )


@pytest.fixture(scope="session")
def test_ramen_103() -> Ramen:
    return Ramen(
        uri=ramen_ns["103"],
        label="Vegetarian Flavor",
        brand="Ve Wong",
        rating=3.0,
        country="Taiwan",
        style="Pack",
        price=3.23,
    )


@pytest.fixture(scope="session")
def test_ramen_1011() -> Ramen:
    return Ramen(
        uri=ramen_ns["1011"],
        label="Bowl Hot & Spicy Chicken Flavor Ramen Noodles With Vegetables",
        brand="Maruchan",
        rating=4.0,
        country="USA",
        style="Bowl",
        price=2.79,
    )


@pytest.fixture(scope="session")
def test_ramen_eater_01() -> RamenEater:
    return RamenEater(
        uri=ex_ns["USR01"],
        likes_ramen_from="Taiwan",
        likes_ramen_brand="Maruchan",
        likes_ramen_style="Pack",
        prohibit_ramen_from="USA",
        favorite_ramen_uris=frozenset(
            [
                URIRef("http://www.frex.com/examples/ramen/101"),
                URIRef("http://www.frex.com/examples/ramen/1011"),
            ]
        ),
    )


@pytest.fixture(scope="session")
def test_ramen_eater_01_context(test_ramen_eater_01) -> RamenEaterContext:
    return RamenEaterContext(ramen_eater_profile=test_ramen_eater_01)


def placeholder_ramen_candidate(dom_obj: Ramen, context) -> RamenCandidate:
    return RamenCandidate(
        context=context,
        domain_object=dom_obj,
        applied_explanations=[],
        applied_scores=[],
    )


class TestRamens:
    test_ramen_101_uri = ramen_ns["101"]
    test_ramen_202_uri = ramen_ns["202"]
    test_ramen_103_uri = ramen_ns["103"]
    test_ramen_eater_01 = ex_ns["USR01"]
