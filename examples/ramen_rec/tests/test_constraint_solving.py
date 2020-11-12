from frex.pipeline_stages.scorers import CandidateRanker
from examples.ramen_rec.app.models import RamenContext, RamenEaterContext
from examples.ramen_rec.app.pipelines import *
from examples.ramen_rec.tests.conftest import placeholder_ramen_candidate
from frex.utils import ConstraintSolver, ConstraintType


def test_choose_ramens_using_constraints(
    sim_ramen_pipe,
    test_ramen_101,
):
    pipeline_candidate_results = tuple(
        sim_ramen_pipe(
            context=RamenContext(target_ramen=test_ramen_101),
        )
    )

    solution = (
        ConstraintSolver()
        .set_candidates(candidates=pipeline_candidate_results)
        .set_sections(sections=2)
        .set_items_per_section(count=3)
        .add_section_constraint(
            attribute_name="price",
            constraint_type=ConstraintType.LEQ,
            constraint_value=7.0,
        )
        .add_section_constraint(
            attribute_name="rating",
            constraint_type=ConstraintType.GEQ,
            constraint_value=7,
        )
        .add_overall_constraint(
            attribute_name="price",
            constraint_type=ConstraintType.LEQ,
            constraint_value=13.0,
        )
        .solve()
    )

    section_ratings = []
    section_prices = []
    total_price = 0
    for section in solution.sections:
        section_rating = 0
        section_price = 0
        for c in section.section_candidates:
            section_rating += c.domain_object.rating
            section_price += c.domain_object.price
            total_price += c.domain_object.price
        section_ratings.append(section_rating)
        section_prices.append(section_price)

    assert (
        all(sr >= 7 for sr in section_ratings)
        and all(sp <= 7 for sp in section_prices)
        and total_price <= 13
        and total_price == solution.overall_attribute_values["price"]
        and section_prices[0] == solution.sections[0].section_attribute_values["price"]
        and len(solution.sections) == 2
        and len(solution.sections[0].section_candidates) == 3
    )
