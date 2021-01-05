from frex.pipeline_stages.scorers import CandidateRanker
from examples.ramen_rec.app.models import RamenContext, RamenEaterContext
from examples.ramen_rec.app.pipelines import *
from examples.ramen_rec.tests.conftest import placeholder_ramen_candidate
from frex.utils import ConstraintSolver
from frex.models.constraints import ConstraintType, SectionSetConstraint
from frex.models import DomainObject
from rdflib import URIRef


def test_choose_ramens_using_constraints(
    mealplan_pipe,
    test_ramen_eater_01,
):
    # pass in the user context and run the pipeline
    output_mealplan = tuple(mealplan_pipe(context=RamenEaterContext(ramen_eater_profile=test_ramen_eater_01),))[0]
    solution = output_mealplan.domain_object

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
    total_price = round(total_price, 2)

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
