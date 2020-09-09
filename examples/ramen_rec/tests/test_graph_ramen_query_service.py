from examples.ramen_rec.tests.conftest import TestRamens
from examples.ramen_rec.app.services import GraphRamenQueryService


def test_get_ramen_by_uri(graph_ramen_query_service: GraphRamenQueryService,
                          test_ramen_101):
    res = graph_ramen_query_service.get_ramen_by_uri(ramen_uri=TestRamens.test_ramen_101_uri)

    assert test_ramen_101 == res


def test_get_ramens_by_uri(graph_ramen_query_service: GraphRamenQueryService,
                           test_ramen_101, test_ramen_202):
    res = graph_ramen_query_service.get_ramens_by_uri(ramen_uris=[TestRamens.test_ramen_101_uri,
                                                                  TestRamens.test_ramen_202_uri])

    assert [test_ramen_101, test_ramen_202] == list(res)
