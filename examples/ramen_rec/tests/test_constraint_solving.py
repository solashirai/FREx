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

    final_candidates = ConstraintSolver().\
        set_candidates(candidates=pipeline_candidate_results)\
        .set_sections(num_sections=2)\
        .set_items_per_section(count=3)\
        .add_section_constraint(attribute_name='rating', constraint_type=ConstraintType.LEQ, constraint_val=13)\
        .add_overall_constraint(attribute_name='rating', constraint_type=ConstraintType.LEQ, constraint_val=22)\
        .solve()

    section_ratings = []
    total_rating = 0
    for section in final_candidates:
        section_rating = 0
        for c in section:
            section_rating += c.domain_object.rating
            total_rating += c.domain_object.rating
        section_ratings.append(section_rating)

    assert (
        all(sr <= 13 for sr in section_ratings)
        and total_rating <= 22
        and len(final_candidates) == 2
        and len(final_candidates[0]) == 3
    )
