from frex.pipeline_stages.scorers import CandidateRanker
from examples.ramen_rec.app.models import RamenContext, RamenEaterContext
from examples.ramen_rec.app.pipelines import *
from examples.ramen_rec.tests.conftest import placeholder_ramen_candidate
from frex.utils import ConstraintSolver
from frex.models.constraints import ConstraintType, SectionSetConstraint
from frex.models import DomainObject
from rdflib import URIRef


def test_choose_ramens_using_constraints(
    sim_ramen_pipe,
    test_ramen_101,
):
    pipeline_candidate_results = tuple(
        sim_ramen_pipe(
            context=RamenContext(target_ramen=test_ramen_101),
        )
    )

    solver_sections = (SectionSetConstraint(scaling=100)
        .set_sections(
        sections=(
            DomainObject(uri=URIRef('placeholder.com/day1')),
            DomainObject(uri=URIRef('placeholder.com/day2'))))
        .add_section_count_constraint(exact_count=3)
        .add_section_assignment_constraint(
            section_a_uri=URIRef('placeholder.com/day1'),
            section_b_uri=URIRef('placeholder.com/day2'),
            constraint_type=ConstraintType.AM1
        )
        .add_section_constraint(
            attribute_name="price",
            constraint_type=ConstraintType.LEQ,
            constraint_value=7,
        )
        .add_section_constraint(
        attribute_name="rating",
        constraint_type=ConstraintType.GEQ,
        constraint_value=7,
        ),
    )
    solver = (
        ConstraintSolver(scaling=100)
        .set_candidates(candidates=pipeline_candidate_results)
        .add_overall_item_constraint(
            attribute_name="price",
            constraint_type=ConstraintType.LEQ,
            constraint_value=13,
        )
        .add_overall_count_constraint(exact_count=6)  # not strictly necessary, but improves solving speed by a ton
        .set_section_set_constraints(section_sets=solver_sections)
    )

    solution = (solver.solve())

    section_ratings = []
    section_prices = []
    total_price = 0
    for section_set in solution.solution_section_sets:
        for section in section_set.sections:
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
            and total_price == round(solution.overall_attribute_values["price"], 2)
            and section_prices[0] == solution.solution_section_sets[0].sections[0].section_attribute_values["price"]
            and len(solution.solution_section_sets[0].sections) == 2
            and len(solution.solution_section_sets[0].sections[0].section_candidates)
            == len(solution.solution_section_sets[0].sections[1].section_candidates) == 3
    )
