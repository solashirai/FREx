import pytest
from rdflib import Namespace
from examples.ramen_rec.app import *
from frex.stores import LocalGraph
from frex.models import Explanation
from frex.pipeline_stages.scorers import CandidateScorer
from frex.pipeline_stages.filters import CandidateFilterer

ramen_onto_ns = Namespace("http://www.frex.com/examples/ramenOnto/")
ramen_ns = Namespace("http://www.frex.com/examples/ramen/")
data_files = [
    (RamenUtils.DATA_DIR / "ramen-ratings.ttl").resolve(),
    (RamenUtils.DATA_DIR / "ramen-users.ttl").resolve(),
]


@pytest.fixture(scope="session")
def ramen_graph() -> LocalGraph:
    g = LocalGraph(file_paths=data_files)
    return g


@pytest.fixture(scope="session")
def graph_ramen_query_service(ramen_graph) -> GraphRamenQueryService:
    ramen_q = GraphRamenQueryService(queryable=ramen_graph)
    return ramen_q


@pytest.fixture(scope="session")
def ramen_candidate_generator(
    graph_ramen_query_service,
) -> SimilarRamenCandidateGenerator:
    ram_gen = SimilarRamenCandidateGenerator(
        ramen_vector_file=(RamenUtils.DATA_DIR / "ramen-vectors.pkl").resolve(),
        ramen_query_service=graph_ramen_query_service,
    )
    return ram_gen


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
def test_ramen_101() -> Ramen:
    return Ramen(
        uri=ramen_ns["101"],
        label="Artificial Sesame Chicken",
        brand="Ve Wong",
        rating=4.25,
        country="Taiwan",
        style="Pack",
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
    )


def placeholder_ramen_candidate(dom_obj: Ramen) -> RamenCandidate:
    return RamenCandidate(
        domain_object=dom_obj, applied_explanations=[], applied_scores=[]
    )


class TestRamens:
    test_ramen_101_uri = ramen_ns["101"]
    test_ramen_202_uri = ramen_ns["202"]
    test_ramen_103_uri = ramen_ns["103"]
