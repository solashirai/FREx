from examples.ramen_rec.tests.conftest import TestRamens
from examples.ramen_rec.app.services import GraphRamenEaterQueryService


def test_get_ramen_eater_by_uri(
    graph_ramen_eater_query_service: GraphRamenEaterQueryService, test_ramen_eater_01
):
    res = graph_ramen_eater_query_service.get_ramen_eater_by_uri(
        ramen_eater_uri=TestRamens.test_ramen_eater_01
    )

    assert test_ramen_eater_01 == res
